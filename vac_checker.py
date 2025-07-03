import requests
import json

def get_vac_status(steam_id, api_key):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error querying the Steam API: {response.status_code}")
        return None
    data = response.json()
    if "players" not in data or len(data["players"]) == 0:
        print("User not found or incorrect SteamID.")
        return None
    return data["players"][0]

def main():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("File config.json not found! Create it with API key.")
        return

    api_key = config.get("api_key")
    if not api_key:
        print("API key is not set in config.json!")
        return

    steam_id = input("Enter SteamID64: ").strip()
    if not steam_id.isdigit() or len(steam_id) < 15:
        print("Invalid SteamID64.")
        return

    result = get_vac_status(steam_id, api_key)
    if result:
        print(f"\nSteamID: {result['SteamId']}")
        print(f"VAC ban: {result['VACBanned']}")
        print(f"Number of game bans: {result['NumberOfGameBans']}")
        print(f"Days since the last ban: {result['DaysSinceLastBan']}")
        print(f"Economic ban: {result['EconomyBan']}")

if __name__ == "__main__":
    main()
