# Hotel Analytics System — ER Diagram

## Entities

- Hotels
- Rooms
- Customers
- Bookings
- Payments
- Reviews
- Services
- Booking Services

## Relationships

- One hotel has many rooms.
- One customer can have many bookings.
- One room can have many bookings over time.
- One booking can have multiple payments.
- One booking can have zero or one review.
- One booking can contain multiple services.
- One service can belong to many bookings.
- `booking_services` resolves the many-to-many relationship between bookings and services.

## Relationship Summary

| Parent | Child | Relationship |
|---|---|---|
| Hotels | Rooms | 1:N |
| Customers | Bookings | 1:N |
| Rooms | Bookings | 1:N |
| Bookings | Payments | 1:N |
| Bookings | Reviews | 1:0..1 |
| Bookings | Booking Services | 1:N |
| Services | Booking Services | 1:N |
