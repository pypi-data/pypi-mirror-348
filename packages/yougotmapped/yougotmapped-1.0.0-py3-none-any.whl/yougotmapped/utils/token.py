# utils/token.py
import os
from pathlib import Path
from dotenv import load_dotenv

def get_api_token():
    # Force .env path to the installed package folder
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    token = os.getenv("IPINFO_TOKEN")
    if token:
        return token

    print("'IPINFO_TOKEN' environment variable not found.")
    print("To use this tool, you need a free API token from ipinfo.io.")
    print("Visit: https://ipinfo.io/signup")
    token = input("Enter your IPInfo token: ").strip()

    if token:
        save = input("Would you like to save this token to a .env file for future runs? (yes/no): ").strip().lower()
        if save in ['yes', 'y']:
            try:
                with open(env_path, "a") as env_file:
                    env_file.write(f"\nIPINFO_TOKEN={token}\n")
                print("Token saved to .env file. Make sure to load it in your script using python-dotenv or similar.")
            except Exception as e:
                print(f"Error saving token: {e}")
        return token

    return None
