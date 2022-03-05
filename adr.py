import numpy as np

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
    valebook_buy = valebook[0]
    valebook_sell = valebook[1]
    valbzbook_buy = valbzbook[0]
    valbzbook_sell = valbzbook[1]
    
    if len(valebook_buy) > 0 and len(valbzbook_buy) > 0 and len(valbzbook_sell) > 0 and len(valebook_sell) > 0:
        bzsell = np.minimum(valbzbook_sell[0])
        lesell = np.minimum(valebook_sell[0])
        bzbuy = np.minimum(valbzbook_buy[0])
        lebuy = np.minimum(valebook_buy[0])
        if lebuy > bzsell + 1:
            orders.append({type: "add", "symbol": "VALBZ", "dir": "BUY", "price": bzsell + 1, "size": 10})
            orders.append({type: "convert", "symbol": "VALBZ", "dir": "SELL", "size": 10 })
            orders.append({type: "add", "symbol": "VALE", "dir": "SELL", "price": lebuy - 1, "size": 10 })

        elif bzbuy > lesell + 1:
            orders.append({type: "add", "symbol": "VALE", "dir": "BUY", "price": lesell + 1, "size": 10 })
            orders.append({type: "convert", "symbol": "VALE", "dir": "SELL", "size": 10 })
            orders.append({type: "add", "symbol": "VALBZ", "dir": "SELL", "price": bzbuy - 1, "size": 10 })
    return orders