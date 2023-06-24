import pickle as pkl
import requests
from os.path import exists
from datetime import date, datetime, timedelta
import json


class PolygonRequest:
    def __init__(self):
        self.__base_ep = "https://api.polygon.io"
        if exists("creds.pkl"):
            self.__api_key = pkl.load(open("creds.pkl", "rb"))
        else:
            self.__api_key = input("Please enter your API key for Polygon: ")
            pkl.dump(self.__api_key, open("creds.pkl", "wb"))
        self.__header = self.__gen_header()
        self.__log_file = "polygon_logs.txt"
        log_handling(
            log_level="INFO",
            msg="Initialized class for Polygon Request",
            log_file=self.__log_file,
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
                log_file=self.__log_file,
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

    def get_yesterday_open_close(self, ticker: str):
        ep = f"/v2/aggs/ticker/{ticker}/prev"
        error_msg = (
            "ERROR: Polygon API error - Previous Day Open/Close. Please see log file."
        )
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_all_historical_open_close(self, ticker: str):
        out = []
        for xx in range(370):
            ref_date = datetime.today() - timedelta(days=370 - xx)
            out += self.get_ticker_open_close(ticker=ticker, ref_date=ref_date)
        json.dump({"data": out}, open(f"cached_history/{ticker}.dat", "w"))
        return out


class SignalAnalysis:
    def __init__(self):
        self.__log_file = "analysis_logs.txt"
        log_handling(
            log_level="INFO",
            msg="Initialized class for Wavelet Analysis",
            log_file=self.__log_file,
        )

    def analyze_historical_ticker(self):
        # TODO: add handler for analysis
        return

    def __fft_analysis(self):
        # TODO: add fast fourier transform analysis
        return

    def __dwt_analysis(self):
        # TODO: add discrete wavelet transform analysis
        return

    def __dwpt_analysis(self):
        # TODO: add discrete wavelet packet transform analysis
        return

    def plot_fft_analysis(self):
        # TODO: add plotting function for fast fourier transform analysis
        return

    def plot_dwt_analysis(self):
        # TODO: add plotting function for discrete wavelet transform analysis
        return

    def plot_dwpt_analysis(self):
        # TODO: add plotting function for discrete wavelet packet transform analysis
        return


def log_handling(log_level: str = "ERROR", msg: str = "", log_file: str = "logs.txt"):
    out = f"{datetime.now()}: {log_level} - {msg}\n"
    with open(log_file, "a") as f:
        f.write(out)
    with open("master_logs.txt", "a") as f:
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
