# This program calculates mortgage payments depending on four inputs
# by the user: Principal, payment term, annual interest rate, and if anniversary
# payments are to be made.
# Written by David Liu

# --- Constants ---
MIN_PRINCIPAL = 1000.0
MAX_PRINCIPAL = 500000.0
MIN_TERM_YEARS = 1
MAX_TERM_YEARS = 30
MIN_INTEREST_RATE = 1.0
MAX_INTEREST_RATE = 10.0
MONTHS_IN_YEAR = 12
ANNIVERSARY_PAYMENT_RATE = 0.05
MAX_ANNIVERSARY_PAYMENT = 5000.0

def get_principal():
    """Get the principal amount from the user, with input validation."""
    while True:
        try:
            principal = float(input(f"Enter principal amount in $ ({MIN_PRINCIPAL:,.0f}-{MAX_PRINCIPAL:,.0f}): "))
            if MIN_PRINCIPAL <= principal <= MAX_PRINCIPAL:
                return principal
            else:
                print(f"Please enter a principal amount between ${MIN_PRINCIPAL:,.0f} and ${MAX_PRINCIPAL:,.0f}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_payment_term():
    """Get the payment term from the user, with input validation."""
    while True:
        try:
            payment_term = int(input(f"Enter payment term in years ({MIN_TERM_YEARS}-{MAX_TERM_YEARS}): "))
            if MIN_TERM_YEARS <= payment_term <= MAX_TERM_YEARS:
                return payment_term
            else:
                print(f"Please enter a payment term between {MIN_TERM_YEARS} and {MAX_TERM_YEARS} years.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def get_annual_interest_rate():
    """Get the annual interest rate from the user, with input validation."""
    while True:
        try:
            annual_interest_rate = float(input(f"Enter annual interest rate as % ({MIN_INTEREST_RATE}-{MAX_INTEREST_RATE}): "))
            if MIN_INTEREST_RATE <= annual_interest_rate <= MAX_INTEREST_RATE:
                return annual_interest_rate
            else:
                print(f"Please enter an annual interest rate between {MIN_INTEREST_RATE}% and {MAX_INTEREST_RATE}%.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_anniversary_payment_choice():
    """Get the user's choice for anniversary payments, with input validation."""
    while True:
        choice = input("Enter 'y' to make anniversary payments, 'n' otherwise: ").lower()
        if choice in ['y', 'n']:
            return choice
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def calculate_monthly_payment(principal, annual_interest_rate, payment_term):
    """Calculate the monthly mortgage payment."""
    term_in_months = MONTHS_IN_YEAR * payment_term
    monthly_interest_rate = annual_interest_rate / (MONTHS_IN_YEAR * 100)
    if monthly_interest_rate == 0:
        return principal / term_in_months
    monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_in_months)
    return monthly_payment

def run_amortization_schedule(principal, annual_interest_rate, payment_term, monthly_payment, anniversary_payment_choice):
    """
    Calculates and prints the amortization schedule.
    Returns a dictionary with summary values.
    """
    term_in_months = MONTHS_IN_YEAR * payment_term
    monthly_interest_rate = annual_interest_rate / (MONTHS_IN_YEAR * 100)

    remaining_principal = principal
    total_interest_paid = 0
    total_anniversary_payment = 0
    total_monthly_payments = 0
    num_months = 0

    print("\nMonth\tPrincipal")

    while remaining_principal > 0:
        num_months += 1
        monthly_interest_payment = remaining_principal * monthly_interest_rate

        current_monthly_payment = monthly_payment
        if current_monthly_payment >= remaining_principal + monthly_interest_payment:
            current_monthly_payment = remaining_principal + monthly_interest_payment

        paid_against_principal = current_monthly_payment - monthly_interest_payment
        remaining_principal -= paid_against_principal
        total_interest_paid += monthly_interest_payment
        total_monthly_payments += current_monthly_payment

        if remaining_principal < 0.01:
            remaining_principal = 0

        print(f"{num_months}\t${remaining_principal:,.2f}")

        if anniversary_payment_choice.lower() == 'y' and num_months % MONTHS_IN_YEAR == 0 and remaining_principal > 0:
            anniversary_payment = min(ANNIVERSARY_PAYMENT_RATE * principal, MAX_ANNIVERSARY_PAYMENT)

            if anniversary_payment > remaining_principal:
                anniversary_payment = remaining_principal

            remaining_principal -= anniversary_payment
            total_anniversary_payment += anniversary_payment
            print(f"Anniversary payment made: ${anniversary_payment:,.2f}. Remaining principal is: ${remaining_principal:,.2f}")

            if remaining_principal < 0.01:
                remaining_principal = 0

    summary = {
        "num_months": num_months,
        "total_interest_paid": total_interest_paid,
        "total_anniversary_payment": total_anniversary_payment,
        "total_monthly_payments": total_monthly_payments,
        "months_saved": term_in_months - num_months
    }
    return summary

def print_summary(summary, principal, anniversary_payment_choice):
    """Prints the final mortgage summary."""
    total_cost = principal + summary['total_interest_paid']

    print(f"\n--- Mortgage Summary ---")
    print(f"Total Monthly Payments: ${summary['total_monthly_payments']:,.2f}")
    print(f"Total Interest Paid: ${summary['total_interest_paid']:,.2f}")

    if anniversary_payment_choice.lower() == 'y':
        print(f"Total Anniversary Payments: ${summary['total_anniversary_payment']:,.2f}")
        print(f"Paid mortgage off {summary['months_saved']} months early.")
        total_cost += summary['total_anniversary_payment']

    print(f"Total Cost of Mortgage: ${total_cost:,.2f}")


def main():
    """Gets user input, calculates mortgage, and prints summary."""
    principal = get_principal()
    payment_term = get_payment_term()
    annual_interest_rate = get_annual_interest_rate()
    anniversary_payment = get_anniversary_payment_choice()

    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, payment_term)
    print(f"\nMonthly payment is: ${monthly_payment:,.2f}")

    summary = run_amortization_schedule(
        principal, annual_interest_rate, payment_term, monthly_payment, anniversary_payment
    )

    print_summary(summary, principal, anniversary_payment)


if __name__ == "__main__":
    main()
