# <span style="color:pink">CharmCord</span>

### The Ultimate Python-Based String Scripting Engine for Discord Bots

---

## 📊 Project Stats
![PyPI - Version](https://img.shields.io/pypi/v/CharmCord)
![PyPI - Downloads](https://img.shields.io/pypi/dm/CharmCord?color=green&label=downloads)
![Total Downloads](https://static.pepy.tech/personalized-badge/CharmCord?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads)
![License](https://img.shields.io/pypi/l/CharmCord)
![Code Stats](https://tokei.rs/b1/github/LilbabxJJ-1/CharmCord)
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)

---

## 🚀 Version 1.0.0 — Official Release!

CharmCord is now officially out of beta!  
A huge thank you to everyone who supported its growth.  
Expect new features, enhancements, and even more powerful tools in future versions!

### 📦 New Function Additions

- `$addButton`
- `$addDropdown`
- `$dropdownOption`
- `$setGlobalUserVar`
- `$getGlobalUserVar`
- `$interactionReply`

### ❗ Deprecated Functions

- `$buttonSend`
- `$slashSend`

---

## 🛠️ Installation

Install CharmCord from PyPI:

```bash
pip install CharmCord
```

---

## ⚙️ Quick Start Example

```python
from CharmCord import charmclient

bot = charmclient(prefix="!", case_insensitive=False, intents=("all",))

bot.on_ready(
    Code="$console[Bot is Ready]"
)

bot.command(
    name="Ping",
    code="$sendMessage[$channelID; Pong!! $ping]"
)

bot.run("<<YOUR_TOKEN_HERE>>")
```

---

## 🤝 Contributing

CharmCord is open-source and contributions are warmly welcomed! If you'd like to improve the project, fix bugs, or add new features, follow these steps:

1. Fork the repository and clone it locally.
2. Create a new branch for your feature or fix.
3. Make and test your changes.
4. Follow PEP8 and good documentation practices.
5. Commit with meaningful messages.
6. Push your branch and open a pull request.
7. Wait for review — and get merged in!

---

## 👥 Contributors

<a href="https://github.com/LilbabxJJ-1/CharmCord/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=LilbabxJJ-1/CharmCord"  alt="CharmCord Contributors"/>
</a>
