import SSDTLane_matrix
import intersection
import re


class Node:
    def __init__(self, name, lane, logic_type=None):
        self.name = name  # 节点名称
        self.lane = lane  # 节点所属泳道
        self.children = []
        self.parent = None
        self.logic_type = logic_type  # 逻辑关系类型 (->, X, +)

    def __repr__(self):
        return f"{self.name}_{self.lane}"


class TreeParser:
    def __init__(self, input_str):
        self.input_str = input_str
        self.nodes = []  # 存储所有节点
        self.node_map = {}  # 节点映射表，方便查找
        self.logic_nodes = []
        self.non_logic_nodes = []
        self.parse()  # 解析树结构

    def parse(self):
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
                self.logic_nodes.append('->')
                idx += 2
            elif self.input_str[idx] == 'X':
                self.logic_nodes.append('X')
                idx += 1
            elif self.input_str[idx] == '+':
                self.logic_nodes.append('+')
                idx += 1
            else:
                node_match = re.match(r'([a-zA-Z0-9_]+)_([a-zA-Z0-9]+)', self.input_str[idx:])
                if node_match:
                    node_name = node_match.group(1)
                    node_lane = node_match.group(2)
                    new_node = Node(node_name, node_lane)
                    self.nodes.append(new_node)
                    self.node_map[node_name] = new_node
                    if stack and stack[-1] != '(':
                        parent = stack[-1]
                        parent.children.append(new_node)
                        new_node.parent = parent
                    stack.append(new_node)
                    if node_name not in self.logic_nodes:
                        self.non_logic_nodes.append(new_node)
                    idx += len(node_name) + len(node_lane) + 1
                else:
                    idx += 1

    def calculate_intersection(self, other_tree):
        intersection_root = self._find_intersection(self.nodes[0], other_tree.nodes[0])
        return intersection_root

    def _find_intersection(self, node_a, node_b):
        if node_a is None or node_b is None:
            return None

        if node_a.name == node_b.name and node_a.lane == node_b.lane:
            intersection_node = Node(node_a.name, node_a.lane, node_a.logic_type)
            for child_a, child_b in zip(node_a.children, node_b.children):
                intersection_child = self._find_intersection(child_a, child_b)
                if intersection_child:
                    intersection_node.children.append(intersection_child)
            return intersection_node
        return None

    def get_activity_nodes(self):
        return {node.name + "_" + node.lane for node in self.non_logic_nodes}

    def tree_to_str(self, root):
        if root is None:
            return ""
        children_str = ",".join([self.tree_to_str(child) for child in root.children])
        if children_str:
            return f"({root.name}_{root.lane},{children_str})"
        else:
            return f"({root.name}_{root.lane})"


def expand_matrix(original_matrix, seq_union, original_nodes):
    expanded_matrix = [['no' for _ in seq_union] for _ in seq_union]

    seq_union_list = list(seq_union)
    node_to_index = {node: index for index, node in enumerate(seq_union_list)}

    for i, row in enumerate(original_matrix):
        for j, value in enumerate(row):
            row_node = original_nodes[i]
            col_node = original_nodes[j]
            if row_node in seq_union and col_node in seq_union:
                # 获取行和列在 seq_union 中的索引
                row_idx = node_to_index[row_node]
                col_idx = node_to_index[col_node]
                expanded_matrix[row_idx][col_idx] = value

    return expanded_matrix


def cal_similarity(expanded_m1, expanded_m2):
    total_elements = 0
    matching_elements = 0

    for i in range(len(expanded_m1)):
        for j in range(len(expanded_m1[i])):
            total_elements += 1
            if expanded_m1[i][j] == expanded_m2[i][j]:
                matching_elements += 1

    # 计算相似度
    similarity = matching_elements / total_elements if total_elements > 0 else 0
    return similarity


def cal_process_similarity(input_str1, input_str2):
    parser1 = TreeParser(input_str1)
    parser2 = TreeParser(input_str2)

    intersection_str = intersection.rpst_intersect(input_str1, input_str2)
    activity_nodes_1 = parser1.get_activity_nodes()
    activity_nodes_2 = parser2.get_activity_nodes()
    activity_nodes_union = activity_nodes_1.union(activity_nodes_2)

    activity_nodes_1_list = list(activity_nodes_1)
    activity_nodes_2_list = list(activity_nodes_2)
    intersection_str_list = list(intersection_str)

    m1 = SSDTLane_matrix.calSSDTLane_matrix(input_str1)
    m2 = SSDTLane_matrix.calSSDTLane_matrix(input_str2)

    expanded_m1 = expand_matrix(m1, activity_nodes_union, activity_nodes_1_list)
    expanded_m2 = expand_matrix(m2, activity_nodes_union, activity_nodes_2_list)

    similarity = cal_similarity(expanded_m1, expanded_m2)
    return similarity


if __name__ == "__main__":
    # example input
    input_str1 = "(ea_l1,X(->( ra_l1,nc_l1 )->(aa_l1, ca_l1,+(sp_l2,sw_l2,sc_l2))))"
    input_str2 = "(ea_l1,da_l1, X(->( ra_l1,nc_l1, db_l2 ), ->(aa_l1, ca_l1,+(sp_l2,sw_l2,dc_l2))))"
    process_similarity = cal_process_similarity(input_str1, input_str2)
    print(process_similarity)




