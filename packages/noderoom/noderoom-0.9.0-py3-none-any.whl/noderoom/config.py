# config.py

# Debug settings
DEBUG = {
    "verbose_output": True,
    "show_parsed_tokens": False,
    "trace_execution": False,
}

# Access functions — more maintainable than globals
def debug_enabled(flag: str) -> bool:
    return DEBUG.get(flag, False)
