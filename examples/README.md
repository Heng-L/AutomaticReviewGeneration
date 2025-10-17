# Examples / 示例

本目录包含数值方法提取功能的各种示例。

This directory contains various examples for the numerical method extraction feature.

---

## 📁 文件结构 / File Structure

```
examples/
├── README.md                          # 本文件 / This file
├── sample_papers/                     # 示例论文文本 / Sample paper texts
│   ├── 10.1234_LBM_heat_transfer.txt # LBM热传递案例
│   └── 10.5678_FEM_bridge.txt        # FEM桥梁工程案例
├── example_extract_constraints.py     # 基础提取示例 / Basic extraction example
├── demo_batch_extract.py              # 批量提取演示 / Batch extraction demo
└── example_full_workflow.py           # 完整工作流示例 / Full workflow example
```

---

## 🚀 快速开始 / Quick Start

### 1. 基础示例 - 单个文件提取

```bash
python examples/example_extract_constraints.py
```

**这个示例展示**：
- 从内嵌的文本中提取约束条件
- 生成YAML文件
- 显示提取结果

**输出**：`example_constraints.yaml`

---

### 2. 批量提取演示

```bash
python examples/demo_batch_extract.py
```

**这个示例展示**：
- 从多个文本文件批量提取
- 生成多个YAML文件
- 统计分析（最常用的方法、变量等）

**输出**：`examples/output_constraints/Constraints_demo_*.yaml`

---

### 3. 完整工作流示例

```bash
# 演示模式（不需要API密钥）
python examples/example_full_workflow.py --demo

# 完整模式（需要SerpAPI密钥）
python examples/example_full_workflow.py --api YOUR_API_KEY

# 分析已有结果
python examples/example_full_workflow.py --analyze ./output_folder
```

**这个示例展示**：
- 可选的文献搜索功能
- 批量提取约束条件
- 详细的统计分析
- 生成摘要报告

**输出**：
- YAML文件
- `summary_report.md` (摘要报告)

---

## 📝 示例论文说明 / Sample Papers

### 1. LBM热传递 (10.1234_LBM_heat_transfer.txt)

**主题**：使用格子Boltzmann方法模拟通道流中的热传递

**包含内容**：
- 格子Boltzmann方程
- D2Q9格子结构
- 速度、温度分布函数
- 入口/出口/壁面边界条件
- 雷诺数和普朗特数
- 显式时间积分

### 2. FEM桥梁工程 (10.5678_FEM_bridge.txt)

**主题**：桥梁结构动力学有限元分析

**包含内容**：
- 运动方程
- 应变-位移关系
- 本构方程（胡克定律）
- 固定支座和滚动支座边界条件
- Newmark-beta时间积分
- Galerkin方法

---

## 🎯 使用场景示例 / Use Case Examples

### 场景1: 学习如何提取

如果你是第一次使用，建议按以下顺序运行：

```bash
# 步骤1: 运行基础示例
python examples/example_extract_constraints.py

# 步骤2: 查看生成的YAML
cat example_constraints.yaml

# 步骤3: 运行批量示例
python examples/demo_batch_extract.py

# 步骤4: 查看输出目录
ls examples/output_constraints/
```

### 场景2: 提取自己的论文

```bash
# 1. 准备文本文件
mkdir my_papers
# 将PDF转换的txt文件放入my_papers/

# 2. 修改demo_batch_extract.py中的路径
# 或直接使用命令行
python MethodExtraction/ExtractConstraints.py \
    -b -i ./my_papers -o ./my_output -k "my_research"

# 3. 查看结果
ls my_output/
```

### 场景3: 与文献搜索集成

```bash
# 需要SerpAPI密钥
export SERPAPI_KEY="your_key_here"

python examples/example_full_workflow.py --api $SERPAPI_KEY
```

---

## 📊 预期输出示例 / Expected Output Examples

### YAML文件示例

```yaml
metadata:
  title: 待定
  doi: 10.1234_LBM_heat_transfer

governing_equations:
  - equation: f_i(x + e_i \Delta t, t + \Delta t) - f_i(x,t) = -\frac{1}{\tau} [f_i(x,t) - f_i^{eq}(x,t)]
    description: 待定

variables:
  - symbol: u
    description: velocity
    unit: m/s

boundary_conditions:
  spatial:
    - "At the inlet: u = U_0 = 0.1 m/s"
  temporal:
    - 待定

discretization:
  spatial_scheme:
    - Explicit time integration scheme
```

### 统计分析示例

```
📊 统计信息:
   总文献数: 2
   总方程数: 11
   总变量数: 27

📈 最常用的离散格式:
   1x: finite element method
   1x: Explicit time integration scheme
```

---

## 🔧 自定义示例 / Customization

### 修改示例以适应你的需求

1. **修改输入文件夹**

```python
# 在demo_batch_extract.py中
input_folder = './your_papers'  # 改为你的文件夹
```

2. **修改提取规则**

```python
# 在ExtractConstraints.py中添加自定义模式
patterns = [
    r'你的自定义正则表达式',
]
```

3. **修改输出格式**

```python
# 在demo_batch_extract.py中添加自定义分析
def custom_analysis(yaml_files):
    # 你的分析代码
    pass
```

---

## 📚 进一步学习 / Further Learning

### 推荐阅读顺序

1. 运行 `example_extract_constraints.py` - 理解基本流程
2. 查看生成的YAML文件 - 了解输出格式
3. 运行 `demo_batch_extract.py` - 学习批量处理
4. 阅读 [快速入门指南](../doc/快速入门指南.md)
5. 阅读 [数值方法提取教程](../doc/数值方法提取教程.md)

### 相关文档

- [快速入门指南](../doc/快速入门指南.md) - 10分钟上手
- [代码详解教程](../doc/代码详解教程.md) - 面向初学者
- [数值方法提取教程](../doc/数值方法提取教程.md) - 完整教程
- [Module README](../MethodExtraction/README.md) - API参考

---

## ❓ 常见问题 / FAQ

### Q: 如何添加自己的论文？

A: 将PDF转换为txt文件，放入一个文件夹，然后运行：
```bash
python MethodExtraction/ExtractConstraints.py -b -i ./your_folder -o ./output
```

### Q: 提取结果不准确怎么办？

A: 可以：
1. 检查原始文本质量
2. 自定义提取规则（修改正则表达式）
3. 手动修正YAML文件

### Q: 如何批量分析多个YAML文件？

A: 参考 `example_full_workflow.py` 中的 `analyze_results()` 函数。

---

## 🤝 贡献示例 / Contributing Examples

欢迎贡献新的示例！

1. 创建新的示例文件
2. 添加清晰的注释
3. 更新本README
4. 提交Pull Request

---

## 📄 许可证 / License

Apache 2.0 License

---

**最后更新**: 2024-10-17  
**维护者**: AutomaticReviewGeneration Team
