import re
import random
import os

def parse_spintax(text):
    """
    Parses spintax in the format {option1|option2|option3}
    """
    pattern = re.compile(r'\{([^{}]+)\}')
    while True:
        match = pattern.search(text)
        if not match:
            break
        options = match.group(1).split('|')
        text = text.replace(match.group(0), random.choice(options), 1)
    return text

def load_proxies():
    """
    Loads proxies from data/proxies.txt
    Expected format: ip:port or user:pass@ip:port
    """
    proxies = []
    path = "data/proxies.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    if "://" not in line:
                        # Assume http if no protocol specified
                        line = "http://" + line
                    proxies.append(line)
    return proxies

def load_blacklist():
    """
    Loads blacklisted user IDs from data/blacklist.txt
    """
    blacklist = set()
    path = "data/blacklist.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    blacklist.add(line)
    return blacklist

def resolve_placeholders(text, user_data=None):
    """
    Replaces placeholders like {username} and {mention}
    """
    if user_data:
        text = text.replace("{username}", user_data.get("username", "user"))
        text = text.replace("{mention}", f"<@{user_data.get('id', '')}>")
    return text
