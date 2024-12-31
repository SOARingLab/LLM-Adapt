import pm4py

def bpmn2rpst(file_name):
    bpmn = pm4py.read_bpmn(file_name)
    rpst = pm4py.convert_to_process_tree(bpmn)
    print(rpst)
    return rpst


if __name__ == "__main__":
    bpmn_file = "offline_credit_card_application.bpmn"  # 替换为您的BPMN XML文件路径
    bpmn2rpst(bpmn_file)