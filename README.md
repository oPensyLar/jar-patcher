# Jar patcher

Hot pacthing JAR over MS Windows & Linux distros



### Notes

- You need elevate priv on local machine tests
- You need change you Active Directory creds on deploy.py
- You need add you servers on srv.lst
- You need change paths to find



### Deploy

Change you Active Directory creds on deploy.py (line 7, line 8)


```python
# login creds
user = "you-ad-user"
passwd = "you-ad-password"
```


Change dir to find (G:\ on this example) on scripts\log4j_vuln_upgrade.ps1 line 106

```
Find-Files "G:\\" $targetClass
```


Change dir to find ("/root" "/mnt" on this example) on scripts\log4j_vuln_upgrade.py line 8

```
find_dir = ["/root", "/mnt"]
```

### Credentials

# Features

 * Unpack, repack & hot patching JAR
 * Backup original files
 * Can undo all changes
 * Logs all steps
 * Multi path JAR finder
 * Auto OS recon
