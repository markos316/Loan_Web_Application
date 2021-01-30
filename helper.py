import pandas as pd



def calculation(p, n, r):
    balance = p

    r = r / 100 / 12

    term_interest = 0

    total_interest = 0

    monthly_paym = round(r * p / (1 - (1 + r) ** -n), 2)

    columns = {'Month', 'Monthly Payment', 'Principal', 'Interest', 'Total Interest', 'Balance'}
    index = range(1, n+1)

    df = pd.DataFrame( index=index, columns=columns)

    df['Monthly Payment'] = monthly_paym

    i = 1

    for index, row in df.iterrows():
        term_interest = balance*r
        df.loc[index, ['Interest']] = round(term_interest, 2)
        df.loc[index, ['Month']] = i
        i+=1

        total_interest += term_interest
        df.loc[index, ['Total Interest']] = round(total_interest, 2)

        principal = monthly_paym - term_interest
        df.loc[index, ['Principal']] = round(principal, 2)

        balance -= principal
        if(balance<0):
            balance = 0
        df.loc[index, ['Balance']] = round(balance, 2)

    return df


print(calculation(5000, 36, 4.5))


#print(calculation(5000, 60, 4.5))