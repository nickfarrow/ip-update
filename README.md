# ip-update
Update ssh ip address in an .aliasrc file, pushed to a git repository.

# Usage
Modify:
```
aliasfile = "/home/nick/plugfiles/.config/.aliasrc"
branch = "arch-x1"
gitloc = '/'.join(aliasfile.split('/')[:-2])
```
to match your .aliasrc file, git branch name, and branch directory respectively.

Run in background on a device and your ip will constantly be up to date so you can ssh in.
