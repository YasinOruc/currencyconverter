import requests
import logging
import os
from dotenv import load_dotenv

# Laad de API-sleutel uit het .env bestand
load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

logging.basicConfig(filename='currency_converter.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200 or 'conversion_rates' not in data:
        raise Exception("Error retrieving exchange rate.")
    exchange_rate = data['conversion_rates'][target_currency]
    return exchange_rate

def convert_currency(base_currency, target_currency, amount):
    rate = get_exchange_rate(base_currency, target_currency)
    result = amount * rate
    return result, rate

def main():
    global language
    language = input("Choose language (EN/NL): ").upper()
    
    if language not in ['EN', 'NL']:
        print("Invalid choice. Defaulting to English.")
        language = 'EN'
    
    welcome_message = "Welcome to the Currency Converter!" if language == 'EN' else "Welkom bij de Valuta-Omzetter!"
    print(welcome_message)
    
    base_currency = input("Enter the base currency code (e.g., EUR): " if language == 'EN' else "Voer de basisvalutacode in (bijv. EUR): ").upper()
    target_currency = input("Enter the target currency code (e.g., USD): " if language == 'EN' else "Voer de doelvalutacode in (bijv. USD): ").upper()
    amount = float(input(f"Enter the amount in {base_currency}: " if language == 'EN' else f"Voer het bedrag in {base_currency} in: "))
    
    try:
        converted_amount, rate = convert_currency(base_currency, target_currency, amount)
        result_message = (f"{amount} {base_currency} = {converted_amount:.2f} {target_currency} "
                          f"(Exchange rate: 1 {base_currency} = {rate:.4f} {target_currency})" if language == 'EN' else
                          f"{amount} {base_currency} = {converted_amount:.2f} {target_currency} "
                          f"(Wisselkoers: 1 {base_currency} = {rate:.4f} {target_currency})")
        print(result_message)
        
        log_message = (f"Converted {amount} {base_currency} to {converted_amount:.2f} {target_currency} at rate {rate}" if language == 'EN' 
                       else f"Geconverteerd {amount} {base_currency} naar {converted_amount:.2f} {target_currency} tegen koers {rate}")
        logging.info(log_message)
        
    except Exception as e:
        error_message = "An error occurred:" if language == 'EN' else "Er is een fout opgetreden:"
        print(f"{error_message} {e}")
        logging.error(f"Error during conversion: {e}" if language == 'EN' else f"Fout tijdens conversie: {e}")

if __name__ == "__main__":
    main()
