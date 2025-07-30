# 🎌 Anime Title Fetcher

A lightweight Python script that fetches the original anime title (Japanese or English-Japanese) from a user-provided input using the Kitsu API.

## 🌟 Features

- ✅ Clean and minimal code.
- 🔎 Automatically corrects and formats the input.
- 🎴 Returns the official title (e.g., "demon slayer" ➜ "Kimetsu no Yaiba").
- ⚡ Built-in caching for faster repeated queries.
- 🌐 Uses the reliable Kitsu.io anime database.

---

## 📦 Requirements

- Python 3.7+
- requests library

Install requests if not already installed:

```bash
pip install requests
```

---

## How to Use

Import the function and call it with an anime name string:

```python
from your_module import get_ani_title

title = get_ani_title("demon slayer")
print(title)  # Output: Kimetsu no Yaiba
```

---

## Examples

| Input            | Output               |
|------------------|----------------------|
| demon slayer     | Kimetsu no Yaiba     |
| attack on titan  | Shingeki no Kyojin   |
| one piece        | One Piece            |
| my hero academia | Boku no Hero Academia|
| naruto_shippuden | Naruto: Shippuden    |

---

## Credits

- Anime data fetched from the [Kitsu API](https://kitsu.io/api/edge/anime).
- Developed by [Arise](https://t.me/wxxoxo).
- Thanks to the open-source community for inspiration and support.
