import pandas as pd
import requests
from datetime import datetime


def fetch_data(fromDate, toDate):
    url = "https://tkil-connect.thyssenkruppindianew.com/api/Ceomis/Inflow_ZFI63"
    params = { 'userName': '10447195', 'password': 'mIsEg55yLCZQo5P', 'companyCode':'1000'}
    params['fromDate'] = fromDate
    params['toDate'] = toDate
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    # df.to_excel("test.xlsx")
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

if __name__ == "__main__":
    df = fetch_data("01-DEC-2020", "31-DEC-2020")
    df['Amount in LC'] = df['Amount in LC'].apply(lambda x: x.replace('.', '').replace(',', '.'))
    df['Amount in LC'] = pd.to_numeric(df['Amount in LC'], errors='coerce').fillna(0)
    grouped_df = df.groupby('Project Cd', as_index=False)['Amount in LC'].sum().reset_index()
    grouped_df['bu'] = grouped_df['Project Cd'].apply(div)
    grouped_df['version'] = datetime.today().date()
    # df.to_excel("test2.xlsx")
    print(grouped_df.head(5))