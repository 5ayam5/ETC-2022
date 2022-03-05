def bond_order(buybook, sellbook):
    orders = []
    for bk in buybook:
        if bk[0] > 1000:
            orders.append({type: "ADD", "symbol": "BOND", "dir": "SELL", "price": bk[0], "size": bk[1]})
    for sk in sellbook:
        if sk[0] < 1000:
            orders.append({type: "ADD", "symbol": "BOND", "dir": "BUY", "price": sk[0], "size": sk[1]})
    return orders