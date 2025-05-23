from utilities import check_limit, log_handling
import pickle as pkl
import requests
from os.path import exists
from datetime import date, datetime, timedelta
import json
from time import sleep


CALLS = 5
RATE_LIMIT = 61


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
        check_limit()
        url = f"{self.__base_ep}{ep}"
        response = requests.get(url=url, headers=self.__header)
        try:
            out = response.json()
            if "status" in out:
                if out["status"] == "OK":
                    log_handling(
                        log_level="INFO",
                        msg=f"Request successfully submitted to {ep}",
                        log_file=self.__log_file,
                    )
                elif out["status"] == "NOT_FOUND":
                    log_handling(
                        log_level="WARNING",
                        msg=f"Request returned no results for request {ep}",
                        log_file=self.__log_file,
                    )
                else:
                    sleep(60)
                    out = self.__send_request(ep=ep, error_msg=error_msg)
            elif "results" in out:
                if "status" in out["results"]:
                    if out["results"]["status"] == "OK":
                        log_handling(
                            log_level="INFO",
                            msg=f"Request successfully submitted to {ep}",
                            log_file=self.__log_file,
                        )
                    elif out["results"]["status"] == "NOT_FOUND":
                        log_handling(
                            log_level="WARNING",
                            msg=f"Request returned no results for request {ep}",
                            log_file=self.__log_file,
                        )
                    else:
                        sleep(60)
                        out = self.__send_request(ep=ep, error_msg=error_msg)
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

    def get_all_historical_open_close(self, ticker: str, date_diff: int = 370):
        if not exists(f"cached_history/{ticker}.json"):
            out = []
            for xx in range(date_diff):
                ref_date = datetime.today() - timedelta(days=date_diff - xx)
                if ref_date.weekday() < 5:
                    temp = self.get_ticker_open_close(ticker=ticker, ref_date=ref_date)
                    if temp["status"] == "OK":
                        out += [temp]
            json.dump({"data": out}, open(f"cached_history/{ticker}.json", "w"))
            return out
        else:
            out = json.load(open(f"cached_history/{ticker}.json", "r"))
            store_date = datetime.strptime(out[-1]["from"], "%Y-%m-%d")
            if store_date != datetime.today():
                date_diff = abs((store_date - datetime.today()).days)
                for xx in range(date_diff):
                    ref_date = datetime.today() - timedelta(days=date_diff - xx)
                    if ref_date.weekday() < 5:
                        temp = self.get_ticker_open_close(
                            ticker=ticker, ref_date=ref_date
                        )
                        if temp["status"] == "OK":
                            out += [temp]
                json.dump({"data": out}, open(f"cached_history/{ticker}.json", "w"))
                return out
            else:
                return None

    def get_recent_trades(self, ticker: str, limit: int = None):
        ep = f"/v3/trades/{ticker}"
        if limit is not None:
            ep += f"?limit={limit}"
        error_msg = "ERROR: Polygon API error - Recent Trades. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_snapshot(self):
        ep = "/v2/snapshot/locale/us/markets/stocks/tickers"
        error_msg = "ERROR: Polygon API error - Snapshot. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_gainers(self):
        ep = "/v2/snapshot/locale/us/markets/stocks/gainers"
        error_msg = "ERROR: Polygon API error - Gainers. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out

    def get_losers(self):
        ep = "/v2/snapshot/locale/us/markets/stocks/losers"
        error_msg = "ERROR: Polygon API error - Losers. Please see log file."
        out = self.__send_request(ep=ep, error_msg=error_msg)
        return out


class SignalAnalysis:
    def __init__(self):
        self.__analysis_dataset = None
        self.__log_file = "analysis_logs.txt"
        log_handling(
            log_level="INFO",
            msg="Initialized class for Wavelet Analysis",
            log_file=self.__log_file,
        )

    @property
    def analysis_dataset(self):
        return self.__analysis_dataset

    @analysis_dataset.setter
    def analysis_dataset(self, dataset: list):
        self.__analysis_dataset = dataset

    def extract_dataset_from_ticker(self, ticker: str, ticker_key: str):
        if exists(f"cached_history/{ticker}.json"):
            self.__analysis_dataset = self.extract_from_ticker_data(
                ticker_key=ticker_key,
                dataset=json.load(open(f"cached_history/{ticker}.json", "r"))["data"],
            )
        else:
            stock_class = PolygonRequest()
            temp = stock_class.get_all_historical_open_close(
                ticker=ticker, date_diff=730
            )
            self.__analysis_dataset = self.extract_from_ticker_data(
                ticker_key=ticker_key, dataset=temp
            )
        return

    def extract_from_ticker_data(self, ticker_key: str, dataset: list):
        available_keys = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "afterHours",
            "preMarket",
        ]
        if ticker_key not in available_keys:
            log_handling(
                log_level="ERROR",
                msg="ERROR: Signal Analysis - Extract from Ticker Data. Please see log files.",
                log_file=self.__log_file,
            )
            out = []
        else:
            out = [xx[ticker_key] for xx in dataset]
        return out

    def analyze_historical_ticker(self, analysis: str):
        if self.__analysis_dataset is not None:
            xyz = 0
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


class ModelGeneration:
    def __init__(self):
        self.__dataset = None
        self.__train = None
        self.__test = None
        return

    @property
    def model_dataset(self):
        return self.__dataset

    @model_dataset.setter
    def model_dataset(self, dataset: list):
        self.__dataset = dataset
        return

    def model_dataset_from_ticker(self, ticker: str):
        if exists(f"cached_history/{ticker}.json"):
            temp = json.load(open(f"cached_history/{ticker}.json", "r"))
            self.__dataset = temp["data"]
        else:
            stock_class = PolygonRequest()
            self.__dataset = stock_class.get_all_historical_open_close(
                ticker=ticker, date_diff=730
            )
        return

    def gen_train_test_sets(self, split: float):
        if self.__dataset is None:
            print("You must set a dataset before invoking this function")
        else:
            train_size = int(len(self.__dataset) * split)
            self.__train, self.__test = (
                self.__dataset[:train_size, :],
                self.__dataset[train_size:, :],
            )
        return


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
    out = test_class.get_all_historical_open_close(ticker=ticker, date_diff=730)
    print(out[0])


if __name__ == "__main__":
    test()
