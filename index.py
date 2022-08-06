import os
import sys
from project.solution.trader import PositionAllocator
from project.solution.config import trading_config
import project.solution.model_monster as model

sys.path = ['../'] + sys.path
sys.path = ['../../'] + sys.path
from input.contest8267.contest.protos._pyprotos import bid_pb2


def model_predict(stock_infos, demo_num=10):
    # 1 定义data 数据接口协议
    # 2 定义返回值
    resp = {stock_info.stock_id: 1 / demo_num for stock_info in stock_infos[:demo_num]}
    return resp



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

        # for stock_id in trade_position:
        #     stock_info = [x for x in resp_question.stock_infos if x.stock_id == stock_id][0]
        #
        #     bid_info = bid_pb2.BidInfo()
        #
        #     position = trade_position[stock_id]
        #
        #     bid_info.stock_id = stock_id
        #     bid_info.market_id = stock_info.market_id
        #     bid_info.bid_type = 0
        #     bid_info.bid_shares = position
        #     bid_info.bid_price = stock_info.sell_infos.prices[-1]
        #     bid_info_list.append(bid_info)

        return bid_info_list


def print_resp_bid(resp_bid, is_print=False):
    if resp_bid is None:
        return
    if not is_print:
        return
    print(f'\n[+] ---------------------------------------- bid')
    print('[+] bid_status')
    for s in resp_bid.bid_status:
        print(f'[+] stock_id = {s.stock_id}')  # 股票id
        print(f'    market_id = {s.market_id}')  # 市场id
        print(f'    transact_shares = {s.transact_shares}')  # 可成交股数
        print(f'    transact_price = {s.transact_price}')  # 成交均价
        print(f'    reason = {s.reason}')  # 反馈结果

    print('[+] position_lists')
    for p in resp_bid.position_lists:
        print(f'    stock_id = {p.stock_id}')  # 股票id
        print(f'    market_id = {p.market_id}')  # 市场id
        print(f'    cost_price = {p.cost_price}')  # 成本价
        print(f'    latest_price = {p.latest_price}')  # 最新价格
        print(f'    share = {p.share}')  # 股数
        print(f'    tradable_share = {p.tradable_share}')  # 可交易数量


# ======================================== main_pipeline ========================================
def main_pipeline(uclient):
    # [optional], get k days history data
    # resp_history = uclient.get_history(k=2)  # k <= 20

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
        if date == 0 and ti == 0:
            print_resp_bid(resp_bid)

        # check cur info (optional)
        resp_user_2 = uclient.user_info()

    # print your final score (optional)
    resp_user_final = uclient.user_info()
    final_PNL = resp_user_final.pnl
    print(f'[+] final_PNL = {final_PNL}')


def invoke(uclient):
    main_pipeline(uclient)
