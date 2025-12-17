import networkx as nx

from polymap.bends.i2 import NodeData


def test_nbs():
    num = 5
    node_datas = {i: {"data": NodeData(is_small=False)} for i in range(num)}
    G = nx.cycle_graph(num)
    nx.set_node_attributes(G, node_datas)
    print(G.nodes(data=True))

    for node in [0, 2, 4]:
        G.nodes(data=True)[node]["data"].is_small = True

    sgn = [n for n, d in G.nodes(data=True) if d["data"].is_small]

    print(G.edges)
    print(sgn)
    sg = nx.induced_subgraph(G, sgn)
    print(sg)
    print(list(nx.connected_components(sg)))
    print(sg.edges)
    # TODO just need to make the edges continue to be directed..


if __name__ == "__main__":
    test_nbs()
