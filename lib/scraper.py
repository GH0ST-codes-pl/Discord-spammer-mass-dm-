import discum

class Scraper(object):

    def __init__(self, guild_id, channel_id, token):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.token = token

        self.scraped = []

    def scrape(self):
        try:
            client = discum.Client(token=self.token, log=False)

            client.gateway.fetchMembers(self.guild_id, self.channel_id, reset=False, keep="all")

            @client.gateway.command
            def scraper(resp):
                try:
                    if client.gateway.finishedMemberFetching(self.guild_id):
                        client.gateway.removeCommand(scraper)
                        client.gateway.close()
                except Exception:
                    pass

            client.gateway.run()

            for user in client.gateway.session.guild(self.guild_id).members:
                self.scraped.append(user)

            client.gateway.close()
        except Exception:
            return
    
    def fetch(self, filter_online=False, exclude_bots=True):
        try:
            self.scrape()
            if not self.scraped:
                return []
            
            filtered = []
            # discum members can be a dict or list depending on session state
            # but we collected them into a list in self.scrape()
            for item in self.scraped:
                # If we have full user objects
                if isinstance(item, dict):
                    user = item
                    if exclude_bots and user.get('bot'):
                        continue
                    if filter_online:
                        presence = user.get('presence', {})
                        status = presence.get('status', 'offline')
                        if status == 'offline':
                            continue
                    filtered.append(user)
                else:
                    # If we only have IDs (from generic scraping or fallback)
                    filtered.append({'id': item, 'username': 'Unknown'})
            
            return filtered
        except Exception as e:
            return []

    def fetch_channels(self):
        try:
            client = discum.Client(token=self.token, log=False)
            channels = client.getGuildChannels(self.guild_id).json()
            extracted_channels = [c['id'] for c in channels if c['type'] in [0, 5]]
            return extracted_channels
        except Exception as e:
            return []
