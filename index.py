import os
import sys
from project.solution.trader import PositionAllocator
from project.solution.utils import print_resp_bid
from project.solution.executor import Executor
from project.solution.config import trading_config
import project.solution.model_monster as model

sys.path = ['../'] + sys.path
sys.path = ['../../'] + sys.path
from input.contest8267.contest.protos._pyprotos import bid_pb2



# ======================================== Your Solution ========================================
class Solution:
    # a solution demo, define your solution here, good luck!
    def main(date, ti, resp_question, resp_user):
        bid_info_list = []

        if (ti in trading_config['a_market_close_tick']) or (
                ti in trading_config['h_market_close_tick']):
            return bid_info_list

        stock_infos = resp_question.stock_infos
        positions_info = resp_user.positions
        current_capital = resp_user.capital

        model_resp = model.predict(stock_infos)

        position_allocator = PositionAllocator(stock_infos=stock_infos,
                                               model_resp=model_resp,
                                               capital=current_capital,
                                               positions_info=positions_info,
                                               ti=ti)

        trade_position = position_allocator.calc_trade_position()
        print(f"trade_position {trade_position}")

        executor = Executor(stock_infos, trade_position)
        bid_info_list = executor.generate_bid_info_list()

        return bid_info_list


# ======================================== main_pipeline ========================================
def main_pipeline(uclient):
    # [optional], get k days history data
    # resp_history = uclient.get_history(k=2)  # k <= 20
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
        bid_info_list = Solution.main(date, ti, resp_question, resp_user)
        # ----------------------------------------------------------------------

        # bid
        resp_bid = uclient.bid(bid_info_list)

        print_resp_bid(resp_bid, is_print=debug)

        # check cur info (optional)
        resp_user_2 = uclient.user_info()

    # print your final score (optional)
    resp_user_final = uclient.user_info()
    final_PNL = resp_user_final.pnl
    print(f'[+] final_PNL = {final_PNL}')


def invoke(uclient):
    main_pipeline(uclient)
