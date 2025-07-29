# GPUBENCH

GPUBench is a benchmarking tool for evaluating the performance of a GPU under pytorch. 

It helps you measure the actual GFLOPS of your GPU in different regime. 

you can run it without installing it by using the following command:

```bash
uvx torch-bench-gpu
```


# To add the right torch

```bash
uv add --pre torch --default-index https://pypi.org/simple --index https://download.pytorch.org/whl/nightly/cu126
```
