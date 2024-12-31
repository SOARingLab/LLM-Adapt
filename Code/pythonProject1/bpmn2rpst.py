import xml.etree.ElementTree as ET
import networkx as nx


def parse_bpmn_xml(file_path):  # 解析BPMN XML文件并返回根元素
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def extract_bpmn_elements(root):  # 提取所有的任务及其流向
    tasks = {}
    sequence_flows = []

    for task in root.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}task"):
        task_id = task.attrib['id']
        task_name = task.attrib['name']
        incoming = [elem.text for elem in task.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming")]
        outgoing = [elem.text for elem in task.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing")]

        tasks[task_id] = {
            'name': task_name,
            'incoming': incoming,
            'outgoing': outgoing
        }

    for flow in root.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
        source_ref = flow.attrib['sourceRef']
        target_ref = flow.attrib['targetRef']
        sequence_flows.append((source_ref, target_ref))

    return tasks, sequence_flows


def build_rpst(tasks, sequence_flows):
    rpst = nx.DiGraph()  # 用图来表示RPST
    for task_id, task in tasks.items():
        rpst.add_node(task_id, type='task', name=task['name'])
    rpst.add_edges_from(sequence_flows)
    return rpst


def print_rpst(rpst):
    print("Nodes:")
    for node in rpst.nodes(data=True):
        print(f"Node: {node[0]}, Type: {node[1].get('type')}, Name: {node[1].get('name')}")
    print("\nEdges:")
    for edge in rpst.edges():
        print(f"Edge: {edge[0]} -> {edge[1]}")


def bpmn2rpst(bpmn_file):  # 此处用节点和连接线来描述RPST的树结构
    root = parse_bpmn_xml(bpmn_file)
    tasks, sequence_flows = extract_bpmn_elements(root)
    rpst = build_rpst(tasks, sequence_flows)
    # print_rpst(rpst)
    return rpst


if __name__ == "__main__":
    bpmn_file = "offline_credit_card_application.xml"  # 替换为您的BPMN XML文件路径
    bpmn2rpst(bpmn_file)
