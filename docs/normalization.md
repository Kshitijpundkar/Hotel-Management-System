# Database Normalization

## Objective

The Hotel Analytics System uses a normalized relational model for its transactional database.

## First Normal Form (1NF)

The database contains atomic values and avoids repeating groups.

Example:
Hotel services are not stored as comma-separated values in the bookings table. A separate `booking_services` table is used.

## Second Normal Form (2NF)

Non-key attributes depend on the complete key.

Service-specific attributes such as service name, category, and standard price are stored in the `services` table rather than `booking_services`.

## Third Normal Form (3NF)

Non-key attributes depend on the primary key and do not contain unnecessary transitive dependencies.

Hotel attributes are stored in the `hotels` table, customer attributes in `customers`, room attributes in `rooms`, and service attributes in `services`.

## Transactional Database

The MySQL database is designed using normalized relational principles to reduce redundancy and maintain data integrity.

## Analytical Database

For Power BI analytics, a dimensional/star-schema model may be created later to simplify reporting and improve analytical performance.s