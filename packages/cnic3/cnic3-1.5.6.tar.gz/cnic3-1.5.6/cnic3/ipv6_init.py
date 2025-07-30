from importlib.resources import files
import random

def init():
    pkg = 'cnic3'
    with files(pkg).joinpath('ipv6_pre.py').open('rb') as f:
        text = f.readlines()
    return random.shuffle(text)
