# *----------------------------------------------------------------*
# |     ABS Tool                *        Coded & Developed by Mar. |
# *----------------------------------------------------------------*
# | Please refer to the README.md if you're confused               |
# | Don't use this script on your main discord account,            |
# | May get your account banned.                                   |
# *----------------------------------------------------------------*
# | This tool requires a verfied discord account to work.          |
# *----------------------------------------------------------------*

import os
import time
import json
import requests
import threading
import logging
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DISCORD_API = "https://discord.com/api/v9"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
DISBOARD_APP_ID = "302050872383242240"
X_SUPER_PROPERTIES = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI5NDI4MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
X_CONTEXT_PROPERTIES = "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQifQ=="

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("abs_tool.log"),
        logging.StreamHandler()
    ]
)

class DisboardBumper:
    def __init__(self, token, channel_id, guild_id):
        self.token = token
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.session = self._create_session()
        self.base_headers = self._build_headers()
        self.command_info = None
        self.last_bump_time = None
        self.running = True
        self.bump_count = 0

    def _create_session(self):
        """Create resilient HTTP session"""
        session = requests.Session()
        retry = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=('GET', 'POST'),
            respect_retry_after_header=True
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        session.mount('https://', adapter)
        return session

    def _build_headers(self):
        """Construct headers for Discord API"""
        return {
            "Authorization": self.token,
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "X-Super-Properties": X_SUPER_PROPERTIES,
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "UTC",
            "Origin": "https://discord.com",
            "Referer": f"https://discord.com/channels/{self.guild_id}/{self.channel_id}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    def get_disboard_command_info(self):
        """Fetch Disboard command ID and version"""
        url = f"{DISCORD_API}/guilds/{self.guild_id}/application-command-index"
        try:
            response = self.session.get(url, headers=self.base_headers, timeout=15)
            if response.status_code == 200:
                for command in response.json().get("application_commands", []):
                    if command.get("application_id") == DISBOARD_APP_ID and command.get("name") == "bump":
                        return {
                            "id": command["id"],
                            "version": command["version"]
                        }
            logging.error(f"Failed to find Disboard command. Status: {response.status_code}")
        except Exception as e:
            logging.error(f"Command discovery error: {str(e)}")
        return None

    def execute_bump(self):
        """Execute the /bump command"""
        if not self.command_info:
            self.command_info = self.get_disboard_command_info()
            if not self.command_info:
                return False

        url = f"{DISCORD_API}/interactions"
        headers = {**self.base_headers, "X-Context-Properties": X_CONTEXT_PROPERTIES}

        payload = {
            "type": 2,
            "application_id": DISBOARD_APP_ID,
            "channel_id": self.channel_id,
            "guild_id": self.guild_id,
            "session_id": f"auto_bump_{int(time.time())}",
            "nonce": str(int(time.time() * 1000)),
            "data": {
                "version": self.command_info["version"],
                "id": self.command_info["id"],
                "name": "bump",
                "type": 1,
                "options": [],
                "application_command": {
                    "id": self.command_info["id"],
                    "application_id": DISBOARD_APP_ID,
                    "version": self.command_info["version"],
                    "default_permission": True,
                    "default_member_permissions": None,
                    "type": 1,
                    "name": "bump",
                    "description": "Bump this server",
                    "guild_id": self.guild_id
                }
            }
        }

        try:
            response = self.session.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code in (200, 204):
                self.last_bump_time = datetime.utcnow()
                self.bump_count += 1
                return True
            logging.warning(f"Bump failed: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"Bump execution error: {str(e)}")
        return False

    def bump_loop(self):
        """Main loop that runs bumps every 2 hours"""
        logging.info(f"Starting bump service for token: {self.token[:15]}...")
        
        while self.running:
            # Calculate next bump time (2 hours from last successful bump)
            next_bump = self.last_bump_time + timedelta(hours=2) if self.last_bump_time else datetime.utcnow()
            
            # If we haven't done first bump or it's time for next bump
            if not self.last_bump_time or datetime.utcnow() >= next_bump:
                success = self.execute_bump()
                status = "SUCCESS" if success else "FAILED"
                logging.info(f"Bump attempt {self.bump_count + 1}: {status}")
            
            # Sleep until next scheduled bump or 30 seconds if failed
            next_check = next_bump if success else datetime.utcnow() + timedelta(seconds=30)
            sleep_seconds = max((next_check - datetime.utcnow()).total_seconds(), 5)
            
            # Sleep in chunks so we can respond to stop signals
            for _ in range(int(sleep_seconds)):
                if not self.running:
                    return
                time.sleep(1)

    def start(self):
        """Start the bump service in a new thread"""
        self.thread = threading.Thread(target=self.bump_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the bump service"""
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=5)

def load_tokens(file_path="tokens.txt"):
    """Load tokens from file with validation"""
    tokens = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                token = line.strip()
                if token.startswith("mfa.") or (len(token) > 50 and "." in token):
                    tokens.append(token)
    return tokens

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Disboard Auto-Bump Service")
    parser.add_argument("-c", "--channel", required=True, help="Channel ID where bump command should be executed")
    parser.add_argument("-g", "--guild", required=True, help="Server (Guild) ID")
    args = parser.parse_args()

    tokens = load_tokens()
    if not tokens:
        logging.error("No valid tokens found in tokens.txt")
        return

    logging.info(f"Loaded {len(tokens)} tokens. Starting bump services...")
    
    bumpers = []
    for token in tokens:
        bumper = DisboardBumper(token, args.channel, args.guild)
        bumper.start()
        bumpers.append(bumper)
        time.sleep(1)

    try:
        # Display status updates
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"ABS TOOL Running. {len(bumpers)} Bumpers active")
            print("=" * 60)
            for i, bumper in enumerate(bumpers):
                status = "ACTIVE" if bumper.running else "STOPPED"
                last_bump = bumper.last_bump_time.strftime("%Y-%m-%d %H:%M:%S UTC") if bumper.last_bump_time else "Never"
                print(f"Token {i+1}: {bumper.token[:20]}...")
                print(f"  Status: {status} | Bumps: {bumper.bump_count} | Last: {last_bump}")
                print("-" * 60)
            print("\nPress Ctrl+C to stop all services")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Stopping all bump services...")
        for bumper in bumpers:
            bumper.stop()
        logging.info("All services stopped. Exiting.")

if __name__ == "__main__":
    main()
