import sys
import time

sys.path = ['../'] + sys.path
sys.path = ['../../'] + sys.path

from input.contest8267.contest.protos._pyprotos import bid_pb2


class Executor:
    def __init__(self, stock_infos, trade_infos):
        self.stock_infos = stock_infos
        self.trade_infos = trade_infos
        self.__current_stock_info = None

    @property
    def current_stock_info(self):
        if self.__current_stock_info is None:
            current_stock_info = {stock_info.stock_id: stock_info for stock_info in self.stock_infos
                                  if (stock_info.stock_id in self.trade_infos)}
            self.__current_stock_info = current_stock_info
        return self.__current_stock_info

    @staticmethod
    def order_generator(stock_info, trade_position):
        bid_info = bid_pb2.BidInfo()
        if not stock_info.is_tradable:
            return bid_info, 'FAIL'

        bid_info.stock_id = stock_info.stock_id
        bid_info.market_id = stock_info.market_id
        bid_info.bid_shares = abs(trade_position)

        bid_info.bid_type = 0 if trade_position >= 0 else 1
        bid_info.bid_price = stock_info.sell_infos.prices[-1] if trade_position >= 0 \
            else stock_info.buy_infos.prices[-1]
        return bid_info, "SUCCESS"

    def generate_bid_info_list(self):
        start_time = time.time()
        bid_info_list = []

        for stock_id in self.trade_infos:
            stock_info = self.current_stock_info[stock_id]
            trade_position = self.trade_infos[stock_id]
            bid_info, msg = self.order_generator(stock_info, trade_position)
            if msg == "SUCCESS":
                bid_info_list.append(bid_info)

        end_time = time.time()
        print(f"Executor time cost {end_time - start_time}s")
        return bid_info_list
