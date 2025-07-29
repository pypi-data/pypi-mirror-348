# 🌍 YouGotMapped — IP Geolocation Mapper

Ever wondered where that weird IP pinging your router is *actually* from? 
Or maybe you're just nosy (respect). Either way — this script's for you.

**YouGotMapped** is a sassy little Python tool that:
- Auto-fetches your IP (if you dare expose yourself)
- Accepts any domain or IP you throw at it
- Contacts the internet (politely) for geo intel
- Drops a sweet, interactive map

---

## ✨ Features

- Lookup **IP addresses** or **domains** like a pro hacker wannabe
- Detects your public IP like "hi, it's me"
- Maps exact-ish coordinates using [ipinfo.io](https://ipinfo.io)
- Generates a **live HTML map** with red circle vibes
- Dependency check? Yup — it acts like a cool installer
- Quietly avoids private IPs (don’t be that guy)
- Clean, modular CLI with argparse support

---

## 🛠️ Requirements

- Python 3.7+
- Packages: `requests`, `folium`, ... (or let the script install it for you!)
- A totally-free `IPINFO_TOKEN` (get it [here](https://ipinfo.io/signup))

---

## 🚀 Run It Like a Legend

use pip !

```bash
# Download it 
pip install yougotmapped

# Run it 
yougotmapped 
```

```bash
# Clone the repo
git clone https://github.com/diputs-sudo/YouGotMapped.git
cd YouGotMapped

# Option 1: Set token temporarily
export IPINFO_TOKEN=your_ipinfo_token

# Option 2: Let the script prompt you and save it to .env

# Run the thing
$ python3 yougotmapped.py
```

Then follow the prompts like a civilized hacker. You can:
- Press Enter to map **your own IP** (hello, paranoia)
- Or enter someone else's... 👀 (just be cool about it)

---

## 🧪 What You Get

- A readout of city, region, country, and more
- A *Google Maps-esque* HTML file you can open in your browser
- Optional delete at the end (for sneaky folks)

**File:** `ip_geolocation_map.html`

You can keep it. Frame it. Or trash it like a spy after a mission.

---

## 🔐 Security Hints

- We only send your query to **ipinfo.io** — no creepy business
- Private IPs are blocked because that’s just weird
- API token is pulled from env vars (no hardcoded sins here)

---

## 🙋 Who Made This?

> Created by a ghost.   
> No name, no trace, no problem.

Contact? Nah, we don’t do that here.    
If it breaks, fix it yourself — you're clearly smart enough to run this.    

---

## ⭐ Why Star This Repo?

Because it's:
- Actually useful
- Small but mighty
- Funny
- And you’re already here reading this — go on, click ⭐

> This repo was cloned 30+ times before it even had a README. That’s how you know it slaps.

Thanks for checking this out.
You got mapped! 🗺️
