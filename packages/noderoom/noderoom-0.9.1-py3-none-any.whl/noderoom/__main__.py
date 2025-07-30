from noderoom.formatting import format_markdown as markdown
import json
import os
import requests
import time
import sys

def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Mac and Linux (posix)
    else:
        os.system('clear')

clear_screen()

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None  # Voice support disabled if no pyttsx3 installed

NODES_FILE = 'nodes.json'

def handle_streamed_response(streamed_lines):
    full_response = ""
    for line in streamed_lines:
        if not line.strip():
            continue
        data = json.loads(line)
        chunk = data.get("response", "")
        # Format chunk on the fly
        formatted_chunk = markdown(chunk, True)
        print(formatted_chunk, end="", flush=True)
        full_response += chunk
        if data.get("done", False):
            break
    print()  # Newline after done
    return full_response

class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

NODE_COLORS = [
    Colors.LIGHT_RED + Colors.BOLD,
    Colors.LIGHT_GREEN + Colors.BOLD,
    Colors.YELLOW + Colors.BOLD,
    Colors.LIGHT_BLUE + Colors.BOLD,
    Colors.LIGHT_PURPLE + Colors.BOLD,
    Colors.LIGHT_CYAN + Colors.BOLD,
    Colors.LIGHT_WHITE + Colors.BOLD,
]

