import pandas as pd

class Loan:
    def __init__(self, amount, interest, terms, extra_paym):
        self.amount = amount
        self.interest = interest
        self.terms = terms
        self.extra_paym = extra_paym

    def getAmount(self):
        return self.amount

    def getInterest(self):
        return self.interest

    def getTerms(self):
        return self.terms

    def getExtraPayment(self):
        return self.extra_paym

    def calculation(self):
        balance = self.amount
        p = self.amount
        n = self.terms
        r = self.interest / 100 / 12
        x = self.extra_paym

        balance = float(balance)
        p = float(p)
        n = int(n)
        x = float(x)

        total_interest = 0
        if r == 0:
            monthly_paym = round(p/n, 2) + x
        else:
            monthly_paym = round(r * p / (1 - (1 + r) ** -n), 2) + x

        columns = {'Month', 'Monthly Payment', 'Principal', 'Interest', 'Total Interest', 'Balance', 'Extra Payment'}
        index = range(1, n + 1)

        df = pd.DataFrame(index=index, columns=columns)

        df['Monthly Payment'] = monthly_paym
        df['Extra Payment'] = x

        i = 1

        for index, row in df.iterrows():
            term_interest = balance * r
            df.loc[index, ['Interest']] = round(term_interest, 2)
            df.loc[index, ['Month']] = i
            i += 1

            total_interest += term_interest
            df.loc[index, ['Total Interest']] = round(total_interest, 2)

            principal = monthly_paym - term_interest
            df.loc[index, ['Principal']] = round(principal, 2)

            balance -= principal
            if (balance < 0):
                balance = 0
                df.loc[index, ['Balance']] = round(balance, 2)

                if r > 0:
                    df.drop(df.index[[index-1, n-1]])
                break
            df.loc[index, ['Balance']] = round(balance, 2)

        return df

    def interest_paid(self):
        df = self.calculation()
        return df['Interest'].sum()

    def total_paid(self):
        df = self.calculation()
        return df['Interest'].sum() + self.amount

