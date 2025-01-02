# LLM-Adapt
## 内容说明
### Dataset文件夹
- 基于hdBPMN与ITSM流程库构建的长尾变化测试数据集
- test1-test12文件夹中分别包含了针对12个不同业务领域的业务流程模型，1-12.csv分别包含了针对每个业务流程模型设计的长尾变化以及预设的长尾变化业务目标
### Code文件夹
- LLM-Adapt的代码实现，功能包括：
  - BPMN与RPST转换：
  - RAG检索：rag4c.py与rag4e.py分别针对中文和英文进行了不同检索方案
  - LLM应用：使用通义千问QWen-Max API，也支持通义千问其它系列API(修改代码中的model="qwen-max"即可)，采用DASHSCOPE_API_KEY在本地配置自己的API-KEY后即可使用
  - 功能性约束验证
  - SSDT-Lane算法实现
- 可用API请参考：https://help.aliyun.com/zh/model-studio/developer-reference/what-is-qwen-llm?spm=a2c4g.11186623.0.0.74b05941QE3V4v#BQnl3
## 环境配置说明
### LLM、RAG、BPMN转RPST、与SSDT-Lane
-  requirements.txt （pip install -r requirements.txt）
- python 3.12
- Tongyi QWen API（采用DASHSCOPE_API_KEY在本地配置自己的API-KEY，配置完成后代码将自动获取，因此无需修改代码）

### 功能性约束验证
- Java 11
- Maven 3
- Node.js 20
- Npm 10
- NuSMV 2.6.0，并添加到path


## Reference
1. hdBPMN库：https://github.com/dwslab/hdBPMN
2. Signavio ITSM库：https://www.signavio.com/reference-models/itsm-process-library/
