"""
torch_bench_gpu.py
Quick GEMM-throughput probe for NVIDIA L40 S (or any Ada/Hopper/Blackwell board).

Author: Arnaud Pannatier
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Callable, List, Optional, Tuple

import torch

# ---------------------------------------------------------------------------- #
# Helper: optional INT8 matmul via TorchAO                                     #
# ---------------------------------------------------------------------------- #


def _torchao_int8_matmul() -> (
    Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None
):
    """Return TorchAO's INT8 GEMM kernel if present & compiled."""
    try:
        from torchao.kernel.intmm import int_matmul  # type: ignore

        os.environ.setdefault("TORCHAO_AUTOTUNER_ENABLE", "1")
        return int_matmul
    except Exception:
        return None


# ---------------------------------------------------------------------------- #
# Helper: FP8 tensor creation + scaled-mm kernel                               #
# ---------------------------------------------------------------------------- #


def _make_fp8_tensors_and_kernel(M: int, N: int, K: int):
    """Return (A_fp8, B_fp8, matmul) with layouts accepted by cuBLASLt.

    Requirements (per cuBLASLt docs & PyTorch `_scaled_mm` implementation):
      • A : **row‑major contiguous** (stride = (K, 1)).
      • B : **column‑major *contiguous*** (stride = (1, K)).  Important: merely
        *viewing* a transposed tensor is not enough; the data must be laid out
        physically with first‑dim stride 1.  We therefore build B via
        `torch.empty_strided` to guarantee a valid memory pattern.
    """
    # -------- A (row‑major contiguous) --------------------------------------
    A32 = torch.randn(M, K, device="cuda", dtype=torch.float32)

    # -------- B (column‑major contiguous) ----------------------------------
    # Allocate with Fortran‑style strides (1, K)
    B32 = torch.empty_strided((K, N), (1, K), dtype=torch.float32, device="cuda")
    B32.normal_()  # fill with ~N(0,1)

    # -------- Per‑tensor scales -------------------------------------------
    scale_a = torch.clamp(A32.abs().amax(), min=1.0)
    scale_b = torch.clamp(B32.abs().amax(), min=1.0)
    inv_scale_a = (1.0 / scale_a).to(torch.float32)
    inv_scale_b = (1.0 / scale_b).to(torch.float32)

    # -------- Cast to FP8 ---------------------------------------------------
    A_fp8 = (A32 * inv_scale_a).to(torch.float8_e4m3fn)
    B_fp8 = (B32 * inv_scale_b).to(torch.float8_e4m3fn)

    # -------- Matmul wrapper ----------------------------------------------
    def fp8_matmul(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        out = torch._scaled_mm(
            a, b, out_dtype=torch.float32, scale_a=inv_scale_a, scale_b=inv_scale_b
        )
        return out

    return A_fp8, B_fp8, fp8_matmul


# ---------------------------------------------------------------------------- #
# Core GEMM-throughput kernel                                                  #
# ---------------------------------------------------------------------------- #


def gemm_tput(
    M: int = 8192,
    N: int = 8192,
    K: int = 8192,
    *,
    dtype: torch.dtype = torch.float32,
    iters: int = 200,
    use_tf32: bool = False,
    matmul: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None = None,
) -> Tuple[float, int, float]:
    """Return (TFLOP/s | TOPS, FLOPs, time_ms_per_iter)."""
    torch.cuda.set_device(0)
    torch.backends.cuda.matmul.allow_tf32 = use_tf32
    if dtype is torch.float32:
        torch.set_float32_matmul_precision("high" if use_tf32 else "highest")

    # Allocate A & B
    if dtype is torch.float8_e4m3fn and matmul is None:
        A, B, matmul = _make_fp8_tensors_and_kernel(M, N, K)
    elif dtype is torch.int8:
        A = torch.randint(-128, 128, (M, K), device="cuda", dtype=torch.int8)
        B = torch.randint(-128, 128, (K, N), device="cuda", dtype=torch.int8)
    elif dtype is torch.float8_e4m3fn:
        A32 = torch.randn(M, K, device="cuda", dtype=torch.float32)
        B32 = torch.randn(K, N, device="cuda", dtype=torch.float32)
        A = A32.to(torch.float8_e4m3fn)
        B = B32.to(torch.float8_e4m3fn)
    else:
        A = torch.randn(M, K, device="cuda", dtype=dtype)
        B = torch.randn(K, N, device="cuda", dtype=dtype)

    matmul = matmul or (lambda a, b: a @ b)

    # Warm-up
    print("   Warming up...")
    for _ in range(50):
        matmul(A, B)
    torch.cuda.synchronize()
    print("   Benchmarking...")

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    start.record()
    for _ in range(iters):
        matmul(A, B)
    end.record()
    torch.cuda.synchronize()

    total_time_ms = start.elapsed_time(end) / iters  # per-iter in ms
    flop = 2 * M * N * K
    perf_tflops = flop / (total_time_ms / 1e3) / 1e12  # ms→s then →TFLOP/s
    return perf_tflops, flop, total_time_ms


# ---------------------------------------------------------------------------- #
# ASCII table pretty-printer                                                   #
# ---------------------------------------------------------------------------- #


def draw_table(
    rows: List[Tuple[str, Optional[float], Optional[int], Optional[float], str]],
) -> None:
    w_reg, w_ops, w_time, w_perf, w_note = 14, 18, 14, 16, 28
    hdr = f"+{'-' * w_reg}+{'-' * w_ops}+{'-' * w_time}+{'-' * w_perf}+{'-' * w_note}+"
    print(hdr)
    print(
        f"|{'Regime':^{w_reg}}|{'Ops (G): 2MNK':^{w_ops}}|{'Time/iter (ms)':^{w_time}}|"
        f"{'Perf (T[F]OPS)':^{w_perf}}|{'Notes':^{w_note}}|"
    )
    print(hdr)
    for name, perf, flop, t_ms, note in rows:
        ops_str = f"{flop / 1e9:,.0f}" if flop is not None else "n/a"
        time_str = f"{t_ms:,.2f}" if t_ms is not None else "n/a"
        perf_str = f"{perf:,.2f}" if perf is not None else "n/a"
        print(
            f"|{name:^{w_reg}}|{ops_str:^{w_ops}}|{time_str:^{w_time}}|"
            f"{perf_str:^{w_perf}}|{note:^{w_note}}|"
        )
    print(hdr)


# ---------------------------------------------------------------------------- #
# Main entry-point                                                             #
# ---------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Micro GPU benchmark for pytorch in different regimes"
    )
    parser.add_argument(
        "--size", type=int, default=8192, help="Matrix dimension M=N=K (default 8192)"
    )
    parser.add_argument(
        "--iters", type=int, default=200, help="Averaging iterations (default 200)"
    )
    args = parser.parse_args()

    N = args.size
    iters = args.iters

    tests: List[
        Tuple[
            str,
            torch.dtype | None,
            bool,
            Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None,
            str,
        ]
    ] = [
        ("FP32-CUDA", torch.float32, False, None, ""),
        ("TF32", torch.float32, True, None, "tensor float"),
        ("FP16", torch.float16, False, None, ""),
        ("BF16", torch.bfloat16, False, None, ""),
    ]

    # FP8
    if hasattr(torch, "float8_e4m3fn") and torch.cuda.get_device_capability(0)[0] >= 8:
        tests.append(("FP8-E4M3", torch.float8_e4m3fn, False, None, "torch._scaled_mm"))
    else:
        tests.append(("FP8", None, False, None, "no native support"))

    # INT8
    int8_kernel = _torchao_int8_matmul()
    if int8_kernel is not None:
        tests.append(("INT8", torch.int8, False, int8_kernel, "torchao int_matmul"))
    else:
        tests.append(("INT8", None, False, None, "torchao missing"))

    rows: List[Tuple[str, Optional[float], Optional[int], Optional[float], str]] = []
    for name, dtype, tf32, matmul, note in tests:
        if dtype is None:
            rows.append((name, None, None, None, note))
            continue
        try:
            print(f"Running {name}...")
            perf, flop, t_ms = gemm_tput(
                M=N, N=N, K=N, dtype=dtype, iters=iters, use_tf32=tf32, matmul=matmul
            )
            rows.append((name, perf, flop, t_ms, note))
        except (RuntimeError, AssertionError) as e:
            rows.append((name, None, None, None, str(e).splitlines()[0]))

    draw_table(rows)


if __name__ == "__main__":
    if not torch.cuda.is_available():
        sys.exit("CUDA device not detected – aborting.")
    main()
