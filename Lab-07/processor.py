def decode_promo_voucher(voucher_code):
    try:
        if not isinstance(voucher_code, str):
            return "Invalid voucher"
        code = voucher_code.strip()
        if '-' not in code:
            return "Invalid voucher format"
        parts = code.split('-')
        if len(parts) != 2:
            return "Invalid voucher format"
        prefix, pct_str = parts[0].strip(), parts[1].strip()
        if not prefix:
            return "Invalid voucher prefix"
        percentage = int(pct_str)
        if percentage < 0 or percentage > 100:
            return "Invalid percentage"
        return f"Valid {prefix.upper()}: {percentage}% OFF"
    except Exception:
        return "Invalid voucher"

def calculate_seat_tier_price(tier_spec):
    try:
        if not isinstance(tier_spec, str):
            return 0.0
        parts = tier_spec.split('@')
        if len(parts) != 2:
            return 0.0
        tier = parts[0].strip().upper()
        row = int(parts[1].strip())
        if row < 0:
            return 0.0
        tier_rates = {
            "VIP": 150.0,
            "PREMIUM": 90.0,
            "GENERAL": 45.0
        }
        if tier not in tier_rates:
            return 0.0
        base = tier_rates[tier]
        return base + (row * 2.0)
    except Exception:
        return 0.0

def parse_attendee_badge(badge_csv):
    try:
        if not isinstance(badge_csv, str):
            return "Invalid badge"
        tokens = badge_csv.split(',')
        if len(tokens) != 3:
            return "Invalid badge format"
        name = tokens[0].strip()
        if not name:
            return "Invalid name"
        age = int(tokens[1].strip())
        if age < 0 or age > 150:
            return "Invalid age"
        seat = tokens[2].strip()
        if not seat:
            return "Invalid seat"
        category = "Child" if age < 18 else "Adult"
        return f"{name} [{category}] - Seat {seat}"
    except Exception:
        return "Invalid badge"

def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price: $", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))

if __name__ == "__main__":
    main()