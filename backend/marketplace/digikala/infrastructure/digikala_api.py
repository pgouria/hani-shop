import requests
import os


ORDERS_API_URL = "https://seller.digikala.com/api/v1/orders/"
VARIANT_API_URL = "https://seller.digikala.com/api/v1/variants/"

class DigikalaClient:
    def __init__(self):
        self.DIGIKALA_TOKEN = os.environ.get("DIGIKALA_TOKEN")
    def headers(self):
        return {
            "authorization": f"{self.DIGIKALA_TOKEN}",
            "Content-Type": "application/json"
        }
    def fetch_orders(self):
        response = requests.get(ORDERS_API_URL, headers=self.headers())
        response.raise_for_status()
        data = response.json()
        items = data.get('data').get('items')
        return items
    def fetch_variants(self):
        all_items = []
        page = 1

        while True:
        
            params = {'page': page}

            
            response = requests.get(VARIANT_API_URL, headers=self.headers(), params=params, timeout=30)
            response.raise_for_status()

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                
                data = response.json()
                
                # Get items and pagination info
                items = data.get('data', {}).get('items', [])
                pager = data.get('data', {}).get('pager', {})

                # Add items from current page to all_items
                all_items.extend(items)

                # Check if there are more pages
                if page >= pager.get('total_page', 1):
                    break

                
                page += 1

            else:
                # Print the error code and message if the request failed
                print(f"Error {response.status_code}: {response.text}")
                break
        return all_items
        







  
          


      
                     
  