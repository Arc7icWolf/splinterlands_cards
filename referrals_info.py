import requests
import json
import argparse


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
def main(player_name, session: requests.Session):
    payments_count, total_payments_in_dollar = get_referral_payments_info(
        player_name, session
    )
    referrals_amount = get_referrals_amount(player_name, session)
    print(
        f"{player_name.capitalize()} earned {total_payments_in_dollar:.2f} dollars "
        f"from {referrals_amount} referrals "
        f"doing {payments_count} eligible purchases."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get referrals payments and referrals count."
    )
    parser.add_argument(
        "player_name",
        nargs="?",
        default="arc7icwolf",
        help="Insert an existing Splinterlands account username.",
    )

    args = parser.parse_args()

    with requests.Session() as session:
        main(args.player_name, session)
