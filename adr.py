def adr_order(valebook, valbzbook):
    # i = -1
    # j = -1
    orders = []
    # done_valbz = set()
    # while i > -len(valebook) and i > -51:
    #     while j > -len(valbzbook) and j > -51:
    #         if valebook[i][0] > valbzbook[j][0] + 1:
    #             done_valbz.add(j)
    #             mn_size = 10 // (valebook[i][0] - valbzbook[j][0]) + 1
    #             orders.append({type: "add", "symbol": "VALBZ", "dir": "SELL", "price": valebook[i][0], "mn": mn_size, "mx": })
    #             break
    #     i -= 1
    if len(valebook) > 0 and len(valbzbook) > 0:
        if valebook[-1][0] > valbzbook[-1][0] + 1:
            orders.append({type: "add", "symbol": "VALBZ", "dir": "BUY", "price": valbzbook[-1][1] + 1, "size": 10})
            orders.append({type: "convert", "symbol": "VALBZ", "dir": "SELL", "size": 10 })
            orders.append({type: "add", "symbol": "VALE", "dir": "SELL", "price": valebook[-1][0] - 1, "size": 10 })

        elif valebook[-1][0] + 1 < valbzbook[-1][0]:
            orders.append({type: "add", "symbol": "VALE", "dir": "BUY", "price": valebook[-1][1] + 1, "size": 10 })
            orders.append({type: "convert", "symbol": "VALE", "dir": "SELL", "size": 10 })
            orders.append({type: "add", "symbol": "VALBZ", "dir": "SELL", "price": valbzbook[-1][0] - 1, "size": 10 })
    return orders