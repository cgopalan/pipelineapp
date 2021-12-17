import requests

URL = "https://api.coingecko.com/api/v3/coins/{coinid}/tickers"


def get_result_json(id, request_num):
    """Make call to coinGecko. If it returns error, log and proceed"""
    exchanges = []
    r = requests.get(URL.format(coinid=id))
    if r.status_code == 200:
        r_json = r.json()
        for ticker in r_json["tickers"]:
            exchanges.append(ticker["market"]["identifier"])
        return {"id": id, "exchanges": exchanges, "taskRun": request_num}
    else:
        print(f"Coin {id} not found")
