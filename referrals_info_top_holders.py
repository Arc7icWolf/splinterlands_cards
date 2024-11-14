import requests
import json
from players_list import get_leaderboards


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


# Get purchases made by referrals and return them
def get_referral_payments(payments_count, player, session: requests.Session):
    url = f"https://api.splinterlands.com/players/referral_payments?page_size={payments_count}&username={player}"
    payments = get_response(url, session)
    return payments


# Sum all the eligible payments and return the total
def sum_total_payments(purchases):
    total_payments = 0
    for payment in purchases:
        affiliate_payment = payment["affiliate_payment"]
        # Split "credits" from the amount received and then sum to the total
        total_payments += float(affiliate_payment.split()[0])
    total_payments_in_dollar = total_payments / 1000  # Get value in dollars
    return total_payments_in_dollar


# Get and return number and total value of referral payments
def get_referral_payments_info(player, session: requests.Session):
    # First, get number of referral payments received by target account
    payments = get_referral_payments(1, player, session)
    payments_count = payments["count"]
    # Then, get all referral payments for target player
    payments = get_referral_payments(payments_count, player, session)
    payments_purchases = payments["purchases"]
    total_payments_in_dollar = sum_total_payments(payments_purchases)
    return payments_count, total_payments_in_dollar


# Get the amount of users referred by target player
def get_referrals_amount(player, session: requests.Session):
    url = f"https://api.splinterlands.com/players/referral_users?username={player}"
    referrals = get_response(url, session)
    return referrals["count"]


# Main func: print result
def main(session: requests.Session):
    player_name_list = get_leaderboards(session)
    referral_info_list = []
    for player_name in player_name_list:
        referrals_amount = get_referrals_amount(player_name, session)
        if referrals_amount == 0:
            continue
        payments_count, total_payments_in_dollar = get_referral_payments_info(
            player_name, session
        )
        referral_info = (
            f"@{player_name} earned {total_payments_in_dollar:.2f} dollars "
            f"from {referrals_amount} referrals "
            f"doing {payments_count} eligible purchases.\n"
        )
        print(referral_info)
        referral_info_list.append(referral_info)
        print("added to the list")

    sorted_referral_info_list = sorted(referral_info_list, key=lambda x: int(x.split("from ")[1].split(" referrals")[0]), reverse=True)

    with open("referral_info.txt", "a", newline="", encoding="utf-8") as file:
        for info in sorted_referral_info_list:
            file.write(info)


if __name__ == "__main__":
    with requests.Session() as session:
        main(session)
