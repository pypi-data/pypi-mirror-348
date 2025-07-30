# ip-to-country

**ip-to-country** is a blazing-fast, offline Python library that determines the country for any given IP address (IPv4 or IPv6) using pre-parsed regional internet registry data.

No internet access or third-party APIs required: everything runs **locally and instantly**.

---

## ⚡ Features

- 🌍 **Offline IP Geolocation** – no network calls or external services
- ⚡ **Super Fast Lookup** – optimized with binary search for IPv4
- ✅ **Supports IPv4 and IPv6**
- 📦 **Uses Official RIR Data** – from AFRINIC, RIPE, ARIN, APNIC, and LACNIC
- 🌐 **Country Code + Name Output** – based on ISO 3166
- 🕵️ Supports special codes like `A1` (Anonymous Proxy), `A2`, `O1`, etc.


---

## 📦 Installation

```bash
pip install ip-to-country
```

## 🛠️ Usage

```python
from ip_to_country import IpToCountry

ip_lookup = IpToCountry()
country_info = ip_lookup.ip_to_country("8.8.8.8")

print(country_info)

# Output: {'country_code': 'US', 'ISO3166-1-Alpha-3': 'USA', 'region': 'Americas', 'continent': 'NA', 'languages': ['en-US', 'es-US', 'haw', 'fr'], 'country_name': 'United States of America', 'currency': 'US Dollar', 'currency_code': 'USD'}

```


