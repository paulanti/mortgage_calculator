from datetime import datetime
import sys
import os


class DifferentPayments:
    def __init__(self, amount, term, rate, date):
        self.amount = amount
        self.term = term
        self.rate = rate
        self.date = date
        self.balance = amount
        self.payment_n = 0
        self.total_interest = 0
        self.total_payment = 0
        self.total_principal = 0


    def amount(self):
        return self.amount


    def term(self):
        return self.term


    def rate(self):
        return self.rate


    def date(self):
        return self.date


    def principal(self):
        self.monthly_principal = self.amount / self.term
        return self.monthly_principal


    def payment_date(self):
        self.payment_date_prev = datetime.strptime(self.date, "%d.%m.%Y")
        if self.payment_date_prev.month < 12:
            self.payment_date_current = self.payment_date_prev.replace(month=self.payment_date_prev.month + 1)
        else:
            self.payment_date_current = self.payment_date_prev.replace(month=1, year=self.payment_date_prev.year + 1)
        self.date = self.payment_date_current.strftime("%d.%m.%Y")
        return self.date


    def days_in_month(self):
        days = self.payment_date_current - self.payment_date_prev
        self.days_month = int(str(days)[:2])
        return self.days_month


    def days_in_year(self):
        date = self.payment_date_prev
        days_in_year = datetime(date.year+1, 1, 1) - datetime(date.year, 1, 1)
        self.days_year = int(str(days_in_year)[:3])
        return self.days_year


    def interest(self):
        self.monthly_interest = ((self.balance * self.rate / 100) / self.days_in_year()) * self.days_in_month()
        return self.monthly_interest


    def cur_balance(self):
        self.balance -= self.principal()
        return self.balance


    def payment(self):
        self.monthly_payment = self.interest() + self.principal()
        return self.monthly_payment


    def number_of_payment(self):
        self.payment_n += 1
        return self.payment_n


    def get_total_interest(self):
        self.total_interest += self.monthly_interest
        return self.total_interest


    def get_total_payment(self):
        self.total_payment += self.monthly_payment
        return self.total_payment


    def get_total_principal(self):
        self.total_principal += self.monthly_principal
        return self.total_principal


    def __str__(self):
        return ("{0:<4} {1:<12} {4:<10.2f} {3:<10.2f} {2:<10.2f} {5:<12.2f}".format
               (self.number_of_payment(), self.payment_date(), self.payment(), 
                self.interest(), self.principal(), self.cur_balance(),
                self.get_total_interest(), self.get_total_payment(), self.get_total_principal()))


class AnnuityPayments(DifferentPayments):
    def payment(self):
        self.monthly_payment = (self.amount * (self.rate / 1200))/(1 - ((1 + (self.rate / 1200))**-self.term))
        if (self.payment_n == self.term) and self.balance != 0:
            self.monthly_payment += (self.interest() + self.balance - self.monthly_payment)
        return self.monthly_payment


    def principal(self):
        self.monthly_principal = self.payment() - self.interest()
        return self.monthly_principal


def mortgage_shedule(calculator):
    columns = ("{0:<4} {1:<12} {2:^10} {3:^10} {4:^10} {5:^10}\n".format
              ("N", "Date", "Principal", "Interest", "Payment", "Balance"))
    columns2 = ("{0:+<4} {0:+<12} {0:+<10} {0:+<10} {0:+<10} {0:+<10}\n".format("+"))
    values = ""
    for i in range(calculator.term):
        values += ("{0}\n".format(calculator))
    total = ("\nTotal: {0:-<10} {1:<10.2f} {2:<10.2f} {3:<10.2f} {0:-<10}".format
            ("-", calculator.total_principal, calculator.total_interest, calculator.total_payment))
    return columns, columns2, values, total


def main():
    arguments = True
    while arguments is True:
        try:
            amount = int(input("Enter amount: "))
            arguments = False
        except ValueError:
            print("Amount must be integer.")
    while arguments is False:
        try:
            term = int(input("Enter term in months: "))
            arguments = True
        except ValueError:
            print("Term must be integer.")
    while arguments is True:
        try:
            rate = float(input("Enter rate: "))
            arguments = False
        except ValueError:
            print("Rate must be integer or float.")
    while arguments is False:
        try:
            date = input("Enter date in format 'DD.MM.YYYY': ")
            assert len(date) == 10, "Format of date isn't DD.MM.YYYY"
            arguments = True
        except ValueError:
            print("Format of date must be DD.MM.YYYY")
    while arguments is True:
        calculator_type = input("1 - Annuity payments\n2 - Different payments\n")
        if calculator_type == "1":
            m = AnnuityPayments(amount, term, rate, date)
            columns, columns2, values, total = mortgage_shedule(m)
            print(columns, columns2, values, total, sep="")
            arguments = False
        elif calculator_type == "2":
            m = DifferentPayments(amount, term, rate, date)
            columns, columns2, values, total = mortgage_shedule(m)
            print(columns, columns2, values, total, sep="")
            arguments = False
        else:
            print("Enter 1 or 2\n")
    while arguments is False:
        save_txt = input("Save to txt? Input y or n: ")
        if save_txt == "y":
            export_txt(columns, columns2, values)
            arguments = True
        elif save_txt == "n":
            pass
            arguments = True
        else:
            print("Enter y or n\n")


def export_txt(columns, columns2, values, total):
    fh = None
    try:
        fh = open("mortgage_calculator.txt", "w")
        fh.write(columns)
        fh.write(columns2)
        fh.write(values)
        return True
    except EnvironmentError as err:
        print("{0}: export error: {1}".format(os.path.basename(sys.argv[0]), err))
    finally:
        if fh is not None:
            fh.close()

if __name__ == "__main__":
    main()