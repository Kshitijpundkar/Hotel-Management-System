"""
Hotel Analytics System
Data Quality Validation

Purpose:
    Validate generated CSV datasets before loading them into MySQL.

Pipeline:
    CSV -> Data Quality Checks -> MySQL -> SQL -> Power BI
"""

from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path(__file__).parent / "data"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load all generated datasets."""

    hotels = pd.read_csv(DATA_DIR / "hotels.csv")
    rooms = pd.read_csv(DATA_DIR / "rooms.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    services = pd.read_csv(DATA_DIR / "services.csv")
    bookings = pd.read_csv(DATA_DIR / "bookings.csv")

    return (
        hotels,
        rooms,
        customers,
        services,
        bookings,
    )


# ============================================================
# BASIC DATASET CHECK
# ============================================================

def check_dataset_size(name, df):
    """Check whether a dataset contains records."""

    print(f"\n{name}")
    print("-" * 50)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    if len(df) == 0:
        print("❌ FAIL: Dataset is empty")
        return False

    print("✅ PASS: Dataset contains records")
    return True


# ============================================================
# NULL VALUE CHECK
# ============================================================

def check_null_values(name, df):
    """Check for missing values."""

    null_counts = df.isnull().sum()

    total_nulls = null_counts.sum()

    print(f"\n{name} - NULL CHECK")
    print("-" * 50)

    if total_nulls == 0:
        print("✅ PASS: No missing values")
        return True

    print("❌ FAIL: Missing values found")

    print(
        null_counts[
            null_counts > 0
        ]
    )

    return False


# ============================================================
# DUPLICATE PRIMARY KEY CHECK
# ============================================================

def check_primary_key(
    name,
    df,
    primary_key,
):
    """Check primary-key uniqueness."""

    duplicate_count = (
        df[primary_key]
        .duplicated()
        .sum()
    )

    print(f"\n{name} - PRIMARY KEY CHECK")
    print("-" * 50)

    print(
        f"Primary key: {primary_key}"
    )

    print(
        f"Duplicate records: {duplicate_count}"
    )

    if duplicate_count == 0:
        print("✅ PASS: Primary key is unique")
        return True

    print("❌ FAIL: Duplicate primary keys found")
    return False


# ============================================================
# FOREIGN KEY CHECK
# ============================================================

def check_foreign_key(
    child_name,
    child_df,
    child_column,
    parent_name,
    parent_df,
    parent_column,
):
    """Check referential integrity."""

    child_values = set(
        child_df[child_column].dropna()
    )

    parent_values = set(
        parent_df[parent_column].dropna()
    )

    invalid_values = (
        child_values - parent_values
    )

    print(
        f"\n{child_name} -> {parent_name}"
    )

    print("-" * 50)

    print(
        f"Relationship: "
        f"{child_column} -> {parent_column}"
    )

    print(
        f"Invalid values: {len(invalid_values)}"
    )

    if len(invalid_values) == 0:
        print("✅ PASS: Foreign key is valid")
        return True

    print("❌ FAIL: Invalid foreign keys found")

    return False


# ============================================================
# BOOKING DATE CHECK
# ============================================================

def check_booking_dates(bookings):
    """Validate booking date relationships."""

    bookings = bookings.copy()

    bookings["booking_date"] = pd.to_datetime(
        bookings["booking_date"]
    )

    bookings["check_in"] = pd.to_datetime(
        bookings["check_in"]
    )

    bookings["check_out"] = pd.to_datetime(
        bookings["check_out"]
    )

    invalid_booking_dates = (
        bookings["check_in"]
        < bookings["booking_date"]
    ).sum()

    invalid_checkout_dates = (
        bookings["check_out"]
        <= bookings["check_in"]
    ).sum()

    print("\nBOOKING DATE VALIDATION")
    print("-" * 50)

    print(
        f"Check-in before booking date: "
        f"{invalid_booking_dates}"
    )

    print(
        f"Check-out before/equal check-in: "
        f"{invalid_checkout_dates}"
    )

    if (
        invalid_booking_dates == 0
        and invalid_checkout_dates == 0
    ):
        print("✅ PASS: Booking dates are valid")
        return True

    print("❌ FAIL: Invalid booking dates found")
    return False


# ============================================================
# STAY DURATION CHECK
# ============================================================

def check_stay_duration(bookings):
    """Check stay duration calculation."""

    bookings = bookings.copy()

    bookings["check_in"] = pd.to_datetime(
        bookings["check_in"]
    )

    bookings["check_out"] = pd.to_datetime(
        bookings["check_out"]
    )

    calculated_duration = (
        bookings["check_out"]
        - bookings["check_in"]
    ).dt.days

    invalid_duration = (
        calculated_duration
        != bookings["stay_duration"]
    ).sum()

    print("\nSTAY DURATION VALIDATION")
    print("-" * 50)

    print(
        f"Incorrect stay durations: "
        f"{invalid_duration}"
    )

    if invalid_duration == 0:
        print("✅ PASS: Stay duration is correct")
        return True

    print("❌ FAIL: Stay duration mismatch")
    return False


# ============================================================
# REVENUE CHECK
# ============================================================

def check_revenue(bookings):
    """Validate booking revenue calculations."""

    bookings = bookings.copy()

    expected_gross = (
        bookings["room_price_per_night"]
        * bookings["stay_duration"]
    )

    expected_discount = (
        expected_gross
        * bookings["discount_rate"]
    )

    expected_net = (
        expected_gross
        - expected_discount
    )

    expected_tax = (
        expected_net
        * 0.12
    )

    expected_total = (
        expected_net
        + expected_tax
    )

    revenue_difference = (
        expected_total
        - bookings["total_amount"]
    ).abs()

    invalid_revenue = (
        revenue_difference > 0.01
    ).sum()

    print("\nREVENUE VALIDATION")
    print("-" * 50)

    print(
        f"Incorrect revenue records: "
        f"{invalid_revenue}"
    )

    if invalid_revenue == 0:
        print("✅ PASS: Revenue calculations are correct")
        return True

    print("❌ FAIL: Revenue calculation errors found")
    return False


# ============================================================
# STATUS / REALIZED REVENUE CHECK
# ============================================================

def check_realized_revenue(bookings):
    """
    Validate realized revenue.

    Cancelled and no-show bookings should have
    zero realized revenue.
    """

    cancelled_invalid = bookings[
        bookings["booking_status"].isin(
            ["Cancelled", "No-show"]
        )
        & (
            bookings["realized_revenue"] != 0
        )
    ]

    completed_invalid = bookings[
        ~bookings["booking_status"].isin(
            ["Cancelled", "No-show"]
        )
        & (
            bookings["realized_revenue"]
            != bookings["total_amount"]
        )
    ]

    invalid_count = (
        len(cancelled_invalid)
        + len(completed_invalid)
    )

    print("\nREALIZED REVENUE VALIDATION")
    print("-" * 50)

    print(
        f"Invalid realized revenue records: "
        f"{invalid_count}"
    )

    if invalid_count == 0:
        print(
            "✅ PASS: Realized revenue logic is correct"
        )
        return True

    print(
        "❌ FAIL: Realized revenue logic has errors"
    )

    return False


# ============================================================
# NEGATIVE VALUE CHECK
# ============================================================

def check_negative_values(bookings):
    """Check for negative financial values."""

    columns = [
        "room_price_per_night",
        "discount_amount",
        "tax_amount",
        "total_amount",
        "realized_revenue",
    ]

    invalid_count = 0

    for column in columns:

        count = (
            bookings[column] < 0
        ).sum()

        invalid_count += count

    print("\nNEGATIVE VALUE CHECK")
    print("-" * 50)

    print(
        f"Negative financial records: "
        f"{invalid_count}"
    )

    if invalid_count == 0:
        print("✅ PASS: No negative financial values")
        return True

    print("❌ FAIL: Negative financial values found")
    return False


# ============================================================
# MAIN QUALITY CHECK
# ============================================================

def main():
    """Run complete data-quality validation."""

    print("=" * 60)
    print("HOTEL ANALYTICS SYSTEM")
    print("DATA QUALITY VALIDATION")
    print("=" * 60)

    (
        hotels,
        rooms,
        customers,
        services,
        bookings,
    ) = load_data()

    results = []

    # --------------------------------------------------------
    # Dataset checks
    # --------------------------------------------------------

    results.append(
        check_dataset_size(
            "HOTELS",
            hotels,
        )
    )

    results.append(
        check_dataset_size(
            "ROOMS",
            rooms,
        )
    )

    results.append(
        check_dataset_size(
            "CUSTOMERS",
            customers,
        )
    )

    results.append(
        check_dataset_size(
            "SERVICES",
            services,
        )
    )

    results.append(
        check_dataset_size(
            "BOOKINGS",
            bookings,
        )
    )

    # --------------------------------------------------------
    # NULL checks
    # --------------------------------------------------------

    results.append(
        check_null_values(
            "HOTELS",
            hotels,
        )
    )

    results.append(
        check_null_values(
            "ROOMS",
            rooms,
        )
    )

    results.append(
        check_null_values(
            "CUSTOMERS",
            customers,
        )
    )

    results.append(
        check_null_values(
            "SERVICES",
            services,
        )
    )

    results.append(
        check_null_values(
            "BOOKINGS",
            bookings,
        )
    )

    # --------------------------------------------------------
    # Primary key checks
    # --------------------------------------------------------

    results.append(
        check_primary_key(
            "HOTELS",
            hotels,
            "hotel_id",
        )
    )

    results.append(
        check_primary_key(
            "ROOMS",
            rooms,
            "room_id",
        )
    )

    results.append(
        check_primary_key(
            "CUSTOMERS",
            customers,
            "customer_id",
        )
    )

    results.append(
        check_primary_key(
            "SERVICES",
            services,
            "service_id",
        )
    )

    results.append(
        check_primary_key(
            "BOOKINGS",
            bookings,
            "booking_id",
        )
    )

    # --------------------------------------------------------
    # Foreign key checks
    # --------------------------------------------------------

    results.append(
        check_foreign_key(
            "ROOMS",
            rooms,
            "hotel_id",
            "HOTELS",
            hotels,
            "hotel_id",
        )
    )

    results.append(
        check_foreign_key(
            "BOOKINGS",
            bookings,
            "customer_id",
            "CUSTOMERS",
            customers,
            "customer_id",
        )
    )

    results.append(
        check_foreign_key(
            "BOOKINGS",
            bookings,
            "room_id",
            "ROOMS",
            rooms,
            "room_id",
        )
    )

    results.append(
        check_foreign_key(
            "BOOKINGS",
            bookings,
            "hotel_id",
            "HOTELS",
            hotels,
            "hotel_id",
        )
    )

    # --------------------------------------------------------
    # Business logic checks
    # --------------------------------------------------------

    results.append(
        check_booking_dates(
            bookings
        )
    )

    results.append(
        check_stay_duration(
            bookings
        )
    )

    results.append(
        check_revenue(
            bookings
        )
    )

    results.append(
        check_realized_revenue(
            bookings
        )
    )

    results.append(
        check_negative_values(
            bookings
        )
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(
        f"Checks passed: {passed}/{total}"
    )

    if passed == total:
        print(
            "\n✅ ALL DATA QUALITY CHECKS PASSED"
        )
        print(
            "Dataset is ready for the MySQL loading stage."
        )

    else:
        print(
            "\n❌ SOME DATA QUALITY CHECKS FAILED"
        )
        print(
            "Fix the issues before loading data into MySQL."
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
    