from project.solution.config import trading_config
from project.solution.risk_crontrol import cash_limiter
import time


class PositionAllocator:
    def __init__(self, stock_infos, model_resp: dict, capital: float,
                 available_cash: float, positions_info, ti: int):

        self.stock_infos = stock_infos
        self.target_weight_info = model_resp
        self.capital = capital
        self.available_cash = available_cash
        self.position_info = positions_info
        self.ti = ti
        self.__stock_price_info = None
        self.__target_weight_info = None
        self.__current_position_info = None
        self.__target_position_info = None

    @property
    def trade_tag(self):
        if self.ti in trading_config['a_market_suspend_tick']:
            return 'h'
        else:
            return 'both'

    @property
    def is_initial_position(self):
        if abs(self.available_cash - self.capital) < 1e3:
            return True
        else:
            return 0

    @property
    def stock_price_info(self):
        if self.__stock_price_info is None:
            stock_price_info = {stock_info.stock_id: stock_info.close for stock_info in self.stock_infos
                                if (stock_info.stock_id in self.target_weight_info) or (
                                        stock_info.stock_id in self.current_position_info)}
            self.__stock_price_info = stock_price_info
        return self.__stock_price_info

    @property
    def current_position_info(self):
        if self.__current_position_info is None:
            if self.trade_tag == 'both':
                position_info_map = {position_info.stock_id: {
                    'market_id': position_info.market_id,
                    'share': position_info.share,
                    'tradable_share': position_info.tradable_share,
                } for position_info in self.position_info}
            else:
                position_info_map = {position_info.stock_id: {
                    'market_id': position_info.market_id,
                    'share': position_info.share,
                    'tradable_share': position_info.tradable_share,
                } for position_info in self.position_info if position_info.market_id == 1}

            self.__current_position_info = position_info_map

        return self.__current_position_info

    @property
    def target_position_info(self):
        if self.__target_position_info is None:
            target_position_map = {stock_id: self.get_stock_target_position(stock_id)
                                   for stock_id in self.target_weight_info}
            self.__target_position_info = target_position_map
        return self.__target_position_info

    def get_stock_target_position(self, stock_id):
        stock_price = self.stock_price_info[stock_id]
        stock_weight = self.target_weight_info[stock_id]
        try:
            stock_position = round(self.capital * stock_weight / stock_price / 100) * 100
        except (ValueError, ZeroDivisionError):
            stock_position = 0

        return stock_position

    def calc_trade_position(self):
        # TODO speed up / test performance
        start_time = time.time()

        trade_position_info = {}
        for stock_id in self.target_position_info:
            # if new position, open to target, else calc the diff
            if stock_id not in self.current_position_info:
                trade_position = self.target_position_info[stock_id]
            else:
                trade_position = self.target_position_info[stock_id] \
                                                - self.current_position_info[stock_id]['share']
            if trade_position < 0:
                trade_position = (-1) * min(abs(trade_position), self.current_position_info[stock_id]['tradable_share'])
            if abs(trade_position) > 1e-5:
                trade_position_info[stock_id] = trade_position

        for stock_id in self.current_position_info:
            if stock_id in self.target_position_info:
                pass
            else:
                trade_position = (-1) * self.current_position_info[stock_id]['tradable_share']
                if abs(trade_position) > 1e-5:
                    trade_position_info[stock_id] = trade_position

        trade_position_info = {k: v for k, v in sorted(trade_position_info.items(), key=lambda kv: (kv[1], kv[0]))}
        trade_position_info = cash_limiter(trade_position_info, self.stock_price_info, self.available_cash,
                                           is_initial_position=self.is_initial_position)
        end_time = time.time()
        print(f"Allocator time cost {end_time - start_time}s")

        return trade_position_info
