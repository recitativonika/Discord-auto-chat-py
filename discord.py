#!/usr/bin/env python3

import requests
import sys
import yaml
import time
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ASCII Art for "Simple DiscordBot"
ascii_art = r"""
   _____ _                 _        _____  _                       _ ____        _   
  / ____(_)               | |      |  __ \(_)                     | |  _ \      | |  
 | (___  _ _ __ ___  _ __ | | ___  | |  | |_ ___  ___ ___  _ __ __| | |_) | ___ | |_ 
  \___ \| | '_ ` _ \| '_ \| |/ _ \ | |  | | / __|/ __/ _ \| '__/ _` |  _ < / _ \| __|
  ____) | | | | | | | |_) | |  __/ | |__| | \__ \ (_| (_) | | | (_| | |_) | (_) | |_ 
 |_____/|_|_| |_| |_| .__/|_|\___| |_____/|_|___/\___\___/|_|  \__,_|____/ \___/ \__|
                    | |                                                              
                    |_|                                                              
"""

print(Fore.CYAN + ascii_art)
print(Fore.GREEN + "Simple DiscordBot")
print(Fore.MAGENTA + "github.com/reciativonika")
print("")  # Add an empty line for better readability

class DiscordBot:
    def __init__(self, token):
        self.base_url = "https://discord.com/api/v9"
        self.headers = {'authorization': token}
        self.username = self.get_username()

    def get_username(self):
        response = requests.get(f"{self.base_url}/users/@me", headers=self.headers).json()
        return f"{response['username']}#{response['discriminator']}"

    def send_message(self, channel_id, message):
        payload = {'content': message}
        response = requests.post(f"{self.base_url}/channels/{channel_id}/messages", headers=self.headers, json=payload)
        return response.json()

def load_config(file_path='config.yaml'):
    with open(file_path) as cfg:
        return yaml.load(cfg, Loader=yaml.FullLoader)

def load_messages(file_path='chat.txt'):  # Changed to chat.txt
    with open(file_path, 'r') as msg_file:
        messages = [line.strip() for line in msg_file if line.strip()]
    return messages

def main():
    config = load_config()
    messages = load_messages()

    # Validate configuration
    if not config.get('token'):
        print(Fore.RED + "[ERROR] No bot token provided in config.yaml!")
        sys.exit()

    if not config.get('channel_id'):
        print(Fore.RED + "[ERROR] No channel ID provided in config.yaml!")
        sys.exit()

    if not messages:
        print(Fore.RED + "[ERROR] No messages found in chat.txt!")  # Changed to chat.txt
        sys.exit()

    # Get delays from configuration
    token_delay = config.get('token_delay', 5)  # Delay for each token
    message_delay = config.get('message_delay', 2)  # Delay for each message
    restart_delay = config.get('restart_delay', 10)  # Delay before restarting

    while True:
        for token in config['token']:
            bot = DiscordBot(token)

            for channel in config['channel_id']:
                # Randomly select a message from the loaded messages
                custom_message = random.choice(messages)
                response = bot.send_message(channel, custom_message)

                if 'content' in response:
                    print(Fore.GREEN + f"[{bot.username}] => Sent to Channel {channel}: {custom_message}")

                time.sleep(message_delay)  # Delay after each message

            print(Fore.YELLOW + f"[INFO] Waiting for {token_delay} seconds before processing the next token...")
            time.sleep(token_delay)  # Delay after processing each token

        print(Fore.YELLOW + f"[INFO] Waiting for {restart_delay} seconds before restarting...")
        time.sleep(restart_delay)  # Delay before restarting

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(Fore.RED + f"[CRITICAL ERROR] {type(e).__name__}: {e}")
