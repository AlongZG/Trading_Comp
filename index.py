import os
import sys
import time
import joblib
from project.solution.trader import PositionAllocator
from project.solution.utils import print_resp_bid, print_resp_user, select_stock_info, stocks_history_parser
from project.solution.executor import Executor
from project.solution.config import trading_config
from project.solution import model_hub

sys.path = ['../'] + sys.path
sys.path = ['../../'] + sys.path
from input.contest8267.contest.protos._pyprotos import bid_pb2



# ======================================== Your Solution ========================================
class Solution:
    # a solution demo, define your solution here, good luck!
    def main(date, ti, resp_question, resp_user, valid_stock_list, resp_history,
             feature_list, model=None):
        start_time = time.time()
        bid_info_list = []

        if ti != trading_config['daily_trade_ti'] or resp_history is None:
            return bid_info_list

        select_stock_info_start_time = time.time()
        stock_infos = select_stock_info(resp_question.stock_infos, valid_stock_list)
        # A_H trading calendar not match
        if len(stock_infos) == 0:
            return bid_info_list

        df_market_info = stocks_history_parser(resp_history, valid_stock_list, feature_list)
        select_stock_info_end_time = time.time()
        print(f"parse_stock_info time cost {select_stock_info_end_time - select_stock_info_start_time}s")

        positions_info = resp_user.positions
        current_capital = resp_user.capital
        available_cash = resp_user.available_cash

        model_start_time = time.time()
        model_resp = model_hub.strategy_ranger_predict(df_market_info, model)
        print(f"model_resp {model_resp}")

        model_end_time = time.time()
        print(f"model time cost {model_end_time - model_start_time}s")

        position_allocator = PositionAllocator(stock_infos=stock_infos,
                                               model_resp=model_resp,
                                               capital=current_capital,
                                               available_cash=available_cash,
                                               positions_info=positions_info,
                                               ti=ti)

        trade_position = position_allocator.calc_trade_position()
        print(f"current_position {position_allocator.current_position_info}")
        print(f"trade_position {trade_position}")

        executor = Executor(stock_infos, trade_position)
        bid_info_list = executor.generate_bid_info_list()
        end_time = time.time()
        print(f"Ti {ti} time cost {end_time - start_time}s")

        return bid_info_list


# ======================================== main_pipeline ========================================
def main_pipeline(uclient):
    # [optional], get k days history data
    resp_history = uclient.get_history(k=1)  # k <= 20

    # prepare
    valid_stock_list = joblib.load(trading_config['valid_stock_path'])
    model_ranger = joblib.load(trading_config['model_ranger_path'])
    feature_list = joblib.load(trading_config['feature_list_path'])
    debug = True

    while True:
        date, ti = uclient.get_date_ti()
        print(f'------------------------------ date = {date}, ti = {ti} --------------------------------------------')

        # question
        resp_question = uclient.question()
        if resp_question is None:
            break

        # check cur info (optional)
        resp_user = uclient.user_info()

        # ----------------------------------------------------------------------
        # your solution
        bid_info_list = Solution.main(date, ti, resp_question, resp_user,
                                      valid_stock_list, resp_history,
                                      feature_list, model=model_ranger)
        # ----------------------------------------------------------------------

        # bid
        resp_bid = uclient.bid(bid_info_list)

        print_resp_bid(resp_bid, is_print=debug)

        # check cur info (optional)
        resp_user_2 = uclient.user_info()
        print_resp_user(resp_user_2, stage='after_bid', is_print=debug)

    # print your final score (optional)
    resp_user_final = uclient.user_info()
    final_PNL = resp_user_final.pnl
    print(f'[+] final_PNL = {final_PNL}')


def invoke(uclient):
    main_pipeline(uclient)

