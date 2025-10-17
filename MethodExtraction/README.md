# MethodExtraction 模块

从科学文献中自动提取数值方法和约束条件。

Automatically extract numerical methods and constraints from scientific literature.

---

## 功能特性 / Features

- ✅ 自动提取LaTeX格式方程 / Extract LaTeX equations
- ✅ 提取变量定义（符号、含义、单位）/ Extract variable definitions (symbol, description, unit)
- ✅ 提取边界条件和初始条件 / Extract boundary and initial conditions  
- ✅ 提取离散格式（有限差分、有限元等）/ Extract discretization schemes (FD, FE, etc.)
- ✅ 生成结构化YAML文件 / Generate structured YAML files
- ✅ 自动标记缺失信息为"待定" / Automatically mark missing info as "TBD"
- ✅ 支持批量处理 / Support batch processing
- ✅ 可与文献检索功能集成 / Can integrate with literature search

---

## 快速开始 / Quick Start

### 安装 / Installation

```bash
cd AutomaticReviewGeneration
pip install -r requirements.txt
```

### 基本用法 / Basic Usage

**方法1：从文本文件提取**

```bash
python MethodExtraction/ExtractConstraints.py \
    --input ./paper.txt \
    --output ./constraints.yaml
```

**方法2：批量提取**

```bash
python MethodExtraction/ExtractConstraints.py \
    --batch \
    --input ./RawFromPDF \
    --output ./output \
    --keyword "CFD" \
    --max 10
```

**方法3：完整工作流（搜索+提取）**

```bash
python MethodExtraction/IntegratedWorkflow.py \
    --keyword "computational fluid dynamics" \
    --api YOUR_SERPAPI_KEY \
    --year 2020 2024 \
    --max 5
```

---

## 模块文件 / Module Files

```
MethodExtraction/
├── __init__.py                 # 模块初始化
├── ExtractConstraints.py       # 核心提取功能
├── IntegratedWorkflow.py       # 集成工作流
└── README.md                   # 本文件
```

---

## 使用示例 / Examples

### 在Python代码中使用

```python
from MethodExtraction import extract_constraints_from_literature

# 读取文献文本
with open('paper.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取约束条件
constraints = extract_constraints_from_literature(
    text=text,
    title="My Paper Title",
    doi="10.1234/example"
)

# 查看结果
print(constraints['governing_equations'])
print(constraints['variables'])
print(constraints['boundary_conditions'])
```

### 批量处理

```python
from MethodExtraction import batch_extract_constraints

yaml_files = batch_extract_constraints(
    input_folder='./papers',
    output_folder='./constraints',
    keyword='CFD',
    max_papers=20
)

print(f"Generated {len(yaml_files)} YAML files")
```

---

## 输出格式 / Output Format

生成的YAML文件包含以下结构：

```yaml
metadata:
  title: 论文标题
  doi: 10.xxxx/xxxxx

governing_equations:
  - equation: LaTeX格式方程
    description: 方程描述

variables:
  - symbol: 变量符号
    description: 变量含义
    unit: 单位

boundary_conditions:
  spatial: [空间边界条件]
  temporal: [时间边界条件]

initial_conditions: [初始条件]

discretization:
  spatial_scheme: [空间离散格式]
  temporal_scheme: [时间离散格式]
  grid_type: 网格类型
  time_step: 时间步长

solver_settings:
  convergence_criteria: 收敛标准
  max_iterations: 最大迭代次数
  relaxation_factors: 松弛因子
```

---

## 命令行参数 / Command Line Arguments

### ExtractConstraints.py

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--input` | `-i` | 输入文件/文件夹 | 必需 |
| `--output` | `-o` | 输出文件/文件夹 | 必需 |
| `--keyword` | `-k` | 关键词（用于命名） | '' |
| `--batch` | `-b` | 批量处理模式 | False |
| `--max` | `-m` | 最大处理文件数 | 10 |

### IntegratedWorkflow.py

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--keyword` | `-k` | 搜索关键词 | 必需 |
| `--api` | `-a` | SerpAPI密钥 | 必需 |
| `--year` | `-y` | 年份范围（起始 结束） | 2020 2024 |
| `--max` | `-m` | 最大文献数 | 10 |
| `--output` | `-o` | 输出目录 | ./constraints_output |

---

## 核心函数 / Core Functions

### extract_constraints_from_literature()

从文献文本中提取约束条件。

**参数:**
- `text` (str): 文献全文
- `title` (str): 文献标题（可选）
- `doi` (str): DOI（可选）

**返回:**
- dict: 约束条件字典

### batch_extract_constraints()

批量提取多个文献的约束条件。

**参数:**
- `input_folder` (str): 输入文件夹
- `output_folder` (str): 输出文件夹
- `keyword` (str): 关键词
- `max_papers` (int): 最大处理文献数

**返回:**
- List[str]: 生成的YAML文件路径列表

---

## 自定义提取规则 / Customize Extraction Rules

可以通过修改`ExtractConstraints.py`中的正则表达式来自定义提取规则：

```python
# 添加新的变量定义模式
patterns = [
    r'where\s+([A-Za-z_]\w*)\s+is\s+([\w\s]+)\s*\(([^\)]+)\)',
    r'你的自定义模式',  # 添加新模式
]

# 添加新的章节标题
method_titles = [
    r'methods?',
    r'你的自定义标题',  # 添加新标题
]
```

---

## 常见问题 / FAQ

**Q: 为什么有些字段显示"待定"？**

A: 这表示在论文中未找到相关信息。你可以：
- 手动查阅原文补充
- 调整提取规则
- 使用LLM增强提取

**Q: 如何处理非英文文献？**

A: 当前主要支持英文。对于其他语言：
- 可以先翻译成英文
- 修改关键词匹配规则

**Q: 提取的方程格式不正确？**

A: 可能是PDF转文本时损坏。建议：
- 使用高质量PDF
- 手动修正YAML文件

---

## 完整教程 / Full Tutorial

详细教程请参阅：
- [中文教程](../doc/数值方法提取教程.md)
- [代码详解](../doc/代码详解教程.md)

---

## 贡献 / Contributing

欢迎提交Issue和Pull Request！

---

## 许可证 / License

Apache 2.0 License

---

## 更新日志 / Changelog

### v1.0.0 (2024-10-17)
- ✨ 初始版本
- ✅ 支持LaTeX方程提取
- ✅ 支持变量定义提取
- ✅ 支持边界条件提取
- ✅ 支持离散格式提取
- ✅ 支持批量处理
- ✅ 支持与文献检索集成
