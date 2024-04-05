import os

def hostinfo(opdir):
    os.popen(f"systeminfo > {opdir}\\hostinfo.txt")
    return f"{opdir}\\hostinfo.txt"

def ipconfig(opdir):
    os.popen(f"ipconfig > {opdir}\\ipconfig.txt")
    return f"{opdir}\\ipconfig.txt"