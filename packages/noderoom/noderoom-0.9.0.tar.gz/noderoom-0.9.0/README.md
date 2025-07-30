# NodeRoom

**NodeRoom** is a terminal-based multi-AI chatroom built for Ollama. Create custom AI nodes, chat with them one-on-one or together in different flow modes, and even enable voice replies with `pyttsx3`!

---

## 🚀 Features

- **Create custom AI nodes** with unique prompts and models.
- **Multi-node conversations** in two styles:
  - **Classic Duel**: each AI replies to the user one after another.
  - **Talking Freely**: one AI replies, then the next AI responds to the first.
- **Add or remove active nodes** in your current chat session at any time.
- **Streamed responses** for real-time AI replies.
- **Color-coded AI messages** for clarity and fun.
- **Voice support** via `pyttsx3` (`--voice` flag).
- **Node voting logic** (placeholder): simulate nodes deciding who should respond.
- **Persistent node storage** in `nodes.json`.
- **Simple command interface** with helpful `/help`.

---

## 🛠 Requirements

- Python 3.7+
- [Ollama](https://ollama.com) running locally on `http://localhost:11434`
- Optional:
  - `pyttsx3` for voice output (`pip install pyttsx3`)

---

## 🧠 Usage

```bash
python noderoom.py [--voice]
```

Then use in-terminal commands to interact:

### 🔧 Commands

| Command          | Description |
|------------------|-------------|
| `/create`        | Create a new AI node |
| `/list`          | List all saved nodes |
| `/active`        | Show currently active nodes |
| `/add <name>`    | Add a saved node to the current chat session |
| `/remove <name>` | Remove a node from the current chat session |
| `/ask <name> <question>` | Ask a specific node a question |
| `/flow <1 or 3>` | Set conversation mode: `1 = Classic Duel`, `3 = Talking Freely` |
| `/delete <name>` | Delete a node permanently |
| `/help`          | Show the tutorial/help screen |
| `/quit`          | Exit the chatroom |

---

## 💡 Example Flow

```bash
> /create
Enter node name (unique): Byte
Enter prompt for this node: You're a helpful assistant who always answers concisely.
Enter model for this node (default 'phi'):

> /add Byte
Node 'Byte' added to active chat session.

> Hello, Byte!
[Byte] (model: phi) says:
Hi there! How can I help?
```

---

## 🗣 Voice Mode

Run with `--voice` to enable text-to-speech output (requires `pyttsx3`):

```bash
python noderoom.py --voice
```

---

## 💾 Node Storage

Nodes are saved in `nodes.json` in the same directory. You can back this up or edit it manually if needed.

---

## 🧪 Flow Modes

### 0️⃣ Default
Similar to Classic Duel, but nodes are unaware of eachother. Good for comparisons.

### 1️⃣ Classic Duel

Every active AI node replies to the user's message in order.

### 2️⃣ Coming Soon...

### 3️⃣ Talking Freely

- User says something
- Node A responds
- Node B responds to Node A
- (Back to user)

Great for 2-node debates or collaborative AI creativity!

---

## 📦 License

MIT License — do what you want, just don’t blame me if your AI becomes self-aware.
