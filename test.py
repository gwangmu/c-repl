#!/usr/bin/python

import re
import sys
import subprocess

out = subprocess.run(["clang", "-fsyntax-only", "-Xclang", "-ast-dump", sys.argv[1]], capture_output=True)
lines = out.stdout.decode().split('\n')

p = "Decl .* {} '([^']+)'".format(sys.argv[2])

for line in lines:
    re_type = re.search(p, line)
    if (re_type):
        print(re_type.group(1))
        break
