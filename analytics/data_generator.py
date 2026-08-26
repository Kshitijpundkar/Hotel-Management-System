"""
Hotel Analytics System
Synthetic Data Generator

Purpose:
    Generate realistic synthetic hotel data for the analytics pipeline.

Pipeline:
    Python -> CSV -> Data Quality Checks -> MySQL -> SQL -> Power BI
"""

from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

NUM_HOTELS = 20
NUM_CUSTOMERS = 10000
NUM_BOOKINGS = 50000

OUTPUT_DIR = Path(__file__).parent / "data"

# Reproducibility
np.random.seed(SEED)
Faker.seed(SEED)

fake = Faker("en_IN")


# ============================================================
# HOTEL CONFIGURATION
# ============================================================

HOTEL_NAMES = [
    "Grand Palace",
    "Royal Orchid",
    "Taj Heritage",
    "The Residency",
    "Silver Oak",
    "Sunrise Grand",
    "Lake View",
    "The Imperial",
    "Green Park",
    "Blue Horizon",
    "Golden Tulip",
    "City Heights",
    "Palm Residency",
    "Royal Comfort",
    "The Fern",
    "Urban Retreat",
    "Regal Suites",
    "Crystal Palace",
    "Heritage Inn",
    "Skyline Grand",
]


CITIES = [
    "Mumbai",
    "Pune",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Goa",
    "Nagpur",
    "Nashik",
    "Indore",
    "Surat",
    "Amritsar",
    "Udaipur",
    "Lucknow",
    "Bhopal",
    "Chandigarh",
    "Kochi",
]


STATE_BY_CITY = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Goa": "Goa",
    "Nagpur": "Maharashtra",
    "Nashik": "Maharashtra",
    "Indore": "Madhya Pradesh",
    "Surat": "Gujarat",
    "Amritsar": "Punjab",
    "Udaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh",
    "Bhopal": "Madhya Pradesh",
    "Chandigarh": "Chandigarh",
    "Kochi": "Kerala",
}


# ============================================================
# ROOM CONFIGURATION
# ============================================================

ROOM_TYPES = [
    "Standard",
    "Deluxe",
    "Executive",
    "Suite",
]


ROOM_TYPE_MULTIPLIER = {
    "Standard": 1.00,
    "Deluxe": 1.35,
    "Executive": 1.75,
    "Suite": 2.50,
}


# ============================================================
# CUSTOMER CONFIGURATION
# ============================================================

CUSTOMER_CITIES = [
    "Mumbai",
    "Pune",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Nagpur",
    "Nashik",
    "Indore",
    "Surat",
    "Lucknow",
    "Bhopal",
    "Chandigarh",
    "Kochi",
]


# ============================================================
# SERVICE CONFIGURATION
# ============================================================

SERVICES = [
    ("Breakfast", "Food & Beverage", 450),
    ("Airport Transfer", "Transportation", 1200),
    ("Spa", "Wellness", 2500),
    ("Laundry", "Housekeeping", 500),
    ("Room Service", "Food & Beverage", 700),
    ("Gym", "Wellness", 800),
    ("Swimming Pool", "Recreation", 600),
    ("Restaurant", "Food & Beverage", 1200),
    ("Conference Hall", "Business", 5000),
    ("Parking", "Transportation", 300),
    ("Extra Bed", "Room Service", 1000),
    ("Breakfast Buffet", "Food & Beverage", 650),
    ("City Tour", "Transportation", 1800),
    ("Kids Activity", "Recreation", 400),
    ("Business Lounge", "Business", 1500),
]


# ============================================================
# BOOKING CONFIGURATION
# ============================================================

BOOKING_START_DATE = pd.Timestamp("2024-01-01")
BOOKING_END_DATE = pd.Timestamp("2026-06-30")


BOOKING_CHANNELS = [
    "Direct",
    "Website",
    "Booking.com",
    "MakeMyTrip",
    "Goibibo",
    "Expedia",
    "Corporate",
    "Walk-in",
]


