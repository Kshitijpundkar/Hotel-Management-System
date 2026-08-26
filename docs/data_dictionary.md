# Hotel Analytics System — Data Dictionary

## 1. Hotels

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| hotel_id | INT | PK | No | Unique identifier for each hotel |
| hotel_name | VARCHAR(100) | - | No | Name of the hotel |
| city | VARCHAR(100) | - | No | City where the hotel is located |
| state | VARCHAR(100) | - | No | State where the hotel is located |
| address | VARCHAR(255) | - | Yes | Hotel address |
| phone | VARCHAR(20) | - | Yes | Hotel contact number |
| email | VARCHAR(100) | - | Yes | Hotel email address |
| star_rating | DECIMAL(2,1) | - | Yes | Hotel rating from 1.0 to 5.0 |

---

## 2. Rooms

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| room_id | INT | PK | No | Unique identifier for each room |
| hotel_id | INT | FK | No | References the hotel containing the room |
| room_number | VARCHAR(20) | - | No | Hotel room number |
| room_type | VARCHAR(50) | - | No | Type of room |
| price_per_night | DECIMAL(10,2) | - | No | Standard price per night |
| status | VARCHAR(20) | - | No | Current room status |

---

## 3. Customers

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| customer_id | INT | PK | No | Unique customer identifier |
| full_name | VARCHAR(100) | - | No | Customer's full name |
| email | VARCHAR(100) | UNIQUE | Yes | Customer email |
| phone | VARCHAR(20) | - | Yes | Customer phone number |
| city | VARCHAR(100) | - | Yes | Customer's city |
| registration_date | DATE | - | Yes | Date customer registered |

---

## 4. Bookings

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| booking_id | INT | PK | No | Unique booking identifier |
| customer_id | INT | FK | No | Customer who made the booking |
| room_id | INT | FK | No | Room associated with the booking |
| booking_date | DATE | - | No | Date the booking was created |
| check_in | DATE | - | No | Customer check-in date |
| check_out | DATE | - | No | Customer check-out date |
| number_of_guests | INT | - | No | Number of guests |
| booking_status | VARCHAR(30) | - | No | Current booking status |

---

## 5. Payments

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| payment_id | INT | PK | No | Unique payment identifier |
| booking_id | INT | FK | No | Booking associated with the payment |
| amount | DECIMAL(10,2) | - | No | Amount paid |
| payment_date | DATETIME | - | No | Date and time of payment |
| payment_method | VARCHAR(30) | - | No | Payment method |
| payment_status | VARCHAR(30) | - | No | Payment status |

---

## 6. Reviews

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| review_id | INT | PK | No | Unique review identifier |
| booking_id | INT | FK | No | Booking associated with the review |
| rating | INT | - | No | Customer rating from 1 to 5 |
| review_text | TEXT | - | Yes | Customer review |
| review_date | DATE | - | Yes | Date of review |

---

## 7. Services

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| service_id | INT | PK | No | Unique service identifier |
| service_name | VARCHAR(100) | - | No | Name of the hotel service |
| service_category | VARCHAR(50) | - | No | Category of service |
| price | DECIMAL(10,2) | - | No | Service price |

---

## 8. Booking Services

| Column | Data Type | Key | Nullable | Description |
|---|---|---|---|---|
| booking_service_id | INT | PK | No | Unique booking-service identifier |
| booking_id | INT | FK | No | Related booking |
| service_id | INT | FK | No | Related service |
| quantity | INT | No | No | Number of services purchased |
| service_amount | DECIMAL(10,2) | - | No | Total amount for the service |

---

# Key Relationships

- One hotel can have many rooms.
- One customer can have many bookings.
- One room can be associated with many bookings over time.
- One booking can have one or more payments.
- One booking can have a review.
- One booking can contain multiple services.
- One service can be used by many bookings.

# Analytical Purpose

The data model supports analysis of:

- Revenue
- Occupancy
- ADR
- RevPAR
- Booking trends
- Cancellation rate
- Customer behavior
- Customer lifetime value
- Room performance
- Hotel performance
- Service revenue
- Customer satisfaction
- Seasonal demand