"""
ExtractConstraints.py

提取文献中的数值方法、模型设置、边界条件和离散格式等信息，
生成结构化的 Constraints.yaml 文件。

Extract numerical methods, model setup, boundary conditions, and discretization
schemes from literature and generate structured Constraints.yaml file.
"""

import os
import re
import sys
import yaml
from typing import Dict, List, Optional, Any


def extract_latex_equations(text: str) -> List[str]:
    """
    从文本中提取LaTeX格式的方程
    Extract LaTeX format equations from text
    
    Args:
        text: 输入文本 / Input text
        
    Returns:
        方程列表 / List of equations
    """
    equations = []
    
    # 匹配 $...$ 和 $$...$$ 格式
    # Match $...$ and $$...$$ formats
    inline_pattern = r'\$([^\$]+)\$'
    display_pattern = r'\$\$([^\$]+)\$\$'
    
    # 匹配 \begin{equation}...\end{equation} 等环境
    # Match equation environments
    env_patterns = [
        r'\\begin\{equation\}(.*?)\\end\{equation\}',
        r'\\begin\{equation\*\}(.*?)\\end\{equation\*\}',
        r'\\begin\{align\}(.*?)\\end\{align\}',
        r'\\begin\{align\*\}(.*?)\\end\{align\*\}',
    ]
    
    # 提取display模式方程
    for match in re.finditer(display_pattern, text, re.DOTALL):
        equations.append(match.group(1).strip())
    
    # 提取环境方程
    for pattern in env_patterns:
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            equations.append(match.group(1).strip())
    
    # 如果没有找到display方程，尝试提取inline方程
    if not equations:
        for match in re.finditer(inline_pattern, text):
            eq = match.group(1).strip()
            # 过滤太短的（可能是单个变量）
            if len(eq) > 5:
                equations.append(eq)
    
    return equations


