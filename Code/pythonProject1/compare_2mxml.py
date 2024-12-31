import xml.etree.ElementTree as ET
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple

def parse_mxml(file_path: str) -> List[Tuple[str, datetime]]:
    """解析MXML文件，提取出(activity, timestamp)元组列表"""
    tree = ET.parse(file_path)
    root = tree.getroot()

    activity_timestamp_pairs = []

    # 遍历MXML的每个事件
    for trace in root.findall(".//ProcessInstance"):
        for event in trace.findall(".//AuditTrailEntry"):
            activity = event.find("WorkflowModelElement").text
            timestamp = event.find("Timestamp").text
            timestamp = datetime.fromisoformat(timestamp)
            activity_timestamp_pairs.append((activity, timestamp))

    return activity_timestamp_pairs

def calculate_activity_similarity(list1: List[str], list2: List[str]) -> float:
    """计算两个活动列表的TF-IDF余弦相似度"""
    vectorizer = TfidfVectorizer().fit_transform([' '.join(list1), ' '.join(list2)])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]

def calculate_timestamp_similarity(timestamps1: List[datetime], timestamps2: List[datetime], threshold: float = 60) -> float:
    """计算两个时间戳列表的相似度，使用时间差和阈值"""
    matched = 0
    total = min(len(timestamps1), len(timestamps2))

    for t1, t2 in zip(timestamps1, timestamps2):
        if abs((t1 - t2).total_seconds()) <= threshold:
            matched += 1

    return matched / total if total > 0 else 0

def compare_mxml_files(file1: str, file2: str):
    """比较两个MXML文件的activity和timestamp的相似度"""
    data1 = parse_mxml(file1)
    data2 = parse_mxml(file2)

    # 提取出两个文件中的activity和timestamp列表
    activities1, timestamps1 = zip(*data1)
    activities2, timestamps2 = zip(*data2)

    # 计算活动相似度
    activity_similarity = calculate_activity_similarity(list(activities1), list(activities2))

    # 计算时间戳相似度
    timestamp_similarity = calculate_timestamp_similarity(list(timestamps1), list(timestamps2))

    print(f"Activity Similarity: {activity_similarity:.2f}")
    print(f"Timestamp Similarity: {timestamp_similarity:.2f}")

# 调用
if __name__ == "__main__":
    file1 = "answer.mxml"
    file2 = "standard_res.mxml"
    compare_mxml_files(file1, file2)
