# 🚀 ABS Tool — Auto Bumper Script for Discord

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20VPS-important)
![Made by](https://img.shields.io/badge/Made%20By-Mar-orange)

> ⚠️ Coded & Developed by **Mar.**  
> ⚠️ Use at your own risk. This may get your Discord account banned.

```
*----------------------------------------------------------------*
|     ABS Tool                *        Coded & Developed by Mar. |
*----------------------------------------------------------------*
| Please refer to this README if you're confused                 |
| Don't use this on your main Discord account,                  |
| May get your account banned.                                  |
*----------------------------------------------------------------*
| This tool requires a verified Discord account to work.         |
*----------------------------------------------------------------*
```

---

## 📌 What is ABS Tool?

**ABS (Auto Bumper Script)** is a Python-based script that automatically sends the `!d bump` command to Disboard every 2 hours — using **user tokens**, not bots, to avoid detection.

Designed to be stealthy, lightweight, and VPS-friendly.

---

## ⚙️ Features

- ✅ Fully automated bumping  
- ✅ Supports **multiple tokens**
- ✅ Spoofs headers and JSON data to avoid detection
- ✅ Logs every bump attempt
- ✅ Works perfectly on VPS (Linux)

---

## 📷 Screenshots

- 🆘 Help command output:  
  ![Help Screenshot](https://files.catbox.moe/3a0n6p.png)

- 📜 `abs_tool.log` in action:  
  ![Log Screenshot](https://files.catbox.moe/svueko.png)

- 🔄 One bumper active:  
  ![One Token Active](https://files.catbox.moe/jfy573.png)

---

## 🧰 Requirements

- Python 3.x  
- `requests` Python module  
  Install it using:
  ```bash
  pip3 install requests
  ```

- A **verified Discord alt account**  
- Channel ID + Guild (Server) ID  
- User token(s) saved in `tokens.txt` (one per line)

---

## 🔑 How to Get Your User Token

> ⚠️ Only works on browser Discord (not desktop app)

1. Open [Discord in your browser](https://discord.com).
2. Press `F12` to open **Developer Tools**.
3. Go to the **Network** tab → enable **XHR**.
4. Send any message in any channel.
5. Click the related request → go to `Headers`.
6. Look for the `Authorization` field — copy it.
7. Paste it into a file called `tokens.txt`.

---

## 🛠️ Usage

```bash
python3 abs.py -c <CHANNEL_ID> -g <GUILD_ID>
```

### Example:

```bash
python3 abs.py -c 123456789012345678 -g 987654321098765432
```

### CLI Help

```
usage: abs.py [-h] -c CHANNEL -g GUILD

Disboard Auto-Bump Service

options:
  -h, --help            Show this help message and exit
  -c, --channel CHANNEL Channel ID where bump command should be sent
  -g, --guild GUILD     Server (Guild) ID
```

---

## 🖥️ VPS Recommended (Run 24/7)

To keep ABS running continuously:

```bash
tmux
python3 abs.py -c <CHANNEL_ID> -g <GUILD_ID>
```

Then `Ctrl+B`, then `D` to detach safely.

---

## ⚠️ Warnings

- 🚫 Don’t use on your **main Discord account** — alt only.
- 🔥 May bypass bot detection, but still violates Discord's TOS.
- 💀 Your account **can be disabled or banned**. Use responsibly.
- 🧪 This project is for **educational and research purposes** only.

---

## 🧑‍💻 Author

Made with 🤍 by **Mar**  
GitHub: [TheDesiignerr](https://github.com/TheDesiignerr)

---

> "If you know, you know."
