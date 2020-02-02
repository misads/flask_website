# encoding=utf-8
from pyecharts import Graph

from app import utils
import random

def get_graph():
    relation = utils.load_yml('app/relation_north.yml')
    nodes = [{"name": relation[i]['label'], "symbolSize": 15, "draggable": "True", "value": round(20 + random.random() * 20, 3),
              "category": 3 if random.random() < 0.01 else relation[i]['category']} for i in relation]

    # nodes = [{"name": "结点1", "symbolSize": 10, "draggable": "False", "value": 10, "category": "energy"},
    #          {"name": "结点2", "symbolSize": 20, "draggable": "False", "value": 10, "category": "energy"},
    #          {"name": "结点3", "symbolSize": 30, "draggable": "False", "value": 10, "category": "energy"},
    #          {"name": "结点4", "symbolSize": 20, "draggable": "False", "value": 10, "category": "temp"},
    #          {"name": "结点5", "symbolSize": 10, "draggable": "False", "value": 10, "category": "temp"},
    #          {"name": "结点6", "symbolSize": 20, "draggable": "False", "value": 10, "category": "temp"},
    #          {"name": "结点7", "symbolSize": 30, "draggable": "False", "value": 10, "category": "flow"},
    #          {"name": "结点8", "symbolSize": 20, "draggable": "False", "value": 10, "category": "temp"}]
    #
    # nodes = [{"name": "结点1", "symbolSize": 30, "draggable": "True", "category": 0},
    #          {"name": "结点2", "symbolSize": 30, "draggable": "True", "category": 0},
    #          {"name": "结点3", "symbolSize": 30, "draggable": "True", "value": 10, "category": 1},
    #          {"name": "结点4", "symbolSize": 30, "draggable": "True", "value": 10, "category": 1},
    #          {"name": "结点5", "symbolSize": 30, "draggable": "True", "value": 10, "category": 1},
    #          {"name": "结点6", "symbolSize": 30, "draggable": "True", "value": 10, "category": 2},
    #          {"name": "结点7", "symbolSize": 30, "draggable": "True", "value": 10, "category": 2},
    #          {"name": "结点8", "symbolSize": 30, "draggable": "True", "value": 10, "category": 3}]

    categories = [{'name': '温度'},
                  {'name': '流量'},
                  {'name': '能耗'},
                  {'name': '异常'}]

    links = []

    # 计算每个结点的度 用于规划每条线的长度
    degree = {relation[i]['label']: 0 for i in relation}

    for i in relation:
        cur = relation[i]['label']
        parents = relation[i]['parents']
        for parent in parents:
            degree[cur] += 1
            degree[relation[parent]['label']] += 1

    for i in relation:
        cur = relation[i]['label']
        parents = relation[i]['parents']
        for parent in parents:
            d = min(degree[cur], degree[relation[parent]['label']])  # 取一条边连接的两个结点中较小的度
            length = 1000 // d  # - random.randint(-100, 100)
            links.append({"source": relation[parent]['label'], "target": cur, "value": length})

    label_color = ['#334553', '#B34038', '#E57F3A']
    label_color = ['#5cb85c', '#337ab7', '#f0ad4e', '#dc3545']  # success warning danger
    line_color = '#353A3F'  # 黑
    # line_color = '#555A5F'  # 黑
    # for i in range(len(nodes)-1):
    #         links.append({"source": nodes[i].get('name'), "target": nodes[i+1].get('name')})

    graph = Graph("智能建筑 | 实时监控", width=1000, height=800)
    # def xxx(g: Chart):
    #     g.get_options()

    graph.add("", nodes, links, categories,
              graph_layout="force",
              is_label_show=True,
              graph_edge_length=[50, 200],
              graph_repulsion=3,
              graph_gravity=0.001,
              is_legend_show=True,
              label_pos="right",
              line_curve=0.2,
              graph_edge_symbol=['', 'arrow'],
              graph_edge_symbolsize=7,
              label_text_color=None,
              line_color=line_color,
              line_opacity=0.75,
              is_random=False,
              label_color=label_color,
              label_formatter='{b}\n{c}')

    return graph