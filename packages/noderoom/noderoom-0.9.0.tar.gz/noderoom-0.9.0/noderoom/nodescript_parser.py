import subprocess
import json
import os
import tempfile
import time

# Path to NodeRoom's __main__.py
NODEROOM_MAIN = os.path.join(os.path.dirname(__file__), "__main__.py")

def run_noderoom_input(user_input, active_nodes, flow_mode=1):
    """
    Launch noderoom with simulated user input and return the response.
    """
    # Prepare a temporary file to simulate input
    script = f"""
import sys
from __main__ import ask_node, load_nodes, NODE_COLORS

nodes = load_nodes()
user_input = {json.dumps(user_input)}
active_nodes = {json.dumps(active_nodes)}

if not active_nodes:
    print("No active AI nodes.")
    sys.exit(0)

if {flow_mode} == 1:
    for idx, node_name in enumerate(active_nodes):
        ask_node(nodes, node_name, user_input, NODE_COLORS[idx % len(NODE_COLORS)])
elif {flow_mode} == 3 and len(active_nodes) >= 2:
    response_a = ask_node(nodes, active_nodes[0], user_input, NODE_COLORS[0])
    response_b = ask_node(nodes, active_nodes[1], response_a, NODE_COLORS[1])
else:
    print("Unsupported flow or insufficient nodes.")
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as temp:
        temp.write(script)
        script_path = temp.name

    try:
        subprocess.run(["python", script_path], check=True)
    finally:
        os.remove(script_path)

if __name__ == "__main__":
    print("=== Demo: Classic Duel ===")
    run_noderoom_input("Hello! What's your take on space travel?", ["Byte", "Toasty"], flow_mode=1)
    print("\n=== Demo: Talking Freely ===")
    run_noderoom_input("What's the future of gaming?", ["Byte", "Toasty"], flow_mode=3)
