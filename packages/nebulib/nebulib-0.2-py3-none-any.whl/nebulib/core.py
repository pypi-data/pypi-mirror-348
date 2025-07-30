import datetime
import hashlib
import random
import string
import psutil
import time

def reverse_pretty(text):
    return ' '.join(word[::-1] for word in text.split())

def emoji_encrypt(text):
    emojis = ['😃', '😎', '🤖', '👻', '🔥', '✨']
    return ''.join(random.choice(emojis) + c for c in text)

def days_until(date_str, date_format="%Y-%m-%d"):
    target = datetime.datetime.strptime(date_str, date_format)
    return (target - datetime.datetime.now()).days

def print_cpu_usage(duration=5):
    for _ in range(duration):
        usage = psutil.cpu_percent(interval=1)
        bars = '|' * int(usage // 2)
        print(f"CPU Usage: [{bars:<50}] {usage}%")

def generate_ascii_art(width=40, height=10):
    chars = ['*', '.', '+', 'x', '-']
    art = ''
    for _ in range(height):
        art += ''.join(random.choice(chars) for _ in range(width)) + '\n'
    return art

def funny_hash(text):
    hash_obj = hashlib.sha256(text.encode())
    base = hash_obj.hexdigest()
    emoji_mix = ['😅', '😂', '🤯', '💥', '😬']
    return ''.join(random.choice(emoji_mix) + c for c in base[:16])
