# UniFi‑API‑Client Python Port

A Python port of the [Art‑of‑WiFi/Unifi‑API‑Client](https://github.com/Art-of-WiFi/Unifi-API-client) library for interacting with Ubiquiti UniFi controllers.  
This project preserves the original PHP functionality via Python’s `requests` and offers:

- cURL‑style options mirroring the PHP implementation  
- Session management (login/logout)  
- Controller‑side backup generation & download  
- Most REST/stat endpoints translated to Python  

> **Note:** User‑management methods (create/update/delete) are currently non‑functional due to authorization/404 errors. Contributions welcome!

---

## Features

- Login to UniFi OS & classic controllers  
- Generate and download network backups  
- Mirror PHP’s cURL options for timeouts, headers, SSL, etc.  
- All major API/stat endpoints converted  
- CSRF handling for UniFi OS  

---

## Dependencies

- http
- sys
- requests
- From requests.exceptions import Timeout, RequestException
- time
- re
- json
- urllib.parse
- http.client
- logging
- base64

## Example Usage

```
from client import Client

# Initialize (disable SSL verify if using self‑signed certs)
client = Client(
    user="admin",
    password="secret",
    baseurl="https://your-controller-ip",
    ssl_verify=False
)

# Login
client.login()

# List sites
sites = client.list_sites()
print(sites)

# Generate & download backup
bak = client.generate_backup(days=0)   # returns [{'url': '/dl/backup/XYZ.unf'}]
content = client.download_backup(bak[0]['url'])
with open("backup.unf", "wb") as f:
    f.write(content)

# Logout
client.logout()
```

## Known Issues

- User management (create/update/delete) as well as some other admin required permissions return 404/unauthorized
- Some endpoints don't get met

## License

- Same as the original github
- MIT