BOOKING_CHANNEL_PROBABILITY = [
    0.15,
    0.20,
    0.18,
    0.15,
    0.10,
    0.07,
    0.10,
    0.05,
]


BOOKING_STATUSES = [
    "Confirmed",
    "Completed",
    "Cancelled",
    "No-show",
]


BOOKING_STATUS_PROBABILITY = [
    0.15,
    0.65,
    0.12,
    0.08,
]


# ============================================================
# GENERATE HOTELS
# ============================================================

def generate_hotels() -> pd.DataFrame:
    """Generate the hotel master dataset."""

    hotels = []

    for hotel_id in range(1, NUM_HOTELS + 1):

        city = CITIES[hotel_id - 1]
        state = STATE_BY_CITY[city]

        star_rating = np.random.choice(
            [2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            p=[0.05, 0.15, 0.20, 0.25, 0.20, 0.15],
        )

        hotel_name = HOTEL_NAMES[hotel_id - 1]

        hotels.append(
            {
                "hotel_id": hotel_id,
                "hotel_name": f"{hotel_name} {city}",
                "city": city,
                "country": "India",
                "state": state,
                "address": (
                    f"{fake.building_number()}, "
                    f"{fake.street_name()}, "
                    f"{city}"
                ),
                "phone_number": fake.phone_number(),
                "email": f"contact{hotel_id}@hotelanalytics.com",
                "star_rating": star_rating,
            }
        )

    return pd.DataFrame(hotels)


# ============================================================
# GENERATE ROOMS
# ============================================================

def generate_rooms(hotels: pd.DataFrame) -> pd.DataFrame:
    """
    Generate rooms for each hotel.

    Room pricing is influenced by:
    1. Hotel star rating
    2. Room type
    """

    rooms = []

    room_id = 1

    for _, hotel in hotels.iterrows():

        hotel_id = int(hotel["hotel_id"])
        star_rating = float(hotel["star_rating"])

        if star_rating >= 4.5:
            num_rooms = np.random.randint(28, 36)

        elif star_rating >= 4.0:
            num_rooms = np.random.randint(24, 32)

        elif star_rating >= 3.5:
            num_rooms = np.random.randint(22, 30)

        else:
            num_rooms = np.random.randint(18, 26)

        for room_number in range(1, num_rooms + 1):

            room_type = np.random.choice(
                ROOM_TYPES,
                p=[0.45, 0.30, 0.15, 0.10],
            )

            base_price = 1000 + (star_rating * 900)

            price = (
                base_price
                * ROOM_TYPE_MULTIPLIER[room_type]
            )

            price *= np.random.uniform(0.90, 1.10)

            price = round(price, 2)

            status = np.random.choice(
                ["Available", "Maintenance", "Inactive"],
                p=[0.94, 0.04, 0.02],
            )

            rooms.append(
                {
                    "room_id": room_id,
                    "hotel_id": hotel_id,
                    "room_number": f"{room_number:03d}",
                    "room_type": room_type,
                    "price_per_night": price,
                    "status": status,
                }
            )

            room_id += 1

    return pd.DataFrame(rooms)


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers() -> pd.DataFrame:
    """Generate synthetic customer master data."""

    customers = []

    registration_start = pd.Timestamp("2023-01-01")
    registration_end = pd.Timestamp("2026-06-30")

    registration_dates = pd.date_range(
        start=registration_start,
        end=registration_end,
        freq="D",
    )

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        registration_date = np.random.choice(
            registration_dates
        )

        city = np.random.choice(
            CUSTOMER_CITIES
        )

        phone = (
            f"{np.random.randint(6, 10)}"
            f"{np.random.randint(100000000, 1000000000)}"
        )

        customers.append(
            {
                "customer_id": customer_id,
                "full_name": fake.name(),
                "email": f"customer{customer_id}@example.com",
                "phone": phone,
                "city": city,
                "registration_date": pd.Timestamp(
                    registration_date
                ).date(),
            }
        )

    return pd.DataFrame(customers)


# ============================================================
# GENERATE SERVICES
# ============================================================

def generate_services() -> pd.DataFrame:
    """Generate hotel service master data."""

    services = []

    for service_id, (name, category, price) in enumerate(
        SERVICES,
        start=1,
    ):

        services.append(
            {
                "service_id": service_id,
                "service_name": name,
                "service_category": category,
                "price": price,
            }
        )

    return pd.DataFrame(services)


# ============================================================
# GENERATE BOOKINGS
# ============================================================

def generate_bookings(
    customers: pd.DataFrame,
    rooms: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate realistic hotel booking transactions.

    Relationships:

        customer_id -> customers.customer_id
        room_id     -> rooms.room_id
        hotel_id    -> hotels.hotel_id
    """

    bookings = []

    customer_ids = customers["customer_id"].to_numpy()

    room_ids = rooms["room_id"].to_numpy()

    room_lookup = rooms.set_index("room_id")

    booking_dates = pd.date_range(
        start=BOOKING_START_DATE,
        end=BOOKING_END_DATE,
        freq="D",
    )

    for booking_id in range(1, NUM_BOOKINGS + 1):

        # ----------------------------------------------------
        # Customer
        # ----------------------------------------------------

        customer_id = int(
            np.random.choice(customer_ids)
        )

        # ----------------------------------------------------
        # Booking date
        # ----------------------------------------------------

        booking_date = pd.Timestamp(
            np.random.choice(booking_dates)
        )

        # ----------------------------------------------------
        # Booking lead time
        # ----------------------------------------------------

        booking_lead_days = int(
            np.random.choice(
                [
                    1,
                    2,
                    3,
                    5,
                    7,
                    10,
                    14,
                    21,
                    30,
                    45,
                    60,
                ],
                p=[
                    0.12,
                    0.12,
                    0.12,
                    0.12,
                    0.12,
                    0.10,
                    0.08,
                    0.07,
                    0.06,
                    0.05,
                    0.04,
                ],
            )
        )

        check_in = (
            booking_date
            + pd.Timedelta(days=booking_lead_days)
        )

        # ----------------------------------------------------
        # Stay duration
        # ----------------------------------------------------

        stay_duration = int(
            np.random.choice(
                [1, 2, 3, 4, 5, 6, 7],
                p=[
                    0.25,
                    0.25,
                    0.20,
                    0.12,
                    0.08,
                    0.06,
                    0.04,
                ],
            )
        )

        check_out = (
            check_in
            + pd.Timedelta(days=stay_duration)
        )

        # ----------------------------------------------------
        # Room
        # ----------------------------------------------------

        room_id = int(
            np.random.choice(room_ids)
        )

        room = room_lookup.loc[room_id]

        hotel_id = int(
            room["hotel_id"]
        )

        room_type = room["room_type"]

        room_price = float(
            room["price_per_night"]
        )

        # ----------------------------------------------------
        # Guests
        # ----------------------------------------------------

        adults = int(
            np.random.choice(
                [1, 2, 3, 4],
                p=[
                    0.15,
                    0.50,
                    0.25,
                    0.10,
                ],
            )
        )

        children = int(
            np.random.choice(
                [0, 1, 2],
                p=[
                    0.70,
                    0.20,
                    0.10,
                ],
            )
        )

        # ----------------------------------------------------
        # Booking channel
        # ----------------------------------------------------

        booking_channel = np.random.choice(
            BOOKING_CHANNELS,
            p=BOOKING_CHANNEL_PROBABILITY,
        )

        # ----------------------------------------------------
        # Booking status
        # ----------------------------------------------------

        booking_status = np.random.choice(
            BOOKING_STATUSES,
            p=BOOKING_STATUS_PROBABILITY,
        )

        # ----------------------------------------------------
        # Discount
        # ----------------------------------------------------

        discount_rate = float(
            np.random.choice(
                [
                    0.00,
                    0.05,
                    0.10,
                    0.15,
                    0.20,
                ],
                p=[
                    0.45,
                    0.25,
                    0.18,
                    0.08,
                    0.04,
                ],
            )
        )

        # ----------------------------------------------------
        # Revenue calculation
        # ----------------------------------------------------

        gross_room_revenue = (
            room_price
            * stay_duration
        )

        discount_amount = (
            gross_room_revenue
            * discount_rate
        )

        net_room_revenue = (
            gross_room_revenue
            - discount_amount
        )

        # ----------------------------------------------------
        # Tax
        # ----------------------------------------------------

        tax_rate = 0.12

        tax_amount = (
            net_room_revenue
            * tax_rate
        )

        total_amount = (
            net_room_revenue
            + tax_amount
        )

        # ----------------------------------------------------
        # Realized revenue
        # ----------------------------------------------------

        if booking_status in [
            "Cancelled",
            "No-show",
        ]:
            realized_revenue = 0.0

        else:
            realized_revenue = total_amount

        # ----------------------------------------------------
        # Store booking
        # ----------------------------------------------------

        bookings.append(
            {
                "booking_id": booking_id,
                "customer_id": customer_id,
                "hotel_id": hotel_id,
                "room_id": room_id,
                "booking_date": booking_date.date(),
                "check_in": check_in.date(),
                "check_out": check_out.date(),
                "stay_duration": stay_duration,
                "adults": adults,
                "children": children,
                "booking_channel": booking_channel,
                "booking_status": booking_status,
                "room_type": room_type,
                "room_price_per_night": round(
                    room_price,
                    2,
                ),
                "discount_rate": discount_rate,
                "discount_amount": round(
                    discount_amount,
                    2,
                ),
                "tax_amount": round(
                    tax_amount,
                    2,
                ),
                "total_amount": round(
                    total_amount,
                    2,
                ),
                "realized_revenue": round(
                    realized_revenue,
                    2,
                ),
            }
        )

    return pd.DataFrame(bookings)


# ============================================================
# SAVE DATA
# ============================================================

def save_dataframe(
    df: pd.DataFrame,
    filename: str,
) -> None:
    """Save a DataFrame as a CSV file."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = OUTPUT_DIR / filename

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Created: {output_path}"
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def main() -> None:
    """Run the complete synthetic data generation pipeline."""

    print("=" * 60)
    print("HOTEL ANALYTICS SYSTEM - DATA GENERATOR")
    print("=" * 60)

    # ========================================================
    # 1. HOTELS
    # ========================================================

    hotels = generate_hotels()

    print(
        f"\nHotels generated: {len(hotels)}"
    )

    print("\nHotel sample:")
    print(hotels.head())

    save_dataframe(
        hotels,
        "hotels.csv",
    )

    # ========================================================
    # 2. ROOMS
    # ========================================================

    rooms = generate_rooms(
        hotels
    )

    print(
        f"\nRooms generated: {len(rooms)}"
    )

    print("\nRoom sample:")
    print(rooms.head())

    save_dataframe(
        rooms,
        "rooms.csv",
    )

    # ========================================================
    # 3. CUSTOMERS
    # ========================================================

    customers = generate_customers()

    print(
        f"\nCustomers generated: {len(customers)}"
    )

    print("\nCustomer sample:")
    print(customers.head())

    save_dataframe(
        customers,
        "customers.csv",
    )

    # ========================================================
    # 4. SERVICES
    # ========================================================

    services = generate_services()

    print(
        f"\nServices generated: {len(services)}"
    )

    print("\nService sample:")
    print(services.head())

    save_dataframe(
        services,
        "services.csv",
    )

    # ========================================================
    # 5. BOOKINGS
    # ========================================================

    bookings = generate_bookings(
        customers,
        rooms,
    )

    print(
        f"\nBookings generated: {len(bookings)}"
    )

    print("\nBooking sample:")
    print(bookings.head())

    save_dataframe(
        bookings,
        "bookings.csv",
    )

    # ========================================================
    # COMPLETION
    # ========================================================

    print("\n" + "=" * 60)
    print(
        "MASTER AND TRANSACTION DATA GENERATION COMPLETED"
    )
    print("=" * 60)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()