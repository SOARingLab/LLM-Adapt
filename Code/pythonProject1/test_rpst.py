import numpy
import pandas

class TreeNode:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

def validate_rpst(pre_order, in_order):
    # 构造树的帮助函数
    def build_tree(in_order, pre_order, in_start, in_end):
        if in_start > in_end:
            return None

        t_node = TreeNode(pre_order[build_tree.pre_index])
        build_tree.pre_index += 1

        if in_start == in_end:
            return t_node

        in_index = in_order.index(t_node.val)

        t_node.left = build_tree(in_order, pre_order, in_start, in_index - 1)
        t_node.right = build_tree(in_order, pre_order, in_index + 1, in_end)

        return t_node

    # 初始化索引
    build_tree.pre_index = 0

    try:
        # 尝试构造树
        root = build_tree(in_order, pre_order, 0, len(in_order) - 1)
        return True
    except:
        return False

def modify_rpst_sequences(pre_order, in_order, events):
    modified_pre_order, modified_in_order = llm_generate_sequences(pre_order, in_order, events)

    # 验证生成的序列是否符合约束条件
    if validate_rpst(modified_pre_order, modified_in_order):
        return modified_pre_order, modified_in_order
    else:
        raise ValueError("生成的RPST序列不符合约束条件，无法唯一确定一棵树")


pre_order = ['A', 'B', 'D', 'E', 'C', 'F']
in_order = ['D', 'B', 'E', 'A', 'F', 'C']

# 获取修改后的RPST序列
modified_pre_order, modified_in_order = modify_rpst_sequences(pre_order, in_order)

print("修改后的前序遍历:", modified_pre_order)
print("修改后的中序遍历:", modified_in_order)