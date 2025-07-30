#Uses bundled libs in Lib folder, from a default installation. This means it has no dependencies needed when installing
import sys,time

def printslow(string):
    for carrier in string:
        sys.stdout.write(carrier)
        time.sleep(0.01)
    sys.stdout.write("\n")