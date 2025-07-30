import json
import datetime

def fetch_ticks(redis_cursor, stocks_list):
    """Function to fetch new ticks from Redis Cursor"""
    try:
        print("Fetching New Ticks from Redis")
        sub = redis_cursor.pubsub()
        sub.subscribe(stocks_list)
        for message in sub.listen():
            if message is not None and isinstance(message, dict):
                print(f"message : {message}")
    except Exception as e:
        print(f"Exception in fetching ticks : {e}")
        pass


def fetch_current_day_open(redis_cursor, symbol):
    """ Function to Fetch Current Day Open """
    try:
        print("fetching current day open price")
        candles_list = redis_cursor.lrange(symbol, 0, 1)
        if candles_list:
            candles_dict = json.loads(candles_list[0])
            print(f"current day open : {candles_dict['open']}")
            return candles_dict["open"]
    except Exception as e:
        print(f"Exception in fetching current day open : {e}")
        return None


def fetch_live_option_candle(redis_cursor, market, symbol, strike_price, option_type):
    """Function to fetch recent option candle"""
    try:
        print(f"fetching live option candle")
        if market == "IN":
            if symbol == "NIFTY BANK":
                poc_result = redis_cursor.get('poc')
            elif symbol == "NIFTY 50":
                poc_result = redis_cursor.get('n50_poc')
            else:
                poc_result = redis_cursor.get('poc')

            options_dict = json.loads(poc_result)

            symbol_ = symbol.replace(" ", "_")
            key_name = f"{symbol_}_{str(int(strike_price))}_{option_type}"
            option_candle = options_dict[key_name]

            # Manipulating Tick Values
            option_candle["close"] = option_candle["last_price"]
            option_candle["timestamp"] = option_candle["exchange_timestamp"]
            option_candle["timestamp"] = datetime.datetime.strptime(str(option_candle["timestamp"]), '%Y-%m-%d %H:%M:%S')
            option_candle["date"] = datetime.datetime.strptime(str(option_candle["timestamp"].date()), '%Y-%m-%d')
            # option_candle["expiry"] = datetime.datetime.today().date().isoformat()

            print(f"live option_candle : {option_candle}")
            return option_candle

        elif market == "US":
            symbol_ = symbol.replace(" ", "_")
            key_name = f"{symbol_}_{str(int(strike_price))}_{option_type}"
            key_symbol = f"us_underlying:{key_name}"
            poc_result = redis_cursor.get(key_symbol)
            # underlying_dict = json.loads(poc_result)
            # option_candle = underlying_dict[key_name]
            option_candle = json.loads(poc_result)
            # Manipulating Tick Values
            option_candle["close"] = option_candle["last_price"]
            option_candle["timestamp"] = option_candle["exchange_timestamp"]
            option_candle["timestamp"] = datetime.datetime.strptime(str(option_candle["timestamp"]),
                                                                    '%Y-%m-%d %H:%M:%S')
            option_candle["date"] = datetime.datetime.strptime(str(option_candle["timestamp"].date()), '%Y-%m-%d')
            # option_candle["expiry"] = datetime.datetime.today().date().isoformat()

            print(f"live option_candle : {option_candle}")
            return option_candle
    except Exception as e:
        print(f"Exception Fetching Option Candle : {e}")
        return None


def fetch_live_option_candles(redis_cursor, symbol, strike_price, option_type):
    """ Function to fetch current-day option candles """
    try:
        print("fetchin day option candles")
        symbol_ = symbol.replace(" ", "_")
        key_name = f"{symbol_}_{str(int(strike_price))}_{option_type}"
        print(f"key_name : {key_name}")
        candles = redis_cursor.lrange(key_name, 0, -1)
        if candles:
            candles_list = [json.loads(i) for i in candles]
            print(f"total live options candles till now : {len(candles_list)}")
            return candles_list
        else:
            return None
    except Exception as e:
        print(f"Exception in fetching day option candles : {e}")
        return None

