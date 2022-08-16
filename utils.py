import pandas as pd
from project.solution.config import trading_config


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
    print(f'    req_success = {resp_user.req_success}')  # # 请求是否成功，True or False
    print(f'    capital = {resp_user.capital}')  # 当前总资产
    print(f'    cash = {resp_user.cash}')  # 总现金
    print(f'    available_cash = {resp_user.available_cash}')  # 可用现金
    print(f'    pnl = {resp_user.pnl}')  # 盈亏金额
    print(f'    return_rate = {resp_user.return_rate}')  # 收益率
    print(f'    total_trade = {resp_user.total_trade}')  # 当前天的总交易金额, 每天在ti == 33的时候会清0
    print(f'    daily_capital = {resp_user.daily_capital}')  # 过去每天的总资产余额
    print(f'    daily_total_trade = {resp_user.daily_total_trade}')  # 过去每天的总交易金额
    print(f'    is_alive = {resp_user.is_alive}')  # 是否爆仓， 如果爆仓，程序直接终止
    print(f'    reason = {resp_user.reason}')  # 爆仓原因


def select_stock_info(stock_infos, valid_stock_list):
    selected_stock_infos = [stock_info for stock_info in stock_infos if (stock_info.stock_id in valid_stock_list)]
    return selected_stock_infos


def select_tradable_stocks(stock_infos):
    tradable_stocks = [stock_info for stock_info in stock_infos if stock_info.is_tradable]
    return tradable_stocks


def market_info_parser_tick(stock_infos):
    market_info_columns = ['stock_id', 'open', 'close', 'high', 'low', 'volume', 'tvr',
                           'bidprice_01', 'bidprice_02', 'bidprice_03', 'bidprice_04',
                           'bidprice_05', 'bidprice_06', 'bidprice_07', 'bidprice_08',
                           'bidprice_09', 'bidprice_10', 'bidvolume_01', 'bidvolume_02',
                           'bidvolume_03', 'bidvolume_04', 'bidvolume_05', 'bidvolume_06',
                           'bidvolume_07', 'bidvolume_08', 'bidvolume_09', 'bidvolume_10',
                           'askprice_01', 'askprice_02', 'askprice_03', 'askprice_04',
                           'askprice_05', 'askprice_06', 'askprice_07', 'askprice_08',
                           'askprice_09', 'askprice_10', 'askvolume_01', 'askvolume_02',
                           'askvolume_03', 'askvolume_04', 'askvolume_05', 'askvolume_06',
                           'askvolume_07', 'askvolume_08', 'askvolume_09', 'askvolume_10']
    market_info_map = {stock_info.stock_id: {
        'open': stock_info.open,
        'close': stock_info.close,
        'high': stock_info.high,
        'low': stock_info.low,
        'volume': stock_info.volume,
        'tvr': stock_info.tvr,
        'bidprice_01': stock_info.buy_infos.prices[0],
        'bidprice_02': stock_info.buy_infos.prices[1],
        'bidprice_03': stock_info.buy_infos.prices[2],
        'bidprice_04': stock_info.buy_infos.prices[3],
        'bidprice_05': stock_info.buy_infos.prices[4],
        'bidprice_06': stock_info.buy_infos.prices[5],
        'bidprice_07': stock_info.buy_infos.prices[6],
        'bidprice_08': stock_info.buy_infos.prices[7],
        'bidprice_09': stock_info.buy_infos.prices[8],
        'bidprice_10': stock_info.buy_infos.prices[9],
        'bidvolume_01': stock_info.buy_infos.volumes[0],
        'bidvolume_02': stock_info.buy_infos.volumes[1],
        'bidvolume_03': stock_info.buy_infos.volumes[2],
        'bidvolume_04': stock_info.buy_infos.volumes[3],
        'bidvolume_05': stock_info.buy_infos.volumes[4],
        'bidvolume_06': stock_info.buy_infos.volumes[5],
        'bidvolume_07': stock_info.buy_infos.volumes[6],
        'bidvolume_08': stock_info.buy_infos.volumes[7],
        'bidvolume_09': stock_info.buy_infos.volumes[8],
        'bidvolume_10': stock_info.buy_infos.volumes[9],
        'askprice_01': stock_info.sell_infos.prices[0],
        'askprice_02': stock_info.sell_infos.prices[1],
        'askprice_03': stock_info.sell_infos.prices[2],
        'askprice_04': stock_info.sell_infos.prices[3],
        'askprice_05': stock_info.sell_infos.prices[4],
        'askprice_06': stock_info.sell_infos.prices[5],
        'askprice_07': stock_info.sell_infos.prices[6],
        'askprice_08': stock_info.sell_infos.prices[7],
        'askprice_09': stock_info.sell_infos.prices[8],
        'askprice_10': stock_info.sell_infos.prices[9],
        'askvolume_01': stock_info.sell_infos.volumes[0],
        'askvolume_02': stock_info.sell_infos.volumes[1],
        'askvolume_03': stock_info.sell_infos.volumes[2],
        'askvolume_04': stock_info.sell_infos.volumes[3],
        'askvolume_05': stock_info.sell_infos.volumes[4],
        'askvolume_06': stock_info.sell_infos.volumes[5],
        'askvolume_07': stock_info.sell_infos.volumes[6],
        'askvolume_08': stock_info.sell_infos.volumes[7],
        'askvolume_09': stock_info.sell_infos.volumes[8],
        'askvolume_10': stock_info.sell_infos.volumes[9]
    } for stock_info in stock_infos}

    df_market_info = pd.DataFrame(market_info_map).T
    df_market_info.index.name = 'stock_id'
    df_market_info = df_market_info.reset_index()[market_info_columns]
    return df_market_info


