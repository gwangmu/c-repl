#!/usr/bin/python

import os
import subprocess

out = subprocess.run("./a.out 3>&1 >/dev/null 2>/dev/null", shell=True, capture_output=True)
print(out.stdout.decode())