def extract_variables_and_units(text: str) -> List[Dict[str, str]]:
    """
    提取变量定义及其单位
    Extract variable definitions and their units
    
    Args:
        text: 输入文本 / Input text
        
    Returns:
        变量信息列表 / List of variable information
    """
    variables = []
    
    # 常见的变量定义模式
    # Common variable definition patterns
    patterns = [
        # "where T is temperature (K)"
        r'where\s+([A-Za-z_]\w*)\s+is\s+([\w\s]+)\s*\(([^\)]+)\)',
        # "T: temperature (K)"
        r'([A-Za-z_]\w*)\s*:\s*([\w\s]+)\s*\(([^\)]+)\)',
        # "temperature T (K)"
        r'([\w\s]+)\s+([A-Za-z_]\w*)\s*\(([^\)]+)\)',
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            if len(match.groups()) == 3:
                var_dict = {
                    'symbol': match.group(1).strip() if match.group(1)[0].isupper() and len(match.group(1)) <= 3 else match.group(2).strip(),
                    'description': match.group(2).strip() if match.group(1)[0].isupper() and len(match.group(1)) <= 3 else match.group(1).strip(),
                    'unit': match.group(3).strip()
                }
                variables.append(var_dict)
    
    return variables


def extract_boundary_conditions(text: str) -> List[str]:
    """
    提取边界条件
    Extract boundary conditions
    
    Args:
        text: 输入文本 / Input text
        
    Returns:
        边界条件列表 / List of boundary conditions
    """
    conditions = []
    
    # 查找包含"boundary condition"的段落
    # Find paragraphs containing "boundary condition"
    keywords = [
        'boundary condition', 'initial condition', 
        'boundary value', 'Dirichlet', 'Neumann',
        'inlet', 'outlet', 'wall condition'
    ]
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in keywords:
            if keyword in line_lower:
                # 获取前后文
                context_start = max(0, i - 1)
                context_end = min(len(lines), i + 2)
                context = '\n'.join(lines[context_start:context_end])
                if context.strip() and context not in conditions:
                    conditions.append(context.strip())
                break
    
    return conditions


def extract_discretization_schemes(text: str) -> List[str]:
    """
    提取离散格式
    Extract discretization schemes
    
    Args:
        text: 输入文本 / Input text
        
    Returns:
        离散格式列表 / List of discretization schemes
    """
    schemes = []
    
    # 离散方法关键词
    # Discretization method keywords
    keywords = [
        'finite difference', 'finite element', 'finite volume',
        'spectral method', 'collocation', 'Galerkin',
        'upwind', 'central difference', 'backward difference',
        'forward difference', 'Runge-Kutta', 'Euler method',
        'Crank-Nicolson', 'implicit', 'explicit'
    ]
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in keywords:
            if keyword in line_lower:
                # 获取包含离散方法的句子
                sentences = re.split(r'[.!?]', line)
                for sent in sentences:
                    if keyword in sent.lower() and sent.strip():
                        schemes.append(sent.strip())
                        break
                break
    
    return schemes


def extract_method_section(text: str) -> str:
    """
    提取方法学相关章节（通常在introduction之后）
    Extract methodology section (usually after introduction)
    
    Args:
        text: 全文文本 / Full text
        
    Returns:
        方法学章节文本 / Methodology section text
    """
    # 常见的方法学章节标题
    # Common methodology section titles
    method_titles = [
        r'methods?',
        r'methodology',
        r'numerical\s+method',
        r'model\s+setup',
        r'model\s+description',
        r'computational\s+method',
        r'simulation\s+method',
        r'mathematical\s+model',
        r'governing\s+equations',
        r'boundary\s+and\s+initial\s+conditions',
    ]
    
    # 构建匹配模式
    pattern = r'\n\s*\d*\.?\s*(' + '|'.join(method_titles) + r')\s*\n'
    
    lines = text.split('\n')
    method_section = ""
    in_method_section = False
    
    for i, line in enumerate(lines):
        # 检查是否是方法学章节标题
        if re.search(pattern, '\n' + line + '\n', re.IGNORECASE):
            in_method_section = True
            method_section = line + '\n'
            continue
        
        # 如果在方法学章节中
        if in_method_section:
            # 检查是否遇到新章节（通过标题判断）
            if re.match(r'\s*\d+\.?\s+[A-Z]', line) and not line[0].isspace():
                # 可能是新章节，检查是否是结果、讨论等
                if re.search(r'(result|discussion|conclusion|reference|acknowledgment)', line, re.IGNORECASE):
                    break
            method_section += line + '\n'
    
    # 如果没有找到明确的方法学章节，尝试提取introduction之后的部分
    if not method_section or len(method_section) < 200:
        intro_pattern = r'\n\s*\d*\.?\s*(introduction)\s*\n'
        intro_match = re.search(intro_pattern, text, re.IGNORECASE)
        if intro_match:
            # 从introduction结束后开始提取
            start_pos = intro_match.end()
            # 提取接下来的3000字符作为方法学部分
            method_section = text[start_pos:start_pos + 3000]
    
    return method_section


def create_constraints_dict(
    title: str,
    doi: str,
    equations: List[str],
    variables: List[Dict[str, str]],
    boundary_conditions: List[str],
    discretization: List[str]
) -> Dict[str, Any]:
    """
    创建约束条件字典
    Create constraints dictionary
    
    Args:
        title: 文献标题 / Paper title
        doi: DOI
        equations: 方程列表 / List of equations
        variables: 变量列表 / List of variables
        boundary_conditions: 边界条件列表 / List of boundary conditions
        discretization: 离散格式列表 / List of discretization schemes
        
    Returns:
        约束条件字典 / Constraints dictionary
    """
    return {
        'metadata': {
            'title': title if title else '待定',
            'doi': doi if doi else '待定',
        },
        'governing_equations': [
            {'equation': eq, 'description': '待定'} 
            for eq in equations
        ] if equations else [{'equation': '待定', 'description': '待定'}],
        'variables': variables if variables else [
            {'symbol': '待定', 'description': '待定', 'unit': '待定'}
        ],
        'boundary_conditions': {
            'spatial': boundary_conditions if boundary_conditions else ['待定'],
            'temporal': ['待定']  # 通常需要单独提取
        },
        'initial_conditions': ['待定'],  # 需要单独提取
        'discretization': {
            'spatial_scheme': discretization if discretization else ['待定'],
            'temporal_scheme': ['待定'],
            'grid_type': '待定',
            'time_step': '待定'
        },
        'solver_settings': {
            'convergence_criteria': '待定',
            'max_iterations': '待定',
            'relaxation_factors': '待定'
        }
    }


def extract_constraints_from_literature(
    text: str,
    title: str = "",
    doi: str = ""
) -> Dict[str, Any]:
    """
    从文献文本中提取约束条件
    Extract constraints from literature text
    
    Args:
        text: 文献全文 / Full text
        title: 文献标题 / Paper title
        doi: DOI
        
    Returns:
        约束条件字典 / Constraints dictionary
    """
    # 提取方法学章节
    method_section = extract_method_section(text)
    
    # 如果没有找到方法学章节，使用全文
    if not method_section or len(method_section) < 100:
        method_section = text
    
    # 提取各种信息
    equations = extract_latex_equations(method_section)
    variables = extract_variables_and_units(method_section)
    boundary_conditions = extract_boundary_conditions(method_section)
    discretization = extract_discretization_schemes(method_section)
    
    # 创建约束条件字典
    constraints = create_constraints_dict(
        title, doi, equations, variables, 
        boundary_conditions, discretization
    )
    
    return constraints


def save_constraints_to_yaml(constraints: Dict[str, Any], output_path: str):
    """
    保存约束条件到YAML文件
    Save constraints to YAML file
    
    Args:
        constraints: 约束条件字典 / Constraints dictionary
        output_path: 输出文件路径 / Output file path
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(constraints, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def batch_extract_constraints(
    input_folder: str,
    output_folder: str,
    keyword: str = "",
    max_papers: int = 10
) -> List[str]:
    """
    批量提取约束条件
    Batch extract constraints from multiple papers
    
    Args:
        input_folder: 包含文本文件的输入文件夹 / Input folder with text files
        output_folder: 输出文件夹 / Output folder
        keyword: 关键词（用于命名）/ Keyword for naming
        max_papers: 最大处理文献数 / Maximum number of papers to process
        
    Returns:
        生成的YAML文件路径列表 / List of generated YAML file paths
    """
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')][:max_papers]
    
    yaml_files = []
    
    for i, txt_file in enumerate(txt_files):
        try:
            # 读取文件
            file_path = os.path.join(input_folder, txt_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 提取DOI（从文件名）
            doi = txt_file.replace('.txt', '') if txt_file.startswith('10.') else ""
            
            # 提取约束条件
            constraints = extract_constraints_from_literature(text, doi=doi)
            
            # 保存到YAML
            output_filename = f"Constraints_{keyword}_{i+1}.yaml" if keyword else f"Constraints_{i+1}.yaml"
            output_path = os.path.join(output_folder, output_filename)
            save_constraints_to_yaml(constraints, output_path)
            
            yaml_files.append(output_path)
            print(f"已处理: {txt_file} -> {output_filename}")
            
        except Exception as e:
            print(f"处理 {txt_file} 时出错: {str(e)}")
            continue
    
    return yaml_files


def main():
    """
    主函数 - 示例用法
    Main function - example usage
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='从文献中提取数值方法和约束条件')
    parser.add_argument('--input', '-i', required=True, help='输入文件或文件夹路径')
    parser.add_argument('--output', '-o', required=True, help='输出文件或文件夹路径')
    parser.add_argument('--keyword', '-k', default='', help='关键词（用于命名）')
    parser.add_argument('--batch', '-b', action='store_true', help='批量处理模式')
    parser.add_argument('--max', '-m', type=int, default=10, help='最大处理文献数（批量模式）')
    
    args = parser.parse_args()
    
    if args.batch:
        # 批量处理
        yaml_files = batch_extract_constraints(
            args.input,
            args.output,
            args.keyword,
            args.max
        )
        print(f"\n完成! 共生成 {len(yaml_files)} 个YAML文件")
    else:
        # 单个文件处理
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        constraints = extract_constraints_from_literature(text)
        save_constraints_to_yaml(constraints, args.output)
        print(f"完成! 已保存到 {args.output}")


if __name__ == '__main__':
    main()
