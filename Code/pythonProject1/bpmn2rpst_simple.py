import pm4py

def bpmn2rpst(file_name):
    bpmn_model = pm4py.read_bpmn("offline_credit_card_application.bpmn")

    process_tree = pm4py.convert_to_process_tree(bpmn_model)
    print(process_tree)
    pm4py.view_process_tree(process_tree, format='svg')  # format='svg'
    print(process_tree)


#new_rpst = "->( X( ->( 'Receive order by website', 'Print out order note' ), ->( 'Receive order by phone', 'write down order note' ), ->( 'Receive order by Lieferando', 'Confirm order', 'Print out order note' ) ), ->( 'Attach order note to pinboard', 'Reassure customer' ), +('bake pizza quickly', 'prepare for delivery'),'deliver pizza quickly', 'receive payment' )"
#new_bpmn = pm4py.convert_to_bpmn(new_rpst)
#pm4py.view_bpmn(new_bpmn)
#preorder = pm4py.get_pre_order_traversal(process_tree)


