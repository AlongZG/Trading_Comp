
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
