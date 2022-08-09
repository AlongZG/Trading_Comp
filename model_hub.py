import random
from project.solution.config import trading_config

# random.seed(86)


def strategy_monster_predict(stock_infos, total_stocks=10):
    stock_id_list = [stock_info.stock_id for stock_info in stock_infos]
    prediction = random.sample(stock_id_list, total_stocks)
    result = {stock_id: 0.5/total_stocks for stock_id in prediction}
    return result


def strategy_ranger_predict(df_market_info, model_ranger,
                            holding_stocks=trading_config['holding_stocks']):
    df_market_info['ask_bid_spread'] = df_market_info['askprice_01'].values - \
                                       df_market_info['bidprice_01'].values

    df_market_info['pred'] = model_ranger.predict(df_market_info.values)
    target_portfolio_df = df_market_info.sort_values('pred', ascending=False).iloc[:holding_stocks][[
        'stock_id']]
    target_portfolio_df['weights'] = trading_config['total_position_limiter'] / holding_stocks
    result = target_portfolio_df.set_index('stock_id').to_dict()['weights']
    return result
