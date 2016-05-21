# This program calculates mortgage payments depending on four inputs
# by the user: Principal, payment term, annual interest rate, and if anniversary
# payments are to be made.
# Written by David Liu, CISC 101, Student # 10060216

def main():
    #Define each variable as an illegal input to start the loop.
    payment_term = 0
    principal = 0
    annual_interest_rate = 0

    #The while loops check for legal numeric input.
    while principal < 1000 or principal > 500000:
        principal = float(input("Enter principal amount in $: "))
    while payment_term < 1 or payment_term > 30:
        payment_term = int(input("Enter payment term in years: "))
    while annual_interest_rate < 1 or annual_interest_rate > 10:
        annual_interest_rate = float(input("Enter annual interest rate as %: "))
    anniversary_payment = input("Enter 'y' to make anniversary payments, 'n' otherwise: ")
    
    #Define variables used in mortgage calculator.
    term_in_months = 12 * payment_term
    monthly_interest_rate = annual_interest_rate / 1200
    monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_in_months)
    print("Monthly payment is: ${0:,.2f}".format(monthly_payment))
        
    print("Month\tPrincipal")
    #Define running totals for interest paid, monthly payments, anniversary payments, and number of months.
    total_interest_paid = 0
    total_monthly_payment = 0
    total_anniversary_payment = 0
    num_months = 0

    #While loop to control entire calculations. 
    remaining_principal = principal
    while remaining_principal >= 0:
        num_months = num_months + 1
        monthly_interest_payment = monthly_interest_rate * remaining_principal
        paid_against_principal = monthly_payment - monthly_interest_payment
        remaining_principal = remaining_principal - paid_against_principal
        if remaining_principal < 0:       
            print(num_months, "\t$0.00")
        else:
            print(num_months, "\t${0:,.2f}".format(remaining_principal))
        if anniversary_payment == 'y':
            if num_months % 12 == 0:
                if 0.05 * remaining_principal < 5000:
                    paid_anniversary = 0.05 * remaining_principal
                elif 0.05 * remaining_principal > 5000:
                    paid_anniversary = 5000
                total_anniversary_payment= total_anniversary_payment + paid_anniversary
                remaining_principal= remaining_principal - paid_anniversary
                print("Anniversary payment made: ${0:,.2f}.".format(paid_anniversary), "Remaining principal is: ${0:,.2f}".format(remaining_principal))
        total_interest_paid += monthly_interest_payment
        total_monthly_payment += monthly_payment
        total_mortgage = total_monthly_payment + total_anniversary_payment
        months_saved = term_in_months - num_months
    #Print outputs (different depending on if anniversary payments were selected).
    if anniversary_payment == 'y':        
        print("Total interest payments are: ${0:2,.2f}".format(total_interest_paid))
        print("Paid mortage off {0} months early.".format(months_saved))
        print("Total monthly payments are: ${0:2,.2f}".format(total_monthly_payment))
        print("Total anniversary payments are: ${0:,.2f}".format(total_anniversary_payment))
        print("Total cost of mortgage is: ${0:,.2f}".format(total_mortgage))   
    else:
        print("Total interest payments are: ${0:2,.2f}".format(total_interest_paid))
        print("Total monthly payments are: ${0:2,.2f}".format(total_monthly_payment))
        print("Total cost of mortgage is: ${0:,.2f}".format(total_mortgage))
main()


        
        
