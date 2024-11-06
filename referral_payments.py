import requests
import json


# Send request, get response
def get_referral_payments(payments_count, player):
    response = requests.get(f"https://api.splinterlands.com/players/referral_payments?page_size={payments_count}&username={player}")
    referral_payments = response.json()
    return referral_payments


def main():
    player_name = "arc7icwolf"
    # First, get number of referral payments received by the target account
    payments = get_referral_payments(1, player_name)
    payments_count = payments["count"]
    # Then, get all referral payments for the target player
    payments = get_referral_payments(payments_count, player_name)
    payments_purchases = payments["purchases"]
    total_payments = 0
    for payment in payments_purchases:
        affiliate_payment = payment["affiliate_payment"]
        # Split "credits" from amount received and sum to total payments received
        total_payments += float(affiliate_payment.split()[0])
    total_payments_in_dollar = total_payments / 1000 # Get value in dollars
    print(f"{player_name} earned {total_payments_in_dollar:.2f} dollars from {payments_count} referral purchases")


if __name__ == "__main__":
    main()
