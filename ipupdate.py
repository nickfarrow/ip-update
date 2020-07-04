import subprocess
import time
import re

aliasfile = "/home/nick/plugfiles/.config/.aliasrc"
branch = "arch-x1"
gitloc = '/'.join(aliasfile.split('/')[:-2])

def get_plugfiles_ip():
    with open(aliasfile, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if "pi=" in line:
                return lines, line.split("@")[1].split("'")[0].strip()
    return False, False



def update_aliasrc(lines, newip):
    for i, line in enumerate(lines):
        if 'pi=' in line:
            lines[i] = "alias pi='ssh pi@{}\n".format(newip)

    
    with open(aliasfile, 'w') as f:
        for line in lines:
            f.write(line)
    
    return


def update_git():
    gc = subprocess.check_output(["git", "checkout", branch], cwd=gitloc)
    print(gc.decode('unicode_escape'))

    ga = subprocess.check_output(["git", "add", aliasfile], cwd=gitloc)
    print(ga.decode('unicode_escape'))
   
    time.sleep(5)

    gc = subprocess.check_output(["git", "commit", "-m", "'Automatic IP address update for rasperry pi'"], cwd=gitloc)
    print(gc.decode('unicode_escape'))

    gp = subprocess.check_output(["git", "push", 'origin', branch], cwd=gitloc)
    print(gp.decode('unicode_escape'))

    return


lines, current_ip = get_plugfiles_ip()
print("aliasrc pi IP: {}".format(current_ip))

while True:
    try:
        ip = subprocess.check_output(["curl", "-s", "https://ifconfig.co/"]).decode('utf-8').strip()

        if 'html' in ip:
            raise ConnectionError("Failed to connect to ifconfig.com")

        print("new IP: {}".format(ip))

    except Exception as e:
        print(e)
        continue
   
    if ip != current_ip:
        print("Different IPs {}, {}".format(current_ip, ip))
        
        print("\n\nUpdating {}".format(aliasfile))
        update_aliasrc(lines, ip)
        
        print("\n\nUpdating git branch {}".format(branch))
        update_git()
        
        current_ip = ip
        print("Updated.")

    time.sleep(60*15)


