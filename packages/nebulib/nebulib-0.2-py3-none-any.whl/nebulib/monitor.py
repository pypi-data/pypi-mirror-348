import platform
import psutil
import shutil
import subprocess
import time
import os

class FPSCounter:
    def __init__(self):
        self.last_time = time.time()
        self.frames = 0
        self.fps = 0

    def tick(self):
        self.frames += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            self.fps = self.frames
            self.frames = 0
            self.last_time = current_time

    def show_fps(self):
        print(f"FPS: {self.fps}")

def get_system_specs():
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM (Total)": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
    }

    # GPU Info (NVIDIA)
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            stderr=subprocess.DEVNULL,
            encoding="utf-8"
        ).strip().split("\n")
        for i, gpu in enumerate(result):
            info[f"GPU {i}"] = gpu
    except Exception:
        info["GPU"] = "NVIDIA GPU not found or nvidia-smi not available"

    return info

def print_cpu_usage_bar(duration=5):
    width = shutil.get_terminal_size((80, 20)).columns
    for _ in range(duration):
        usage = psutil.cpu_percent(interval=1)
        bars = int((usage / 100) * (width - 20))
        print(f"CPU Usage: [{'#' * bars:<{width - 20}}] {usage:.2f}%")

def print_gpu_usage_bar(duration=5):
    try:
        width = shutil.get_terminal_size((80, 20)).columns
        for _ in range(duration):
            result = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                stderr=subprocess.DEVNULL,
                encoding="utf-8"
            ).strip().split("\n")
            for i, val in enumerate(result):
                usage = int(val)
                bars = int((usage / 100) * (width - 20))
                print(f"GPU {i} Usage: [{'#' * bars:<{width - 20}}] {usage}%")
            time.sleep(1)
    except Exception:
        print("GPU monitoring requires NVIDIA GPU and nvidia-smi.")