def load_nodes():
    if not os.path.exists(NODES_FILE):
        return {}
    with open(NODES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_nodes(nodes):
    with open(NODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2)

def tutorial():
    print(f"""
{colors.LIGHT_GREEN}Welcome to {Colors.BOLD}NodeRoom{Colors.END}{colors.LIGHT_GREEN}! Let's get you started with creating your first node.{colors.END}

- Nodes are your AI agents with a name, model, and prompt.
- You can create many nodes and chat with them anytime.
- Use /add to bring nodes into your current chat session.
- Commands you can use:
   /create - Create a new AI node
   /list   - List all your AI nodes
   /active - Show AI nodes active in this chat session
   /add    - Add an existing AI node to the current chat session
   /remove - Remove a node from the current chat session
   /ask    - Ask a question to a specific active node
   /delete - Delete an AI node permanently
   /flow   - Set conversation flow mode (1=Classic, 3=Talking Freely)
   /help   - Show this message again
   /quit   - Exit the program

Let's create your first node now!
""")

def create_node(nodes):
    name = input("Enter node name (unique): ").strip()
    if name in nodes:
        print(f"Node '{name}' already exists! Pick a different name.")
        return
    prompt = input("Enter prompt for this node: ").strip()
    model = input("Enter model for this node (default 'phi'): ").strip() or "phi"
    nodes[name] = {"prompt": prompt, "model": model}
    save_nodes(nodes)
    print(f"Node '{name}' created and saved.")

def list_nodes(nodes):
    if not nodes:
        print("You have no AI nodes yet.")
    else:
        print("Your AI nodes:")
        for n in nodes:
            print(f" - {n}")

def list_active_nodes(active_nodes):
    if not active_nodes:
        print("No nodes currently active in this chat session.")
    else:
        print("Active nodes in this chat session:")
        for n in active_nodes:
            print(f" - {n}")

def get_ollama_response(prompt, model="phi", stream=False):
    ollama_api_url = "http://localhost:11434/api/generate"
    try:
        data = {"model": model, "prompt": prompt, "stream": stream}
        response = requests.post(ollama_api_url, json=data, stream=stream)
        response.raise_for_status()

        if stream:
            return handle_streamed_response(response.iter_lines())
        else:
            result = response.json()
            print(result.get("response", "").strip())
            return result.get("response", "").strip()
    except Exception as e:
        print(f"Error contacting OLLaMA: {e}")
        return ""

def speak_text(engine, text):
    if engine:
        engine.say(text)
        engine.runAndWait()

def ask_node(nodes, node_name, question, color_code, voice_engine=None):
    node = nodes[node_name]
    full_prompt = f"{node['prompt']}\nUser: {question}\nAI:"
    print(f"\n{color_code}[{node_name}] (model: {node['model']}) says:{Colors.END}\n")
    response = get_ollama_response(full_prompt, model=node['model'], stream=True)
    # No extra print here to avoid doubling output
    if voice_engine and response.strip():
        speak_text(voice_engine, response)
    return response

def delete_node(nodes, active_nodes, node_name):
    if node_name not in nodes:
        print(f"No node named '{node_name}' found.")
        return
    if node_name in active_nodes:
        active_nodes.remove(node_name)
    del nodes[node_name]
    save_nodes(nodes)
    print(f"Node '{node_name}' deleted.")

def nodes_vote_to_respond(nodes, active_nodes, user_input):
    # Simple voting system: nodes score their willingness to respond
    votes = {}
    for node_name in active_nodes:
        prompt = nodes[node_name]['prompt']
        # We just simulate voting by asking each node "Should I respond to: <input>?"
        vote_prompt = f"{prompt}\nUser: Should you respond to this input? \"{user_input}\" (Answer with YES or NO)\nAI:"
        response = get_ollama_response(vote_prompt, model=nodes[node_name]['model'], stream=False)
        votes[node_name] = response.strip().upper().startswith("YES")
    return votes

def main():
    voice_enabled = False
    voice_engine = None

    if '--voice' in sys.argv:
        if pyttsx3:
            voice_engine = pyttsx3.init()
            voice_enabled = True
            print(f"{Colors.LIGHT_GREEN}Voice output enabled!{Colors.END}")
        else:
            print(f"{Colors.LIGHT_RED}pyttsx3 not installed! Install it with pip. Voice disabled.{Colors.END}")

    nodes = load_nodes()
    if not nodes:
        tutorial()
        create_node(nodes)

    active_nodes = []
    flow_mode = 1  # Default: 1 = Classic Duel, 3 = Talking Freely

    print("\nType /help for commands.")

    while True:
        cmd = input("\n> ").strip()
        if cmd == '':
            continue

        if cmd.startswith('/'):
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ''

            if command == '/quit':
                print("Goodbye, human.")
                break
            elif command == '/help':
                tutorial()
            elif command == '/list':
                list_nodes(nodes)
            elif command == '/active':
                list_active_nodes(active_nodes)
            elif command == '/create':
                create_node(nodes)
            elif command == '/delete':
                if arg:
                    delete_node(nodes, active_nodes, arg)
                else:
                    print("Usage: /delete <node_name>")
            elif command == '/add':
                if arg:
                    if arg not in nodes:
                        print(f"No node named '{arg}' found.")
                    elif arg in active_nodes:
                        print(f"Node '{arg}' is already active in this chat session.")
                    else:
                        active_nodes.append(arg)
                        print(f"Node '{arg}' added to active chat session.")
                else:
                    print("Usage: /add <node_name>")
            elif command == '/remove':
                if arg:
                    if arg in active_nodes:
                        active_nodes.remove(arg)
                        print(f"Node '{arg}' removed from active chat session.")
                    else:
                        print(f"Node '{arg}' is not active in this chat session.")
                else:
                    print("Usage: /remove <node_name>")
            elif command == '/ask':
                parts_ask = arg.split(maxsplit=1)
                if len(parts_ask) == 2:
                    node_name, question = parts_ask
                    if node_name not in active_nodes:
                        print(f"Node '{node_name}' is not active. Use /add to add it.")
                    else:
                        idx = active_nodes.index(node_name) % len(NODE_COLORS)
                        ask_node(nodes, node_name, question, NODE_COLORS[idx], voice_engine if voice_enabled else None)
                else:
                    print("Usage: /ask <node_name> <question>")
            elif command == '/flow':
                if arg in ('1', '3'):
                    flow_mode = int(arg)
                    print(f"Conversation flow set to mode {flow_mode}.")
                else:
                    print("Usage: /flow 1 or /flow 3")
            else:
                print(f"Unknown command: {command}")
        else:
            # User input that nodes will respond to depending on flow_mode
            if not active_nodes:
                print("No active AI nodes. Use /add to add nodes to this chat.")
                continue

            if flow_mode == 1:
                # Classic Duel: nodes respond one by one to user input
                for idx, node_name in enumerate(active_nodes):
                    print(f"\n{NODE_COLORS[idx % len(NODE_COLORS)]}[{node_name}] responding...{Colors.END}")
                    ask_node(nodes, node_name, cmd, NODE_COLORS[idx % len(NODE_COLORS)], voice_engine if voice_enabled else None)
            elif flow_mode == 3:
                # Talking Freely: user input -> node A responds -> node B responds -> back to user
                print(f"\n{NODE_COLORS[0]}[{active_nodes[0]}] responding...{Colors.END}")
                response_a = ask_node(nodes, active_nodes[0], cmd, NODE_COLORS[0], voice_engine if voice_enabled else None)

                print(f"\n{NODE_COLORS[1]}[{active_nodes[1]}] responding...{Colors.END}")
                response_b = ask_node(nodes, active_nodes[1], response_a, NODE_COLORS[1], voice_engine if voice_enabled else None)
            else:
                print("Unsupported flow mode. Use /flow 1 or /flow 3.")

if __name__ == "__main__":
    main()
