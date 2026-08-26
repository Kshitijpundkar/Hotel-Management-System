CREATE DATABASE IF NOT EXISTS hotel_analytics;
USE hotel_analytics;

-- ============================================================
-- 1. HOTELS
-- ============================================================

CREATE TABLE IF NOT EXISTS hotels (
    hotel_id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,  
    email VARCHAR(100) NOT NULL,
    star_rating DECIMAL(2,1),

        CONSTRAINT chk_hotel_star_rating
        CHECK (star_rating BETWEEN 1.0 AND 5.0)
);


-- ============================================================
-- 2. ROOMS
-- ============================================================

CREATE TABLE IF NOT EXISTS rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Available',

    CONSTRAINT fk_rooms_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotels(hotel_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_room_price
        CHECK (price_per_night >= 0),

    CONSTRAINT chk_room_status
        CHECK (status IN (
            'Available',
            'Maintenance',
            'Inactive'
        )),

    CONSTRAINT uq_hotel_room
        UNIQUE (hotel_id, room_number)
);


-- ============================================================
-- 3. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    registration_date DATE DEFAULT (CURRENT_DATE)
);


-- ============================================================
-- 4. BOOKINGS
-- ============================================================

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,
    room_id INT NOT NULL,

    booking_date DATE NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,

    number_of_guests INT NOT NULL DEFAULT 1,

    booking_channel VARCHAR(50) NOT NULL,

    booking_status VARCHAR(30) NOT NULL DEFAULT 'Confirmed',

    CONSTRAINT fk_bookings_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_bookings_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_booking_dates
        CHECK (check_out > check_in),

    CONSTRAINT chk_booking_guests
        CHECK (number_of_guests > 0),

    CONSTRAINT chk_booking_status
        CHECK (booking_status IN (
            'Confirmed',
            'Completed',
            'Cancelled',
            'No Show'
        ))
);


-- ============================================================
-- 5. PAYMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    amount DECIMAL(12,2) NOT NULL,

    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    payment_method VARCHAR(30) NOT NULL,

    payment_status VARCHAR(30) NOT NULL DEFAULT 'Completed',

    CONSTRAINT fk_payments_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0),

    CONSTRAINT chk_payment_status
        CHECK (payment_status IN (
            'Completed',
            'Pending',
            'Failed',
            'Refunded'
        ))
);


-- ============================================================
-- 6. REVIEWS
-- ============================================================

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    rating INT NOT NULL,

    review_text TEXT,

    review_date DATE DEFAULT (CURRENT_DATE),

    CONSTRAINT fk_reviews_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_review_rating
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT uq_booking_review
        UNIQUE (booking_id)
);


-- ============================================================
-- 7. SERVICES
-- ============================================================

CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,

    service_name VARCHAR(100) NOT NULL,

    service_category VARCHAR(50) NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    CONSTRAINT chk_service_price
        CHECK (price >= 0)
);


-- ============================================================
-- 8. BOOKING SERVICES
-- ============================================================

CREATE TABLE IF NOT EXISTS booking_services (
    booking_service_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    service_id INT NOT NULL,

    quantity INT NOT NULL DEFAULT 1,

    service_amount DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_booking_services_booking
        FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_booking_services_service
        FOREIGN KEY (service_id)
        REFERENCES services(service_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_service_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_service_amount
        CHECK (service_amount >= 0),

    CONSTRAINT uq_booking_service
        UNIQUE (booking_id, service_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_rooms_hotel_id
    ON rooms(hotel_id);

CREATE INDEX idx_bookings_customer_id
    ON bookings(customer_id);

CREATE INDEX idx_bookings_room_id
    ON bookings(room_id);

CREATE INDEX idx_bookings_booking_date
    ON bookings(booking_date);

CREATE INDEX idx_bookings_check_in
    ON bookings(check_in);

CREATE INDEX idx_bookings_check_out
    ON bookings(check_out);

CREATE INDEX idx_bookings_status
    ON bookings(booking_status);

CREATE INDEX idx_payments_booking_id
    ON payments(booking_id);

CREATE INDEX idx_payments_payment_date
    ON payments(payment_date);

CREATE INDEX idx_payments_status
    ON payments(payment_status);

CREATE INDEX idx_reviews_booking_id
    ON reviews(booking_id);

CREATE INDEX idx_booking_services_booking_id
    ON booking_services(booking_id);

CREATE INDEX idx_booking_services_service_id
    ON booking_services(service_id);


-- ============================================================
-- VERIFY TABLES
-- ============================================================

SHOW TABLES;