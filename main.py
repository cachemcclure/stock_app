import pickle as pkl
import requests
from os.path import exists
from datetime import date
from datetime import datetime


class PolygonRequest:
    def __init__(self):
        self.__base_ep = "https://api.polygon.io"
        if exists("creds.pkl"):
            self.__api_key = pkl.load(open("creds.pkl", "rb"))
        else:
            self.__api_key = input("Please enter your API key for Polygon: ")
            pkl.dump(self.__api_key, open("creds.pkl", "wb"))
        self.__header = self.__gen_header()
        log_handling(
            log_level="INFO", msg="Initialized class", log_file="polygon_logs.txt"
        )

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value: str):
        self.__api_key = value
        return

    def __gen_header(self):
        header = {"Authorization": f"Bearer {self.__api_key}"}
        return header

    def __send_request(self, ep: str, error_msg: str):
        url = f"{self.__base_ep}{ep}"
        response = requests.get(url=url, headers=self.__header)
        try:
            out = response.json()
            log_handling(
                log_level="INFO",
                msg=f"Request successfully submitted to {ep}",
                log_file="polygon_logs.txt",
            )
        except Exception as err:
            log_handling(log_level="ERROR", msg=str(err), log_file="polygon_logs.txt")
            print(error_msg)
            out = {}
        return out

    def get_all_available_tickers(self):
        ep = "/v3/reference/tickers"
        error_msg = (
            "ERROR: Polygon API error - All Available Tickers. Please see log file."
        )
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_ticker_details(self, ticker: str):
        ep = f"/v3/reference/tickers/{ticker}"
        error_msg = "ERROR: Polygon API error - Ticker Details. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_ticker_open_close(self, ticker: str, ref_date: date):
        ep = f"/v1/open-close/{ticker}/{ref_date.strftime('%Y-%m-%d')}"
        error_msg = "ERROR: Polygon API error - Ticker Open/Close. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out


def log_handling(log_level: str = "ERROR", msg: str = "", log_file: str = "logs.txt"):
    out = f"{datetime.now()}: {log_level} - {msg}\n"
    with open(log_file, "a") as f:
        f.write(out)


def test():
    test_date = "2022-04-01"
    ticker = "AAPL"
    test_class = PolygonRequest()
    print(test_class.get_ticker_details(ticker=ticker))
    print(
        test_class.get_ticker_open_close(
            ticker=ticker, ref_date=datetime.strptime(test_date, "%Y-%m-%d").date()
        )
    )


if __name__ == "__main__":
    test()
