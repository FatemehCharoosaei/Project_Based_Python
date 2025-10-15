import requests
def get_exchange_rate(base_currency, target_currency):
   url = f"https://v6.exchangerate-api.com/v6/2cfc1e026e998825155a0c8d/latest/{base_currency}"
   response = requests.get(url)
   
   try:
       data = response.json()
   except requests.exceptions.JSONDecodeError:
       print("❌ Failed to decode JSON. Response content:", response.text)
       return None
   if 'conversion_rates' in data and target_currency in data['conversion_rates']:
       return data['conversion_rates'][target_currency]
   else:
       print("❌ API response error:", data)
       return None
def convert_currency(amount, exchange_rate):
   return amount * exchange_rate
if __name__ == '__main__':
   base_currency = input("Enter base currency: ").upper()
   target_currency = input("Enter target currency: ").upper()
   amount = float(input("Enter amount: "))
   
   exchange_rate = get_exchange_rate(base_currency, target_currency)
   if exchange_rate:
       converted_amount = convert_currency(amount, exchange_rate)
       print(f"{amount} {base_currency} is {converted_amount:.2f} {target_currency}")
   else:
       print("❌ Failed to fetch exchange rate.")