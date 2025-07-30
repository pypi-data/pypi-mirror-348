import re


def format_commit_message(commit_msg: str) -> str:
    """Strip conventional commit prefix and format the rest of the message into a human-readable sentence.

    Example:
        Input: "feat(auth): add login functionality"
        Output: "Add login functionality."

        Input: "fix: resolve memory leak"
        Output: "Resolve memory leak."

    Args:
        commit_msg (str): The original commit message.

    Returns:
        str: Human-readable formatted commit message.

    """
    # Regex to match conventional commit prefix
    match = re.match(r'^(?:\w+)(?:\([\w\-]+\))?!?:\s*(.+)', commit_msg)
    if match:
        core_msg = match.group(1)
    else:
        core_msg = commit_msg.strip()

    # Capitalize first word and ensure ending punctuation
    formatted = core_msg[0].upper() + core_msg[1:]
    if not formatted.endswith(('.', '!', '?')):
        formatted += '.'

    return formatted