def market_info_parser(stock_infos, ti):
    stock_infos = select_tradable_stocks(stock_infos)

    res = []
    for stock_info in stock_infos:
        res.append([stock_info.stock_id, ti, stock_info.open, stock_info.close, stock_info.high, stock_info.low,
                    stock_info.volume, stock_info.tvr, stock_info.buy_infos.prices[0], stock_info.buy_infos.prices[1],
                    stock_info.buy_infos.prices[2], stock_info.buy_infos.prices[3], stock_info.buy_infos.prices[4],
                    stock_info.buy_infos.prices[5], stock_info.buy_infos.prices[6], stock_info.buy_infos.prices[7],
                    stock_info.buy_infos.prices[8], stock_info.buy_infos.prices[9], stock_info.buy_infos.volumes[0],
                    stock_info.buy_infos.volumes[1], stock_info.buy_infos.volumes[2], stock_info.buy_infos.volumes[3],
                    stock_info.buy_infos.volumes[4], stock_info.buy_infos.volumes[5], stock_info.buy_infos.volumes[6],
                    stock_info.buy_infos.volumes[7], stock_info.buy_infos.volumes[8], stock_info.buy_infos.volumes[9],
                    stock_info.sell_infos.prices[0], stock_info.sell_infos.prices[1], stock_info.sell_infos.prices[2],
                    stock_info.sell_infos.prices[3], stock_info.sell_infos.prices[4], stock_info.sell_infos.prices[5],
                    stock_info.sell_infos.prices[6], stock_info.sell_infos.prices[7], stock_info.sell_infos.prices[8],
                    stock_info.sell_infos.prices[9], stock_info.sell_infos.volumes[0], stock_info.sell_infos.volumes[1],
                    stock_info.sell_infos.volumes[2], stock_info.sell_infos.volumes[3],
                    stock_info.sell_infos.volumes[4], stock_info.sell_infos.volumes[5],
                    stock_info.sell_infos.volumes[6], stock_info.sell_infos.volumes[7],
                    stock_info.sell_infos.volumes[8], stock_info.sell_infos.volumes[9]])
    return res


def stocks_history_parser(resp_history, valid_stock_list, feature_list):
    result_map = []
    for ti in range(27):
        if ti not in trading_config['a_market_suspend_tick']:
            stock_infos = resp_history.stock_list[ti].daili_stock_list
            market_info_map = market_info_parser(stock_infos, ti)
            result_map += market_info_map

    df_result = pd.DataFrame(result_map)
    df_result.columns = ['stock_id', 'ti', 'open', 'close', 'high', 'low', 'volume', 'tvr', 'bidprice_01',
                         'bidprice_02', 'bidprice_03', 'bidprice_04', 'bidprice_05', 'bidprice_06', 'bidprice_07',
                         'bidprice_08', 'bidprice_09', 'bidprice_10', 'bidvolume_01', 'bidvolume_02', 'bidvolume_03',
                         'bidvolume_04', 'bidvolume_05', 'bidvolume_06', 'bidvolume_07', 'bidvolume_08', 'bidvolume_09',
                         'bidvolume_10', 'askprice_01', 'askprice_02', 'askprice_03', 'askprice_04', 'askprice_05',
                         'askprice_06', 'askprice_07', 'askprice_08', 'askprice_09', 'askprice_10', 'askvolume_01',
                         'askvolume_02', 'askvolume_03', 'askvolume_04', 'askvolume_05', 'askvolume_06', 'askvolume_07',
                         'askvolume_08', 'askvolume_09', 'askvolume_10']
    df_result[
        ['bidvolume_01', 'bidvolume_02', 'bidvolume_03', 'bidvolume_04', 'bidvolume_05', 'bidvolume_06', 'bidvolume_07',
         'bidvolume_08', 'bidvolume_09', 'bidvolume_10', 'askvolume_01', 'askvolume_02', 'askvolume_03', 'askvolume_04',
         'askvolume_05', 'askvolume_06', 'askvolume_07', 'askvolume_08', 'askvolume_09', 'askvolume_10']] = df_result[
        ['bidvolume_01', 'bidvolume_02', 'bidvolume_03', 'bidvolume_04', 'bidvolume_05', 'bidvolume_06', 'bidvolume_07',
         'bidvolume_08', 'bidvolume_09', 'bidvolume_10', 'askvolume_01', 'askvolume_02', 'askvolume_03', 'askvolume_04',
         'askvolume_05', 'askvolume_06', 'askvolume_07', 'askvolume_08', 'askvolume_09', 'askvolume_10']].astype(float)

    df_result = df_result[df_result['stock_id'].isin(valid_stock_list)]
    df_result = df_result[feature_list]

    stats = ['mean', 'std', 'min', 'max', 'first', 'last']
    dict_stats = dict.fromkeys(df_result.columns[1:], stats)
    df_stocks_history = df_result.groupby('stock_id').agg(dict_stats)
    df_stocks_history.reset_index(inplace=True)
    return df_stocks_history
