import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]
SHEETY_USER_ENDPOINT = os.environ["SHEETY_USER_ENDPOINT"]

class DataManager:

    def __init__(self):
        self._user = os.environ["SHEETY_USRERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.token = os.getenv("SHEETY_TOKEN")

        self._authorization = {
            "Authorization": f"Bearer {self.token}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers = self._authorization)
        data = response.json()
        print(data)

        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                headers= self._authorization,
                json=new_data
            )



    def get_customer_emails(self):
        email_list = []
        response = requests.get(url= SHEETY_USER_ENDPOINT, headers= self._authorization)

        for user in  response.json()["users"]:
            email_list.append(user["email"])

        return email_list
