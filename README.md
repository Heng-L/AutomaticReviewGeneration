<p align="center">
  <img src="https://github.com/Invalid-Null/AutomaticReviewGeneration/blob/main/Icon.png" height="150">
</p>


<h1 align="center">
  Automatic Review Generation
</h1>

基于大语言模型的自动综述生成

Automatic Review Generation Method based on Large Language Models


[![Python package](https://github.com/Invalid-Null/AutomaticReviewGeneration/actions/workflows/python-package.yml/badge.svg)](https://github.com/Invalid-Null/AutomaticReviewGeneration/actions/workflows/python-package.yml)
![GitHub License](https://img.shields.io/github/license/Invalid-Null/AutomaticReviewGeneration?logo=github)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Invalid-Null/AutomaticReviewGeneration/total)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Invalid-Null/AutomaticReviewGeneration)
![GitHub last commit](https://img.shields.io/github/last-commit/Invalid-Null/AutomaticReviewGeneration)


![Support Platform](https://img.shields.io/badge/GUI%20Platform-Windows-lightgrey.svg)
![Language](https://img.shields.io/badge/Language-Python3-yellow.svg)
![](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=Python&logoColor=ffffff) 


# Key Requirements

下述密钥必须由使用者自行提供。

The following keys must be provided by the user themselves.

 - 谷歌学术检索 Google Search API https://serpapi.com/
 - 大语言模型（二选一或均提供） LLM API (Choose one or both)
   - Claude2 https://claude.ai/chats
   - 支持Open AI 格式的模型地址和密钥 URL and Key compatible with OpenAI format
 - 爱思唯尔开发者 Elsevier Research Products APIs https://dev.elsevier.com/

# OS Requirements

*Windows* 支持此 GUI。 GUI 已在以下系统上进行了测试：

This GUI is supported for *Windows*. The GUI has been tested on the following systems:

+ Windows10:需要Microsoft edge浏览器以供实现文献下载 Microsoft edge browser is required for literature downloading.

该软件包支持 *Linux*、*Windows* 或其他支持 python3 的平台。 该软件包已在以下系统上进行了测试：

This package is supported for  *Linux*, *Windows*, or other platform supports python3. This package has been tested on the following systems:

+ Windows10: 全流程支持，需要Microsoft edge浏览器以供实现文献下载 Full process supported, Microsoft edge browser is required for literature downloading. 

+ CentOS7: 不支持文献检索模块 Without LiteratureSearch



# GUI Installation Guide:
Windows平台打包图形化界面：

Pack GUI on Windows:
```
pyinstaller -Fw GUI.py -i Icon.png
```


# Usage

[图形化界面使用中文教程](doc/GUI使用教程.md)

[English tutorial on using GUI](doc/GUI_tutorial.md)

## New Feature: Numerical Method Extraction / 新功能：数值方法提取

✨ **自动从科学文献中提取数值方法和约束条件** / Automatically extract numerical methods and constraints from scientific literature

### Features / 功能特性

- ✅ 提取LaTeX格式方程 / Extract LaTeX equations
- ✅ 提取变量定义（符号、含义、单位）/ Extract variables (symbol, description, unit)
- ✅ 提取边界条件和初始条件 / Extract boundary & initial conditions
- ✅ 提取离散格式（有限差分、有限元等）/ Extract discretization schemes (FD, FE, etc.)
- ✅ 生成结构化YAML文件 / Generate structured YAML files
- ✅ 支持批量处理 / Support batch processing

### Quick Start / 快速开始

```bash
# 单个文件提取 / Extract from single file
python MethodExtraction/ExtractConstraints.py -i paper.txt -o constraints.yaml

# 批量提取 / Batch extraction
python MethodExtraction/ExtractConstraints.py -b -i ./papers -o ./output -k "CFD" -m 10

# 运行示例 / Run example
python examples/demo_batch_extract.py
```

### Documentation / 文档

- [快速入门指南](doc/快速入门指南.md) - 10分钟上手教程
- [代码详解教程](doc/代码详解教程.md) - 面向LLM领域初学者的详细讲解
- [数值方法提取教程](doc/数值方法提取教程.md) - 完整使用教程
- [Module README](MethodExtraction/README.md) - API参考


# Publication

专利申请已被专利局接收；文章在投。[ArXiv预印本](https://arxiv.org/abs/2407.20906)

The patent application has been accepted by the Patent Office; the article is being submitted. [ArXiv Preprint](https://arxiv.org/abs/2407.20906)


# License

该项目受 **Apache 2.0 许可证**保护。

This project is covered under the **Apache 2.0 License**.
