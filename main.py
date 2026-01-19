import os
import sys
import json
import time
import psutil
import random
import logging
import asyncio
from tasksio import TaskPool
from datetime import datetime
from lib.scraper import Scraper
from aiohttp import ClientSession, FormData

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)

def print_banner():
    """Display colorful ASCII banner with author credits"""
    banner = """
\x1b[38;5;196m╔═══════════════════════════════════════════════════════════════════════╗
\x1b[38;5;202m║  ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗                ║
\x1b[38;5;208m║  ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗               ║
\x1b[38;5;214m║  ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║               ║
\x1b[38;5;220m║  ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║               ║
\x1b[38;5;226m║  ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝               ║
\x1b[38;5;190m║  ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                ║
\x1b[38;5;154m║                                                                       ║
\x1b[38;5;118m║           ███╗   ███╗ █████╗ ███████╗███████╗    ██████╗ ███╗   ███╗ ║
\x1b[38;5;82m║           ████╗ ████║██╔══██╗██╔════╝██╔════╝    ██╔══██╗████╗ ████║ ║
\x1b[38;5;46m║           ██╔████╔██║███████║███████╗███████╗    ██║  ██║██╔████╔██║ ║
\x1b[38;5;51m║           ██║╚██╔╝██║██╔══██║╚════██║╚════██║    ██║  ██║██║╚██╔╝██║ ║
\x1b[38;5;45m║           ██║ ╚═╝ ██║██║  ██║███████║███████║    ██████╔╝██║ ╚═╝ ██║ ║
\x1b[38;5;39m║           ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝ ╚═╝     ╚═╝ ║
\x1b[38;5;33m║                                                                       ║
\x1b[38;5;27m║                    \x1b[1m\x1b[38;5;201m⚡ MASS DM ADVERTISER ⚡\x1b[0m                      ║
\x1b[38;5;21m║                                                                       ║
\x1b[38;5;57m║              \x1b[38;5;255m🚀 Created by: \x1b[1m\x1b[38;5;196mGH0ST-codes-pl\x1b[0m\x1b[38;5;57m 🚀                  ║
\x1b[38;5;93m║          \x1b[38;5;255m🔗 GitHub: \x1b[4m\x1b[38;5;51mgithub.com/GH0ST-codes-pl\x1b[0m\x1b[38;5;93m 🔗             ║
\x1b[38;5;129m║                                                                       ║
\x1b[38;5;165m║  \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Single User DM    \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Mass DM    \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Mass Channel      \x1b[38;5;165m║
\x1b[38;5;201m║  \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Multi-User DM     \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Message Content Fetch           \x1b[38;5;201m║
\x1b[38;5;201m║  \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Image Support     \x1b[38;5;226m[\x1b[38;5;46m✓\x1b[38;5;226m]\x1b[38;5;255m Rate Limit Protection           \x1b[38;5;201m║
\x1b[38;5;196m╚═══════════════════════════════════════════════════════════════════════╝\x1b[0m
"""
    print(banner)
    print("\x1b[38;5;208m⚠️  WARNING: \x1b[38;5;255mSelfbots are against Discord ToS. Use at your own risk!\x1b[0m")
    print("\x1b[38;5;46m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m\n")

