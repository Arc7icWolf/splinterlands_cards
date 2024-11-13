import requests
import json

# Send request to the API and return the deserialized response
def get_response(url, session: requests.Session):
    try:
        request = requests.Request("GET", url=url).prepare()
        response = session.send(request, allow_redirects=False)
        response.raise_for_status()
        response = response.json()
        return response
    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return {}


# Get leaderboards for target tokens
def get_leaderboards(session: requests.Session):
    tokens_list = [
        "COLLECTION_POWER",
        "CREDITS",
        "DEC",
        "LICENSE",
        "PLOT",
        "TRACT",
        "REGION",
        "SPSTOTAL",
    ]
    accounts_list = []
    for token in tokens_list:
        url = f"https://api.splinterlands.com/players/richlist?token_type={token}"
        leaderboard = get_response(url, session)
        for account in leaderboard['richlist']:
            accounts_list.append(account['player'])

    return set(accounts_list)


# Main func: print result
def main(session: requests.Session):
    accounts = get_leaderboards(session)
    print(f"Found {len(accounts)} accounts")

if __name__ == "__main__":
    with requests.Session() as session:
        main(session)
