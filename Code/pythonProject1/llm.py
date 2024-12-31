from http import HTTPStatus
from dashscope import Generation
import os
import rag4c
import rag4e

## single call
# def call_with_messages():
#     messages = [{'role': 'system', 'content': 'You are an expert in process modeling,familiar with process adaptation.\
#     Your goal is to modify the existing business process model based on long-tail changes and return RPST sequence.RPST means \
#     refined process structure tree. The key components of RPST include:1.SEQ(sequence):SEQ represents a series of activities \
#     that are executed in order.2.XOR(Exclusive OR):XOR represents an exclusive choice structure. Only one path is selected and \
#     executed at a time, making this structure suitable for representing decision points or conditional branches.3.AND(parallel):\
#     AND represents a parallel execution structure.4.leaf node:Leaf Nodes are the lowest level in the RPST and cannot be further \
#     decomposed, typically representing individual activities or tasks.5. In the RPST sequence I provided to you, "->" denotes \
#     SEQ, "X" denotes XOR, and "+" denotes AND. Long-tail changes result from residual uncertainty at various levels. If the uncertainty\
#      is reported L2-L3: prioritize local adjustments to the existing business processes, such as adding branches or modifying activity \
#      nodes;if reported L4 or undefined: rely on existing knowledge to address the issue.\ This is an example: original RPST sequence is \
#      "->(X(->(Receive order by website,Print out ordernote),->(Receive orderby phone,write downorder note)),bake and deliver pizza,receive payment)"\
#      Now all places need to be disinfected. The modified RPST sequence is"->(X(->(Receive order by website,Print out ordernote),->(Receive orderby phone,write downorder note)),disinfect place, bake and deliver pizza,receive payment)"\
#     '}, {'role': 'user', 'content': '请介绍一下通义千问'}]
#
#     response = Generation.call(
#         api_key=os.getenv("DASHSCOPE_API_KEY"),
#         model="qwen-max",
#         messages=messages,
#         result_format='message',
#     )
#     if response.status_code == HTTPStatus.OK:
#         print(response)
#     else:
#         print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
#             response.request_id, response.status_code,
#             response.code, response.message
#         ))


def get_response(messages):
    response = Generation.call(api_key=os.getenv("DASHSCOPE_API_KEY"),
                               model="qwen-max",
                               messages=messages,  # 将输出设置为"message"格式
                               result_format='message')
    return response


if __name__ == '__main__':
    messages = [{'role': 'system', 'content': 'You are an expert in process modeling,familiar with process adaptation.\
    Your goal is to modify the existing business process model based on long-tail changes and return RPST sequence.RPST means \
    refined process structure tree. The key components of RPST include:1.SEQ(sequence):SEQ represents a series of activities \
    that are executed in order.2.XOR(Exclusive OR):XOR represents an exclusive choice structure. Only one path is selected and \
    executed at a time, making this structure suitable for representing decision points or conditional branches.3.AND(parallel):\
    AND represents a parallel execution structure.4.leaf node:Leaf Nodes are the lowest level in the RPST and cannot be further \
    decomposed, typically representing individual activities or tasks.5. In the RPST sequence I provided to you, "->" denotes \
    SEQ, "X" denotes XOR, and "+" denotes AND. Long-tail changes result from residual uncertainty at various levels. If the uncertainty\
     is reported L2-L3: prioritize local adjustments to the existing business processes, such as adding branches or modifying activity \
     nodes;if reported L4 or undefined: rely on existing knowledge to address the issue.\ This is an example: original RPST sequence is \
     "->(X(->(Receive order by website,Print out ordernote),->(Receive orderby phone,write downorder note)),bake and deliver pizza,receive payment)"\
     Now all places need to be disinfected. The modified RPST sequence is"->(X(->(Receive order by website,Print out ordernote),->(Receive \
     orderby phone,write downorder note)),disinfect place, bake and deliver pizza,receive payment)"'}]

    for i in range(3):  #
        user_input = input("Input：")
        # rag
        context = rag4e.rag_topk_chunk(user_input, 1)
        user_input_with_rag = user_input + "You can refer to:" + context[0]
        print(user_input_with_rag)
        messages.append({'role': 'user', 'content': user_input})

        assistant_output = get_response(messages).output.choices[0]['message']['content']
        # 将大模型的回复信息添加到messages列表中
        messages.append({'role': 'assistant', 'content': assistant_output})
        print(f'模型输出：{assistant_output}')
        print('\n')
