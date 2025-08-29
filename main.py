
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "DEL"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
      
        # slowing down requests to avoid rate limit
        time.sleep(2)

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Search for Flights and Send Notifications ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days= 30)

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: ₹{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

    # ============= Sending Email when the flight is found ================

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")

        email_list = data_manager.get_customer_emails()
        notification_manager.send_email(email_list= email_list,
                            message_body= f"Low price alert! Only {cheapest_flight.price} Rupees to fly "
                            f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                            f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."

        )

