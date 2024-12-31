import re
from collections import deque


class Node:
    def __init__(self, name, lane):
        self.name = name  # 节点名称
        self.lane = lane  # 所属泳道
        self.children = []
        self.parent = None


class TreeParser:
    def __init__(self, input_str):
        self.input_str = input_str
        self.nodes = []  # 存储所有节点
        self.node_map = {}  # 节点映射表，方便查找
        self.logic_nodes = []  # 存储所有逻辑节点（->, X, +）
        self.non_logic_nodes = []  # 存储所有非逻辑节点
        self.matrix = []  # 最终矩阵
        self.parse()  # 解析RPST树结构

    def parse(self):  # 使用栈来解析树结构
        stack = []
        idx = 0
        while idx < len(self.input_str):
            if self.input_str[idx] == '(':
                stack.append('(')
                idx += 1
            elif self.input_str[idx] == ')':
                stack.pop()
                idx += 1
            elif self.input_str[idx] == ',':
                idx += 1
            elif self.input_str[idx] == '-' and self.input_str[idx + 1] == '>':
                self.logic_nodes.append('->')  # 解析顺序关系（->）
                idx += 2
            elif self.input_str[idx] == 'X':  # 解析互斥关系（X）
                self.logic_nodes.append('X')
                idx += 1
            elif self.input_str[idx] == '+':  # 解析并行关系（+）
                self.logic_nodes.append('+')
                idx += 1
            else:
                node_match = re.match(r'([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)', self.input_str[idx:])  # 匹配普通节点（带泳道后缀）
                if node_match:
                    node_name = node_match.group(1)
                    node_lane = node_match.group(2)
                    new_node = Node(node_name, node_lane)  # 创建节点
                    self.nodes.append(new_node)
                    self.node_map[node_name] = new_node
                    if stack and stack[-1] != '(':
                        parent = stack[-1]  # 上一个节点
                        parent.children.append(new_node)  # 将当前节点作为父节点的子节点
                        new_node.parent = parent
                    stack.append(new_node)  # 将新节点压入栈中
                    if node_name not in self.logic_nodes:
                        self.non_logic_nodes.append(new_node)  # 非逻辑节点
                    idx += len(node_name) + len(node_lane) + 1
                else:
                    idx += 1  # 继续向后解析

    def calculate_matrix(self):
        num_nodes = len(self.non_logic_nodes)
        self.matrix = [['' for _ in range(num_nodes)] for _ in range(num_nodes)]

        for i, node_a in enumerate(self.non_logic_nodes):
            for j, node_b in enumerate(self.non_logic_nodes):
                if i == j:
                    self.matrix[i][j] = 'no'  # 自己与自己不可达
                    continue
                self.matrix[i][j] = self.calculate_relationship(node_a, node_b)
        return self.matrix

    def calculate_relationship(self, node_a, node_b):
        if node_a.lane != node_b.lane:  # 检查节点 a 和 b 的泳道是否相同
            return self.calculate_cross_lane(node_a, node_b)

        common_ancestor = self.find_common_ancestor(node_a, node_b)  # 检查在树结构中，a和b是否属于不同的逻辑节点（优化为从父节点往上检查，寻找共同祖先，判断是X、+还是其它）
        if common_ancestor == 'X':
            return 'PAR'  # 对应论文算法中的X
        elif common_ancestor == '+':
            return self.calculate_parallel(node_a, node_b)
        else:
            return self.calculate_sequential(node_a, node_b)

    def find_common_ancestor(self, node_a, node_b):  # 递归查找a和b的公共祖先，并返回祖先的逻辑节点类型
        path_a = self.get_path_to_root(node_a)
        path_b = self.get_path_to_root(node_b)
        common_ancestor = None

        for ancestor_a, ancestor_b in zip(reversed(path_a), reversed(path_b)):  # 反向遍历路径，找到第一个共同节点
            if ancestor_a == ancestor_b:
                common_ancestor = ancestor_a
            else:
                break

        if common_ancestor is None:
            return None
        elif common_ancestor in self.logic_nodes:
            return common_ancestor
        else:
            return None

    def get_path_to_root(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = current.parent
        return path

    def calculate_cross_lane(self, node_a, node_b):
        return f'1*'

    def calculate_sequential(self, node_a, node_b):
        return '1'

    def calculate_parallel(self, node_a, node_b):
        return '1'


def calSSDTLane_matrix(input_str):
    parser = TreeParser(input_str)
    result = parser.calculate_matrix()
    return result


