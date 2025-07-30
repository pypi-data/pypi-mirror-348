import psutil
import time
import threading

try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False

def get_system_specs():
    cpu = psutil.cpu_freq()
    ram = psutil.virtual_memory()
    specs = {
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "CPU Frequency": f"{cpu.current:.2f} MHz" if cpu else "N/A",
        "Total RAM": f"{ram.total / (1024**3):.2f} GB"
    }
    if gpu_available:
        gpus = GPUtil.getGPUs()
        if gpus:
            specs["GPU"] = gpus[0].name
            specs["GPU Memory Total"] = f"{gpus[0].memoryTotal} MB"
    return specs

def _print_usage_bar(label, percent, width=40):
    filled = int(width * percent / 100)
    bar = "█" * filled + "-" * (width - filled)
    print(f"{label}: |{bar}| {percent:.1f}%")

def print_cpu_usage_bar(interval=1.0):
    try:
        while True:
            usage = psutil.cpu_percent(interval=interval)
            _print_usage_bar("CPU Usage", usage)
    except KeyboardInterrupt:
        print("Stopped CPU monitor.")

def print_gpu_usage_bar(interval=1.0):
    if not gpu_available:
        print("GPUtil not installed or GPU not available.")
        return
    try:
        while True:
            gpus = GPUtil.getGPUs()
            if gpus:
                usage = gpus[0].load * 100
                _print_usage_bar("GPU Usage", usage)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped GPU monitor.")

class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0

    def frame(self):
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed >= 1.0:
            fps = self.frame_count / elapsed
            print(f"FPS: {fps:.2f}")
            self.start_time = time.time()
            self.frame_count = 0

class CPSCounter:
    def __init__(self):
        self.click_count = 0
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def click(self):
        with self.lock:
            self.click_count += 1

    def _loop(self):
        while self.running:
            time.sleep(1)
            with self.lock:
                cps = self.click_count
                self.click_count = 0
            print(f"CPS: {cps}")

    def stop(self):
        self.running = False
        self.thread.join()
