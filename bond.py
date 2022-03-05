def bond_order(buybook, sellbook):
    orders_buy = []
    orders_sell = []
    for bk in buybook:
        if bk[0] > 1000:
            orders_sell.append({type: "add", "symbol": "BOND", "dir": "SELL", "price": bk[0], "size": bk[1]})
    for sk in sellbook:
        if sk[0] < 1000:
            orders_buy.append({type: "add", "symbol": "BOND", "dir": "BUY", "price": sk[0], "size": sk[1]})
    orders_buy.sort(key=lambda x: x["price"])
    orders_sell.sort(key=lambda x: -x["price"])
    orders = []
    i = 0
    while i < min(len(orders_buy), len(orders_sell)):
        orders.append(orders_buy[i])
        orders.append(orders_sell[i])
        i += 1
    # append remaining
    orders.extend(orders_buy[i:])
    orders.extend(orders_sell[i:])
    return orders