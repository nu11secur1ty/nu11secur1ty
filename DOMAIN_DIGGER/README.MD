### DOMAIN DIGGER - Advanced Domain Discovery Tool

Professional-grade domain enumeration and subdomain discovery platform

![](https://github.com/nu11secur1ty/nu11secur1ty/blob/master/DOMAIN_DIGGER/docs/domain_gidder.jpg)

# Online in Win 11 PowerShell
```
(Invoke-WebRequest -Uri "https://raw.githubusercontent.com/nu11secur1ty/nu11secur1ty/master/DOMAIN_DIGGER/domain_digger.py").Content | python - your_damain --options
```
- example:
```
(Invoke-WebRequest -Uri "https://raw.githubusercontent.com/nu11secur1ty/nu11secur1ty/master/DOMAIN_DIGGER/domain_digger.py").Content | python - your_domain_name --workers 50
```
