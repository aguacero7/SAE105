import subprocess
import sys

with open("Dependencies") as file:
    for line in file:
        subprocess.check_call([sys.executable,"-m","pip","install",str(line[:-1])])
