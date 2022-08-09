from project.solution.config import trading_config
import math


def cash_limiter(trade_infos, current_stock_info, available_cash, is_initial_position=False):
    if is_initial_position:
        return trade_infos

    buy_total_amount = 0
    sell_total_amount = 0

    for stock_id in trade_infos:
        trade_position = trade_infos[stock_id]
        stock_price = current_stock_info[stock_id]

        if trade_position > 0:
            buy_total_amount += trade_position * stock_price
        else:
            sell_total_amount += abs(trade_position) * stock_price

    sell_buy_unbalance = max(buy_total_amount - sell_total_amount, 0)

    if available_cash - sell_buy_unbalance < trading_config['cash_waring_floor']:
        print(f"Hit Cash Warning Floor : available_cash {available_cash } "
              f"buy_total_amount {buy_total_amount} sell_total_amount {sell_total_amount} "
              f"sell_buy_unbalance {sell_buy_unbalance}")

        limited_trade_position_infos = {}
        limited_buy_amount = buy_total_amount - sell_buy_unbalance - \
                             min(available_cash - trading_config['cash_waring_floor'], 0)
        cash_limit_factor = limited_buy_amount / buy_total_amount

        for stock_id in trade_infos:
            trade_position = trade_infos[stock_id]
            if trade_position > 0:
                limited_trade_position = math.floor(trade_position * cash_limit_factor / 100) * 100
                if limited_trade_position > 1e-5:
                    limited_trade_position_infos[stock_id] = limited_trade_position
            else:
                limited_trade_position_infos[stock_id] = trade_position

    else:
        limited_trade_position_infos = trade_infos
    return limited_trade_position_infos

# TODO add trade volume predict