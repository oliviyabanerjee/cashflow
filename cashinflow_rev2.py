import pandas as pd
import requests
from datetime import datetime


def get_fiscal_year_period_block():
    this_year = datetime.now().year
    this_month = datetime.now().month
    return (this_month - 1, this_year)

def date_selection_for_apis():
    date_today = datetime.now().date()
    fromDate = datetime(date_today.year, date_today.month, 1)
    fromDate = fromDate.strftime("%d-%b-%Y").upper()
    toDate = datetime(date_today.year, date_today.month, date_today.day)
    toDate = toDate.strftime("%d-%b-%Y").upper()
    print(fromDate, toDate)
    return (fromDate, toDate)


def fetch_bank_acc():
    url = "https://tkil-connect.thyssenkruppindianew.com:1701/api/Ceomis/GLITEM_FBL3N"
    params = {'userName': '10447195', 'password': 'mIsEg55yLCZQo5P', 'companyCode':'1000', 'fromGl' : '4000100', 'toGl':'4009999', 'xopsel':'', 'xclsel':'', 'xaisel' : 'X', 'x_Norm' : 'X'}
    dates = date_selection_for_apis()
    params['fromDate'] = dates[0]
    params['toDate'] = dates[1]
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    df = pd.DataFrame(data)
    return df



def fetch_data():
    url = "https://tkil-connect.thyssenkruppindianew.com:1701/api/Ceomis/Zfi38"
    params = { 'userName': '10447195', 'password': 'mIsEg55yLCZQo5P'}
    params['fiscalYear'] = get_fiscal_year_period_block()[1]
    params['periodBlock'] = get_fiscal_year_period_block()[0]
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def div(wbs):
    if len(wbs) == 0:
        return None
    elif wbs[0] == '2':
        return "Energy"
    elif wbs[0] == '3':
        return "MHE"
    elif wbs[0] == '1':
        return "MHE"
    elif wbs[0] == '6':
        return "Cement"
    elif wbs[0] == '4':
        return "Sugar"
    elif wbs[0] == '5':
        return "Manufacturing"
    else:
        return None


def lc_amt(x):
    if str(x)[-1] == '-':
        y = '-' + x[:-1]
        return float(y)
    else:
        return float(x)



if __name__ == "__main__":
    df = fetch_data()
    df_bacc = fetch_bank_acc()
    df = df[df["To_be_Deleted"] != "X"]
    df['LC_Amount'] = df['LC_Amount'].apply(lc_amt)
    grouped_df = df.groupby('Cle_Doc', as_index=False)['LC_Amount'].sum().reset_index()
    # # print(grouped_df.head(5))
    df_bacc['Amount in LC'] = df_bacc['Amount in LC'].apply(lc_amt)
    grouped_df_bacc = df_bacc.groupby('Document Number', as_index=False)['Amount in LC'].sum().reset_index()
    grouped_df_bacc.to_csv('fbl3n.csv')
    grouped_df.to_csv('zfi38.csv')
    print(grouped_df_bacc.head(5))
    # print(df.head(5))


    # df['Amount in LC'] = df['Amount in LC'].apply(lambda x: x.replace('.', '').replace(',', '.'))
    # df['Amount in LC'] = pd.to_numeric(df['Amount in LC'], errors='coerce').fillna(0)
    # grouped_df = df.groupby('Project Cd', as_index=False)['Amount in LC'].sum().reset_index()
    # grouped_df['bu'] = grouped_df['Project Cd'].apply(div)
    # grouped_df['version'] = datetime.today().date()
    # # df.to_excel("test2.xlsx")
    # print(grouped_df.head(5))