class Discord(object):

    def __init__(self):
        if sys.platform == "linux":
            self.clear = lambda: os.system("clear")
        else:
            self.clear = lambda: os.system("cls")

        self.clear()
        print_banner()  # Display colorful banner with credits
        
        self.tokens = []
        self.cached_headers = {}

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None
        self.invite = None

        try:
            for line in open("data/tokens.txt"):
                self.tokens.append(line.replace("\n", ""))
        except Exception:
            open("data/tokens.txt", "a+").close()
            logging.info("Please insert your tokens \x1b[38;5;9m(\x1b[0mtokens.txt\x1b[38;5;9m)\x1b[0m")
            sys.exit()

        logging.info("Successfully loaded \x1b[38;5;9m%s\x1b[0m token(s)\n" % (len(self.tokens)))
        
        print("\x1b[38;5;51m╔════════════════════════════════════╗\x1b[0m")
        print("\x1b[38;5;51m║\x1b[0m         \x1b[1m\x1b[38;5;226mSELECT MODE\x1b[0m              \x1b[38;5;51m║\x1b[0m")
        print("\x1b[38;5;51m╚════════════════════════════════════╝\x1b[0m\n")
        print("\x1b[38;5;46m  [1]\x1b[0m 🎯 Single User DM")
        print("\x1b[38;5;201m  [2]\x1b[0m 📢 Mass DM")
        print("\x1b[38;5;196m  [3]\x1b[0m 📺 Mass Channel")
        print("\x1b[38;5;51m  [4]\x1b[0m 👥 Target Multiple IDs\n")
        self.mode = input("\x1b[38;5;51m[?]\x1b[0m Choice \x1b[38;5;51m→\x1b[0m ")
        if self.mode not in ["1", "2", "3", "4"]:
            sys.exit()
        
        if self.mode == "1":
            self.user_id = input("\x1b[38;5;51m[?]\x1b[0m User ID \x1b[38;5;51m→\x1b[0m ")
        elif self.mode == "4":
            self.user_ids = input("\x1b[38;5;51m[?]\x1b[0m User IDs (comma separated or file.txt) \x1b[38;5;51m→\x1b[0m ")
        else:
            server_input = input("\x1b[38;5;51m[?]\x1b[0m Invite or Guild ID \x1b[38;5;51m→\x1b[0m ")
            if server_input.isdigit():
                 self.guild_id = server_input
                 if self.mode == "2":
                     self.channel_id = input("\x1b[38;5;51m[?]\x1b[0m Channel ID \x1b[38;5;51m→\x1b[0m ")
                 else:
                     self.channel_id = None
                 self.invite = None
            else:
                 self.invite = server_input

        # Ask for amount for Single User (1) AND Mass Channel (3)
        if self.mode in ["1", "3"]:
            try:
                self.amount = int(input("\x1b[38;5;51m[?]\x1b[0m Amount \x1b[38;5;51m→\x1b[0m "))
            except Exception:
                self.amount = 1
        else:
            self.amount = 1

        self.use_msg_id = input("\x1b[38;5;51m[?]\x1b[0m Use Message ID for content? (y/n) \x1b[38;5;51m→\x1b[0m ").lower() == "y"
        if self.use_msg_id:
            self.fetch_channel_id = input("\x1b[38;5;51m[?]\x1b[0m Message Channel ID \x1b[38;5;51m→\x1b[0m ")
            self.fetch_message_id = input("\x1b[38;5;51m[?]\x1b[0m Message ID \x1b[38;5;51m→\x1b[0m ")
            self.message = "" # Will be fetched later
        else:
            self.message = input("\x1b[38;5;51m[?]\x1b[0m Message \x1b[38;5;51m→\x1b[0m ").replace("\\n", "\n")
        try:
            self.delay = float(input("\x1b[38;5;51m[?]\x1b[0m Delay \x1b[38;5;226m(recommended: 3-5s)\x1b[0m \x1b[38;5;51m→\x1b[0m "))
        except Exception:
            self.delay = 3.0  # Default 3 seconds for safety

        self.image = input("\x1b[38;5;51m[?]\x1b[0m Image Path \x1b[38;5;8m(Enter for none)\x1b[0m \x1b[38;5;51m→\x1b[0m ").strip()
        if self.image != "" and not os.path.exists(self.image):
            logging.info("File not found \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (self.image))
            sys.exit()
            
        print("\n\x1b[38;5;46m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m")
        print("\x1b[38;5;226m⚡ Starting bot... Please wait...\x1b[0m")
        print("\x1b[38;5;46m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m\n")

    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)

    async def headers(self, token):
        if token in self.cached_headers:
            return self.cached_headers[token]

        async with ClientSession() as client:
            async with client.get("https://discord.com/app") as response:
                cookies = str(response.cookies)
                try:
                    dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                    sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]
                except:
                    dcfduid = ""
                    sdcfduid = ""
        
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__dcfduid=%s; __sdcfduid=%s; locale=en-US" % (dcfduid, sdcfduid),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "te": "trailers",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9015 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE1Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTUgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTYzNjQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM0OTk4LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }

        self.cached_headers[token] = headers
        return headers

    async def fetch_message_content(self, token, channel_id, message_id):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.get(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("content", "")
                    else:
                        logging.info(f"Failed to fetch message {message_id} (Status: {response.status})")
                        return None
        except Exception as e:
            logging.info(f"Error fetching message: {e}")
            return None

    async def login(self, token):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.get("https://discord.com/api/v9/users/@me") as response:
                    if response.status == 200:
                        logging.info("Valid token \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                    elif response.status == 401:
                        logging.info("Invalid account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 403:
                        logging.info("Locked account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
        except Exception:
            pass

    async def join(self, token):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.post("https://discord.com/api/v9/invites/%s" % (self.invite)) as response:
                    json = await response.json()
                    if response.status == 200:
                        self.guild_name = json["guild"]["name"]
                        self.guild_id = json["guild"]["id"]
                        self.channel_id = json["channel"]["id"]
                        logging.info("Successfully joined %s \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (self.guild_name[:20], token[:59]))
                    elif response.status == 401:
                        logging.info("Invalid account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 403:
                        logging.info("Locked account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info("Ratelimited \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
        except Exception:
            pass

    async def create_dm(self, token, user_id):
        try:
            # Add random delay to appear more human-like
            await asyncio.sleep(random.uniform(1.0, 3.0))
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.post("https://discord.com/api/v9/users/@me/channels", json={"recipients": [user_id]}) as response:
                    json = await response.json()
                    if response.status == 200:
                        return json["id"]
                    elif response.status == 401:
                        logging.info("Invalid account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403:
                        logging.info("Locked account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                        return False
                    elif response.status == 429:
                        logging.info("Ratelimited \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        await asyncio.sleep(random.uniform(10.0, 15.0))  # Longer wait on rate limit
                        return await self.create_dm(token, user_id)
                    else:
                        return False
        except Exception:
            return await self.create_dm(token, user_id)

    async def direct_message(self, token: str, channel: str):
        try:
            # Add random delay before sending message
            await asyncio.sleep(random.uniform(1.5, 4.0))
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                if self.image != "":
                    data = FormData()
                    data.add_field("payload_json", json.dumps({"content": self.message, "nonce": self.nonce(), "tts": False}))
                    data.add_field("file", open(self.image, "rb"))
                    request = client.post("https://discord.com/api/v9/channels/%s/messages" % (channel), data=data)
                else:
                    request = client.post("https://discord.com/api/v9/channels/%s/messages" % (channel), json={"content": self.message, "nonce": self.nonce(), "tts":False})

                async with request as response:
                    response_data = await response.json()
                    if response.status == 200:
                        logging.info("Successfully sent message \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                    elif response.status == 401:
                        logging.info("Invalid account \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403 and response_data["code"] == 40003:
                        logging.info("Ratelimited \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        await asyncio.sleep(random.uniform(10.0, 15.0))
                        await self.direct_message(token, channel)
                    elif response.status == 403 and response_data["code"] == 50007:
                        logging.info("User has direct messages disabled \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                    elif response.status == 403 and response_data["code"] == 40002:
                        logging.info("Locked \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        self.tokens.remove(token)
                        return False
                    elif response.status == 429:
                        logging.info("Ratelimited \x1b[38;5;9m(\x1b[0m%s\x1b[38;5;9m)\x1b[0m" % (token[:59]))
                        await asyncio.sleep(random.uniform(10.0, 15.0))
                        await self.direct_message(token, channel)
                    else:
                        return False
        except Exception:
            await self.direct_message(token, channel)

    async def send(self, token: str, user: str):
        channel = await self.create_dm(token, user)
        if channel == False:
            return await self.send(random.choice(self.tokens), user)
        response = await self.direct_message(token, channel)
        if response == False:
            return await self.send(random.choice(self.tokens), user)

    async def send_channel(self, token: str, channel_id: str):
        response = await self.direct_message(token, channel_id)
        if response == False:
            return await self.send_channel(random.choice(self.tokens), channel_id)

    async def start(self):
        if len(self.tokens) == 0:
            logging.info("No tokens loaded.")
            sys.exit()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    await pool.put(self.login(token))
                else:
                    self.stop()
                    
        if len(self.tokens) == 0: self.stop()

        if self.use_msg_id and self.message == "":
            logging.info("Fetching message content...")
            content = await self.fetch_message_content(self.tokens[0], self.fetch_channel_id, self.fetch_message_id)
            if content:
                self.message = content
                logging.info(f"Successfully fetched message content: \x1b[38;5;226m{self.message[:50]}...\x1b[0m")
            else:
                logging.info("Could not fetch message content. Exiting.")
                self.stop()

        if self.mode != "1" and self.mode != "4":
            print()
            if self.invite:
                logging.info("Joining server.")
                print()

                async with TaskPool(1_000) as pool:
                    for token in self.tokens:
                        if len(self.tokens) != 0:
                            await pool.put(self.join(token))
                            if self.delay != 0: await asyncio.sleep(self.delay)
                        else:
                            self.stop()
            else:
                 logging.info("Skipping join (Guild ID provided).")
            
            if len(self.tokens) == 0: self.stop()

            scraper = Scraper(
                token=self.tokens[0],
                guild_id=self.guild_id,
                channel_id=self.channel_id
            )
            
            if self.mode == "3":
                 self.targets = scraper.fetch_channels()
                 self.targets = self.targets * self.amount
                 logging.info("Successfully scraped \x1b[38;5;9m%s\x1b[0m channels (Multipier: %s)" % (len(self.targets) // self.amount, self.amount))
            else:
                  self.targets = scraper.fetch()
                  logging.info("Successfully scraped \x1b[38;5;9m%s\x1b[0m members" % (len(self.targets)))
        elif self.mode == "4":
            if os.path.exists(self.user_ids):
                with open(self.user_ids, "r") as f:
                    self.targets = [line.strip() for line in f if line.strip()]
            else:
                self.targets = [i.strip() for i in self.user_ids.split(",") if i.strip()]
            logging.info("Successfully loaded \x1b[38;5;9m%s\x1b[0m user IDs" % (len(self.targets)))
        else:
            self.targets = [self.user_id] * self.amount

        print()
        logging.info("Sending messages.")
        print()

        if len(self.tokens) == 0: self.stop()

        async with TaskPool(1_000) as pool:
            for target in self.targets:
                if len(self.tokens) != 0:
                    if self.mode == "3":
                        await pool.put(self.send_channel(random.choice(self.tokens), target))
                    else:
                        await pool.put(self.send(random.choice(self.tokens), target))
                    if self.delay != 0: await asyncio.sleep(self.delay)
                else:
                    self.stop()

if __name__ == "__main__":
    client = Discord()
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        sys.exit()
