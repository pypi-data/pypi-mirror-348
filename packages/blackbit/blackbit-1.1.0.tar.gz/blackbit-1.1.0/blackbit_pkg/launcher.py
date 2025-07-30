import pkg_resources
import subprocess
import sys
from pathlib import Path

def main():
    # Locate the bundled .exe
    exe_path = pkg_resources.resource_filename("blackbit_pkg", "data/blackbit.exe")
    # Launch it, forwarding any arguments
    args = [exe_path] + sys.argv[1:]
    return subprocess.call(args)
