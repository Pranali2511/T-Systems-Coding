import pandas as pd
import io
import requests
from typing import  Optional
from requests.adapters import HTTPAdapter, Retry

exr_base_url = "https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M."
url_raw_data = "https://sdwwsrest.ecb.europa.eu/service/data/BP6/"

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    url = exr_base_url + source + ".EUR.SP00.A?detail=dataonly"
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = requests.get(url,headers={'Accept': 'text/csv'},verify=False)
        df = pd.read_csv(io.StringIO(response.text))
        exr_ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
        return exr_ts
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")


def get_raw_data(identifier: str) -> pd.DataFrame:
    url = url_raw_data + identifier + "?detail=dataonly"
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = requests.get(url,headers={'Accept': 'text/csv'},verify=False)
        df = pd.read_csv(io.StringIO(response.text))
        raw_ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
        print (raw_ts)
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

def get_data(identifier: str,target_currency: Optional[str] = None) -> pd.DataFrame:
    data_df = pd.DataFrame()
    if target_currency is None:
        data_df = get_raw_data(identifier)
    else:
        source = target_currency
        exr_ts = get_exchange_rate(source)
        raw_ts = get_raw_data(identifier)
        print('exr: \n', exr_ts)
        print('ts: \n', raw_ts)
        print('op: \n', data_df)
        data_df['TIME_PERIOD'] = exr_ts['TIME_PERIOD']
        data_df['OBS_VALUE'] = exr_ts['OBS_VALUE'] * raw_ts['OBS_VALUE']
    return data_df


if __name__ == '__main__':
    #get_exchange_rate("GBP")
    #get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")

