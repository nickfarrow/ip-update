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

def git_stash(newbranch):
    prior_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=gitloc).decode('utf-8').strip()
    print(prior_branch)

    gs = subprocess.check_output(["git", "stash"], cwd=gitloc)
    print(gs.decode('unicode_escape'))
    
    gc = subprocess.check_output(["git", "checkout", newbranch], cwd=gitloc)
    print(gc.decode('unicode_escape'))

    return prior_branch


def git_restore(prior_branch):
    gc = subprocess.check_output(["git", "checkout", prior_branch], cwd=gitloc)
    print(gc.decode('unicode_escape'))

    gs = subprocess.check_output(["git", "stash", "pop"], cwd=gitloc)
    print(gs.decode('unicode_escape'))
    return


def update_git():
    ga = subprocess.check_output(["git", "add", aliasfile], cwd=gitloc)
    print(ga.decode('unicode_escape'))
  
    gc = subprocess.check_output(["git", "commit", "-m", "'Automatic IP address update for rasperry pi'"], cwd=gitloc)
    print(gc.decode('unicode_escape'))

    gp = subprocess.check_output(["git", "push", 'origin', branch], cwd=gitloc)
    print(gp.decode('unicode_escape'))
    
    return

prior_branch = git_stash(branch)
lines, current_ip = get_plugfiles_ip()
print("aliasrc pi IP: {}".format(current_ip))
git_restore(prior_branch)


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
        
        print("Stashing any existing git changes...")
        prior_branch = git_stash(branch)

        print("\n\nUpdating {}".format(aliasfile))
        update_aliasrc(lines, ip)
        
        print("\n\nUpdating git branch {}".format(branch))
        update_git()
        
        print("\n\n Restoring stashed changes...")
        git_restore(prior_branch)

        current_ip = ip
        print("Updated.")

    time.sleep(60*15)
