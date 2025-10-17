"""
完整示例：批量提取约束条件
Complete Example: Batch Extract Constraints

这个脚本演示如何从多个论文中批量提取数值方法和约束条件。
This script demonstrates how to batch extract numerical methods and constraints from multiple papers.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MethodExtraction.ExtractConstraints import batch_extract_constraints
import yaml


def display_yaml_summary(yaml_file):
    """
    显示YAML文件的摘要
    Display summary of YAML file
    """
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print(f"\n{'='*70}")
    print(f"文件: {os.path.basename(yaml_file)}")
    print(f"File: {os.path.basename(yaml_file)}")
    print(f"{'='*70}")
    
    # Metadata
    print(f"\n📄 元数据 (Metadata):")
    print(f"   DOI: {data['metadata']['doi']}")
    
    # Equations
    n_eq = len([eq for eq in data['governing_equations'] if eq['equation'] != '待定'])
    print(f"\n📐 控制方程 (Governing Equations): {n_eq} 个")
    for i, eq in enumerate(data['governing_equations'][:2], 1):
        if eq['equation'] != '待定':
            print(f"   {i}. {eq['equation'][:60]}...")
    
    # Variables
    n_var = len([v for v in data['variables'] if v['symbol'] != '待定'])
    print(f"\n🔤 变量定义 (Variables): {n_var} 个")
    for var in data['variables'][:3]:
        if var['symbol'] != '待定':
            print(f"   • {var['symbol']}: {var['description']} ({var['unit']})")
    
    # Boundary conditions
    n_bc = len([bc for bc in data['boundary_conditions']['spatial'] if bc != '待定'])
    print(f"\n🔲 边界条件 (Boundary Conditions): {n_bc} 个")
    for bc in data['boundary_conditions']['spatial'][:2]:
        if bc != '待定':
            print(f"   • {bc[:60]}...")
    
    # Discretization
    schemes = [s for s in data['discretization']['spatial_scheme'] if s != '待定']
    print(f"\n🔢 离散格式 (Discretization): {len(schemes)} 个")
    for scheme in schemes[:2]:
        print(f"   • {scheme[:60]}...")


def main():
    print("="*70)
    print("批量提取约束条件 - 完整示例")
    print("Batch Extract Constraints - Complete Example")
    print("="*70)
    
    # 设置路径
    input_folder = os.path.join(
        os.path.dirname(__file__), 
        'sample_papers'
    )
    output_folder = os.path.join(
        os.path.dirname(__file__), 
        'output_constraints'
    )
    
    # 检查输入文件夹
    if not os.path.exists(input_folder):
        print(f"\n❌ 错误: 输入文件夹不存在: {input_folder}")
        print(f"❌ Error: Input folder not found: {input_folder}")
        return
    
    # 列出输入文件
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    print(f"\n📁 输入文件夹: {input_folder}")
    print(f"📁 Input folder: {input_folder}")
    print(f"\n找到 {len(txt_files)} 个文本文件:")
    print(f"Found {len(txt_files)} text files:")
    for txt_file in txt_files:
        print(f"   • {txt_file}")
    
    # 批量提取
    print(f"\n{'='*70}")
    print("开始批量提取...")
    print("Starting batch extraction...")
    print(f"{'='*70}")
    
    yaml_files = batch_extract_constraints(
        input_folder=input_folder,
        output_folder=output_folder,
        keyword='demo',
        max_papers=10
    )
    
    # 显示结果
    print(f"\n{'='*70}")
    print(f"✅ 提取完成!")
    print(f"✅ Extraction completed!")
    print(f"{'='*70}")
    print(f"\n共生成 {len(yaml_files)} 个YAML文件:")
    print(f"Generated {len(yaml_files)} YAML files:")
    for yaml_file in yaml_files:
        print(f"   ✓ {yaml_file}")
    
    # 显示每个YAML文件的摘要
    print(f"\n{'='*70}")
    print("详细摘要 (Detailed Summary)")
    print(f"{'='*70}")
    
    for yaml_file in yaml_files:
        display_yaml_summary(yaml_file)
    
    # 统计分析
    print(f"\n{'='*70}")
    print("统计分析 (Statistical Analysis)")
    print(f"{'='*70}")
    
    all_schemes = []
    all_variables = []
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        schemes = data['discretization']['spatial_scheme']
        all_schemes.extend([s for s in schemes if s != '待定'])
        
        variables = [v['symbol'] for v in data['variables'] if v['symbol'] != '待定']
        all_variables.extend(variables)
    
    # 统计离散格式
    from collections import Counter
    scheme_counts = Counter(all_schemes)
    
    print("\n最常用的空间离散格式 (Most Common Spatial Schemes):")
    for scheme, count in scheme_counts.most_common(5):
        print(f"   {count}x: {scheme}")
    
    # 统计变量
    var_counts = Counter(all_variables)
    print("\n最常见的变量 (Most Common Variables):")
    for var, count in var_counts.most_common(10):
        print(f"   {count}x: {var}")
    
    print(f"\n{'='*70}")
    print("完成! 所有结果已保存到:")
    print(f"Done! All results saved to:")
    print(f"   {output_folder}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
