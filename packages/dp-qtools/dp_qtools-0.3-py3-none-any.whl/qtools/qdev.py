from datetime import datetime
from pprint import pprint

def debug(obj):
    """
    Prints a debug line on the console with timestamp (for strings or objects)

    Example:
        > qdev.debug("before loop")

        🛠️  2025-04-14 18:18:06 - before loop

    Args:

        obj (obj): any variable, objects will be pretty printed
    """
    if isinstance(obj, str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🛠️ {timestamp} - {obj}")
    else:
        pprint(obj)
