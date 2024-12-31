import xml.etree.ElementTree as ET

tree = ET.parse('simulation_logs.mxml')
root = tree.getroot()

for instance in root.findall(".//ProcessInstance"):
    instance_id = instance.get('id')
    print(f"Instance ID: {instance_id}")
    for entry in instance.findall(".//AuditTrailEntry"):
        activity = entry.find("WorkflowModelElement").text
        timestamp = entry.find("Timestamp").text
        print(f"  Activity: {activity}, Timestamp: {timestamp}")
