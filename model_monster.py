import random
random.seed(86)


def predict(stock_infos, total_stocks=10):
    stock_id_list = [stock_info.stock_id for stock_info in stock_infos]
    prediction = random.sample(stock_id_list, total_stocks)
    result = {stock_id: 0.5/total_stocks for stock_id in prediction}
    return result
