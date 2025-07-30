
---

## 🤖 Greetron

**Greetron** is a lightweight Python package designed for chatbots and virtual assistants that need friendly, professional, or informal greetings and goodbyes — with optional personalization via the user's name.

---

### ✨ Features

* ✅ Randomized greetings and goodbyes
* ✅ Supports **formal** and **informal** tones
* ✅ Adds the user’s **name** naturally into responses
* ✅ Lightweight and dependency-free

---

### 📦 Installation

If published to PyPI:

```bash
pip install greetron
```


### 🚀 Usage

```python
from greetron import get_random_greeting, get_random_goodbye

print(get_random_greeting())  # formal greeting
print(get_random_greeting("Aryan"))  # formal greeting with name
print(get_random_greeting("Aryan", mode="informal"))  # Informal greeting with name

print(get_random_goodbye())  # formal goodbye
print(get_random_goodbye("Aryan"))  # formal goodbye with name
print(get_random_goodbye("Aryan", mode="informal"))  # inFormal goodbye with name
```

---

### 📂 Greeting Modes

| Mode       | Description                                 |
| ---------- | ------------------------------------------- |
| `formal`   | Professional tone (e.g., business/chatbots) |
| `informal` | Friendly/casual tone for personal bots      |

---

### 🔧 Function Signatures

```python
get_random_greeting(name: str = None, mode: str = "informal") -> str
get_random_goodbye(name: str = None, mode: str = "informal") -> str
```

* `name`: Optional — A user’s name to personalize the message
* `mode`: Optional — `"formal"` or `"informal"` tone

---

### 🧠 Example Output

```python
get_random_greeting("Aryan", mode="formal")
# "Hello, Aryan! How may I assist you today?"

get_random_goodbye("Aryan", mode="informal")
# "Catch ya later, Aryan!"
```

---

### 📘 License

MIT License

---

Let me know if you'd like:

* Badge support (e.g., version, build)
* GitHub Actions setup for publishing to PyPI
* CLI or Streamlit demo interface

