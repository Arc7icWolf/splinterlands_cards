import requests
import json


# Send request, get response
def get_referral_payments(payments_count, player):
    response = requests.get(f"https://api.splinterlands.com/players/referral_payments?page_size={payments_count}&username={player}")
    referral_payments = response.json()
    return referral_payments


def main():
    player_name = "arc7icwolf"
    payments = get_referral_payments(1, player_name)
    payments_count = payments["count"]
    payments = get_referral_payments(payments_count, player_name)
    payments_purchases = payments["purchases"]
    total_payments = 0
    for payment in payments_purchases:
        affiliate_payment = payment["affiliate_payment"]
        total_payments += float(affiliate_payment.split()[0])
    total_payments_in_dollar = total_payments / 1000
    print(f"{total_payments_in_dollar:.2f} dollars from {payments_count} referral purchases")


if __name__ == "__main__":
    main()
