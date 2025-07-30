# Nebulib v0.3

Nebulib is a Python library focused on **real-time system performance monitoring**.

## Latest Changelog
- Added CPS Monitor Function

## Features

- Get full system specs (CPU, RAM, GPU)
- Live CPU usage bar in terminal
- GPU usage monitor (NVIDIA only)
- FPS Counter
- CPS monitor

## Example

```python
from nebulib import get_system_specs, print_cpu_usage_bar, FPSCounter

print(get_system_specs())
print_cpu_usage_bar()

fps = FPSCounter()
while True:
    fps.tick()
    fps.show_fps()
```
