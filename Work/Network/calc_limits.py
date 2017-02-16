from iterate import iterate
def upper():
    tot=0
    hits=0
    for T in iterate("./graphs_all"):
        G=T[0]
        poi=T[1]
        p_exact=(G.node[poi]['city'],G.node[poi]['state'])

        for i in G.node:
            if i==poi:continue
            if p_exact==(G.node[i]['city'],G.node[i]['state']):
                hits+=1
                break
        tot+=1

    return float(hits)/float(tot)

print upper()
