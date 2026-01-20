import re
import random
import os
import json
import base64

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

def get_random_ua():
    return random.choice(USER_AGENTS)

def get_sec_headers(ua):
    """
    Generates realistic Sec-CH-UA headers based on the User-Agent.
    """
    platform = "Windows"
    if "Macintosh" in ua: platform = "macOS"
    elif "Linux" in ua: platform = "Linux"
    
    # Simple mapping for common browsers
    if "Chrome" in ua:
        ua_list = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
    elif "Edg" in ua:
        ua_list = '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"'
    else:
        ua_list = '"Not_A Brand";v="8", "Chromium";v="120"'

    return {
        "sec-ch-ua": ua_list,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"'
    }

def get_fingerprint(ua):
    """
    Generates a base64 encoded x-super-properties fingerprint based on the User-Agent.
    """
    os_name = "Windows"
    if "Macintosh" in ua: os_name = "Mac OS X"
    elif "Linux" in ua: os_name = "Linux"
    
    browser = "Chrome"
    if "Firefox" in ua: browser = "Firefox"
    elif "Edg" in ua: browser = "Edge"

    # Using a more recent client build number
    client_build_number = 256191 + random.randint(0, 500)

    props = {
        "os": os_name,
        "browser": browser,
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": ua,
        "browser_version": "120.0.0.0",
        "os_version": "10" if os_name == "Windows" else "10.15.7",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": client_build_number,
        "client_event_source": None
    }
    
    return base64.b64encode(json.dumps(props).encode()).decode()

def parse_spintax(text):
# ... rest of the file ...
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
