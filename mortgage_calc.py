from datetime import datetime
import sys
import os


class DifferentPayments:
    def __init__(self, amount, time, rate, date):
        self.amount = amount
        self.time = time
        self.rate = rate
        self.date = date
        self.base_amount_left = amount


    def amount(self):
        return self.amount


    def time(self):
        return self.time


    def rate(self):
        return self.rate


    def date(self):
        return self.date


    def payment(self):
        return self.amount / self.time


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


    def month_rates(self):
        self.month_percentage = ((self.base_amount_left * self.rate / 100) / self.days_in_year()) * self.days_in_month()
        return self.month_percentage


    def amount_left(self):
        self.base_amount_left -= self.payment()
        return self.base_amount_left


    def full_payment(self):
        self.full_month_payment = self.month_rates() + self.payment()
        return self.full_month_payment


    def __str__(self):
        return ("{0:<12} {3:<11.2f} {2:<12.2f} {1:<10.2f} {4:<12.2f}".format
               (self.payment_date(), self.full_payment(), self.month_rates(), self.payment(), self.amount_left()))


class AnnuityPayments(DifferentPayments):
    def full_payment(self):
        self.full_month_payment = (self.amount * (self.rate / 1200))/(1 - ((1 + (self.rate / 1200))**-self.time))
        return self.full_month_payment


    def payment(self):
        return self.full_payment() - self.month_rates()


def printer(calculator):
    columns = ("{0:<4} {1:<12} {2:^11} {3:^10} {4:^10} {5:^10}\n".format
              ("N", "Date", "BasePayment", "Percentage", "Payment", "Left"))
    columns2 = ("{0:+<4} {0:+<12} {0:+<11} {0:+<10} {0:+<10} {0:+<12}\n".format("+"))
    values = ""
    for i in range(calculator.time):
        values += ("{0:<4} {1}\n".format(i+1, calculator))
    return columns, columns2, values


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
            time = int(input("Enter time: "))
            arguments = True
        except ValueError:
            print("Time must be integer.")
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
            m = AnnuityPayments(amount, time, rate, date)
            columns, columns2, values = printer(m)
            print(columns, columns2, values, sep="")
            arguments = False
        elif calculator_type == "2":
            m = DifferentPayments(amount, time, rate, date)
            columns, columns2, values = printer(m)
            print(columns, columns2, values, sep="")
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


def export_txt(columns, columns2, values):
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