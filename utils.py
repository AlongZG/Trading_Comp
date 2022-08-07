from project.solution.config import trading_config
import joblib


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


def print_resp_user(resp_user, stage='before_bid', is_print=False):
    if not is_print: return
    print(f'\n[+] ---------------------------------------- user, {stage}')
    print(f'    req_success = {resp_user.req_success}') # # 请求是否成功，True or False
    print(f'    capital = {resp_user.capital}') # 当前总资产
    print(f'    cash = {resp_user.cash}') # 总现金
    print(f'    available_cash = {resp_user.available_cash}') # 可用现金
    print(f'    pnl = {resp_user.pnl}') # 盈亏金额
    print(f'    return_rate = {resp_user.return_rate}') # 收益率
    print(f'    total_trade = {resp_user.total_trade}') # 当前天的总交易金额, 每天在ti == 33的时候会清0
    print(f'    daily_capital = {resp_user.daily_capital}') # 过去每天的总资产余额
    print(f'    daily_total_trade = {resp_user.daily_total_trade}') # 过去每天的总交易金额
    print(f'    is_alive = {resp_user.is_alive}') # 是否爆仓， 如果爆仓，程序直接终止
    print(f'    reason = {resp_user.reason}') # 爆仓原因


def select_stock_info(stock_infos):
    valid_stock_list = joblib.load(trading_config['valid_stock_path'])
    selected_stock_infos = [stock_info for stock_info in stock_infos if stock_info.stock_id in valid_stock_list]
    return selected_stock_infos

