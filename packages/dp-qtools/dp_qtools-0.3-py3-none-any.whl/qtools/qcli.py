def message(line: str, kind: str = "success") -> None:
    """
    Prints a CLI message with a preceding emoji.

    Example:
        > qcli.message("5 files copied", "info")

        ℹ️ 5 files copied

    Args:

        line (str): the message

        kind (str): kind of icon: success, info, error, warning, doing, ball, star
    """
    prefixes = {
        "info": "ℹ️  ",
        "error": "❌ ",
        "warning": "⚠️  ",
        "doing": "⏳ ",
        "ball": "🟠 ",
        "star": "⭐ "
    }
    prefix = prefixes.get(kind, "✅ ")
    print(f"{prefix}{line}")
