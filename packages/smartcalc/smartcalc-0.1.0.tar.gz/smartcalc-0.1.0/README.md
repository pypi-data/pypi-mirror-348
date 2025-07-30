# 🧮 SmartCalc

A minimalistic, keyboard-driven one-line calculator powered by **Pygame**.  

It features a dark/light Tokyo Night-inspired theme, supports:
- variable assignments (`result = 3+5`),  
- post-assignments (`12**3 > c`) c now equals 1728,
- accumulation (`227 >> c`), if both line calculated c = 1995,
- input history navigation,
- and beautifully formatted numeric output.

---

![Bare essentials outside and a beast inside](img/01.png)

## ✨ More Features

- ✅ One-line interactive input interface
- ✅ Variable assignment (`a = 5`) and accumulation (`2 + 3 >> total`)
- ✅ Keyboard-only navigation — no mouse required
- ✅ Tokyo Night color scheme (dark/light switchable)
- ✅ Auto-scaling font size to fit long results
- ✅ Right-aligned results with underscore-separated formatting (`10_000`)
- ✅ Input history navigation with ↑ and ↓ arrows

---

## 🎮 Controls

| Key        | Action                        |
|------------|-------------------------------|
| `Enter`    | Evaluate expression           |
| `Backspace`| Delete one character          |
| `T`        | Toggle dark/light theme       |
| `↑ / ↓`    | Recall previous/next inputs   |

---

## 📦 Requirements

- Python 3.10+
- [`pygame`](https://www.pygame.org/news) (tested with `2.5+`)

Install Pygame via pip if you haven't already:

```bash
uv add pygame
# or
pip install pygame
```

---

## 🔤 Supported Syntax

* **Standard math**: `1 + 2 * 3 - 4 / 2`

* **Variables**:

  ```python
  a = 5
  b = 10
  a + b
  ```

* **Post-assignment (accumulator)**:

  ```python
  10 >> total
  5 >> total   # total now becomes 15
  ```

* **Most Python math operators**: `+`, `-`, `*`, `/`, `**`, `%`

* **Last result is stored in `_`**

---

## 🔧 Fonts

The app uses 
[`FiraCode Nerd Font`](https://github.com/ryanoasis/nerd-fonts) 
for crisp symbols and readability.

* It will be used by default from `fonts/FiraCodeNerdFont-Regular.ttf`.
* If not, the system’s default font will be used as fallback.

To install FiraCode Nerd Font manually:

---

## 🚀 Running the App

```bash
calc  # if installed via uv tool install smartcalc
# or
uv run core.py  # if downloaded from git
# or
python core.py
```

Make sure the `FiraCodeNerdFont-Regular.ttf` in fonts/ directory.

---

## 📂 Project Structure

```
smartcalc/
├── __init__.py
├── core.py
└── fonts/
    └── FiraCodeNerdFont-Regular.ttf

pyproject.toml
README.md
```

---

## 🛠️ Future Ideas

* Cursor movement and editing (←, →)
* Scrollable history buffer
* Command-line launch options (e.g. `--theme=light`)
* User-defined functions
* Save/load variable memory

---

## 📝 License

This project is licensed under the GNU General Public License.

---

Made with 💻 and ☕ by Sergey Samoylov
