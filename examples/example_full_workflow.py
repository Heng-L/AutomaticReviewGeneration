"""
完整示例：从文献搜索到约束提取
Complete Example: From Literature Search to Constraint Extraction

注意：此示例需要SerpAPI密钥才能运行文献搜索部分
Note: This example requires SerpAPI key to run the literature search part

如果没有API密钥，可以跳过搜索步骤，直接从已有的文本文件提取。
If you don't have API key, you can skip the search step and extract from existing text files.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_without_api():
    """
    演示：不使用API，仅从示例文件提取
    Demo: Extract from sample files without API
    """
    print("="*70)
    print("演示模式：从示例文件提取约束条件")
    print("Demo Mode: Extract constraints from sample files")
    print("="*70)
    
    from MethodExtraction.ExtractConstraints import batch_extract_constraints
    
    # 设置路径
    input_folder = os.path.join(os.path.dirname(__file__), 'sample_papers')
    output_folder = os.path.join(os.path.dirname(__file__), 'full_demo_output')
    
    print(f"\n📁 输入文件夹: {input_folder}")
    print(f"📁 输出文件夹: {output_folder}")
    
    # 批量提取
    print(f"\n开始提取...")
    yaml_files = batch_extract_constraints(
        input_folder=input_folder,
        output_folder=output_folder,
        keyword='full_demo',
        max_papers=10
    )
    
    print(f"\n✅ 完成! 共生成 {len(yaml_files)} 个YAML文件:")
    for yaml_file in yaml_files:
        print(f"   ✓ {os.path.basename(yaml_file)}")
    
    return yaml_files


def demo_with_api(api_key):
    """
    演示：使用API搜索并提取
    Demo: Search with API and extract
    
    Args:
        api_key: SerpAPI密钥
    """
    print("="*70)
    print("完整演示：文献搜索 + 约束提取")
    print("Full Demo: Literature Search + Constraint Extraction")
    print("="*70)
    
    from MethodExtraction.IntegratedWorkflow import search_and_extract_constraints
    
    # 设置搜索参数
    keyword = "computational fluid dynamics channel flow"
    year_start = 2023
    year_end = 2024
    max_papers = 3
    
    print(f"\n🔍 搜索参数:")
    print(f"   关键词: {keyword}")
    print(f"   年份范围: {year_start} - {year_end}")
    print(f"   最大文献数: {max_papers}")
    
    # 执行完整工作流
    print(f"\n开始执行完整工作流...")
    
    try:
        search_and_extract_constraints(
            keyword=keyword,
            api_keys=[api_key],
            year_start=year_start,
            year_end=year_end,
            max_papers=max_papers,
            output_dir="./full_demo_constraints"
        )
    except Exception as e:
        print(f"\n⚠️  搜索过程出错: {str(e)}")
        print("这可能是因为:")
        print("  1. API密钥无效或已过期")
        print("  2. 网络连接问题")
        print("  3. API调用次数超限")
        print("\n将切换到演示模式...")
        return demo_without_api()


def analyze_results(yaml_files):
    """
    分析提取结果
    Analyze extraction results
    """
    import yaml
    from collections import Counter
    
    print(f"\n" + "="*70)
    print("结果分析 (Result Analysis)")
    print("="*70)
    
    all_equations = []
    all_schemes = []
    all_variables = []
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 收集方程
        for eq in data['governing_equations']:
            if eq['equation'] != '待定':
                all_equations.append(eq['equation'][:50] + '...')
        
        # 收集离散格式
        for scheme in data['discretization']['spatial_scheme']:
            if scheme != '待定':
                all_schemes.append(scheme)
        
        # 收集变量
        for var in data['variables']:
            if var['symbol'] != '待定':
                all_variables.append(var['symbol'])
    
    # 统计
    print(f"\n📊 统计信息:")
    print(f"   总文献数: {len(yaml_files)}")
    print(f"   总方程数: {len(all_equations)}")
    print(f"   总变量数: {len(all_variables)}")
    print(f"   总离散格式数: {len(all_schemes)}")
    
    # 最常见的离散格式
    print(f"\n📈 最常用的离散格式 (Top 5):")
    scheme_counts = Counter(all_schemes)
    for scheme, count in scheme_counts.most_common(5):
        print(f"   {count}x: {scheme[:60]}")
    
    # 最常见的变量
    print(f"\n🔤 最常见的变量 (Top 10):")
    var_counts = Counter(all_variables)
    for var, count in var_counts.most_common(10):
        print(f"   {count}x: {var}")
    
    # 方程示例
    print(f"\n📐 提取的方程示例 (前3个):")
    for i, eq in enumerate(all_equations[:3], 1):
        print(f"   {i}. {eq}")


def generate_summary_report(yaml_files, output_file="summary_report.md"):
    """
    生成摘要报告
    Generate summary report
    """
    import yaml
    
    print(f"\n" + "="*70)
    print(f"生成摘要报告: {output_file}")
    print(f"Generating summary report: {output_file}")
    print("="*70)
    
    report = []
    report.append("# 约束提取摘要报告\n")
    report.append("# Constraint Extraction Summary Report\n\n")
    report.append(f"生成时间: {os.popen('date').read()}\n")
    report.append(f"总文献数: {len(yaml_files)}\n\n")
    report.append("---\n\n")
    
    for i, yaml_file in enumerate(yaml_files, 1):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        report.append(f"## 文献 {i}: {data['metadata']['doi']}\n\n")
        
        # 方程
        n_eq = len([eq for eq in data['governing_equations'] if eq['equation'] != '待定'])
        report.append(f"**控制方程**: {n_eq} 个\n\n")
        for eq in data['governing_equations'][:2]:
            if eq['equation'] != '待定':
                report.append(f"- `{eq['equation'][:60]}...`\n")
        report.append("\n")
        
        # 变量
        n_var = len([v for v in data['variables'] if v['symbol'] != '待定'])
        report.append(f"**变量定义**: {n_var} 个\n\n")
        for var in data['variables'][:3]:
            if var['symbol'] != '待定':
                report.append(f"- {var['symbol']}: {var['description']} ({var['unit']})\n")
        report.append("\n")
        
        # 边界条件
        n_bc = len([bc for bc in data['boundary_conditions']['spatial'] if bc != '待定'])
        report.append(f"**边界条件**: {n_bc} 个\n\n")
        
        # 离散格式
        schemes = [s for s in data['discretization']['spatial_scheme'] if s != '待定']
        report.append(f"**离散格式**: {', '.join(schemes[:2])}\n\n")
        
        report.append("---\n\n")
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(report)
    
    print(f"✅ 报告已生成: {output_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='完整演示：从文献搜索到约束提取',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 演示模式（不需要API密钥）:
   python example_full_workflow.py --demo

2. 完整模式（需要API密钥）:
   python example_full_workflow.py --api YOUR_SERPAPI_KEY

3. 仅分析已有结果:
   python example_full_workflow.py --analyze ./output_folder
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='演示模式：使用示例文件（不需要API）')
    parser.add_argument('--api', type=str,
                       help='SerpAPI密钥（用于文献搜索）')
    parser.add_argument('--analyze', type=str,
                       help='分析已有YAML文件的文件夹')
    
    args = parser.parse_args()
    
    if args.analyze:
        # 仅分析模式
        import glob
        yaml_files = glob.glob(os.path.join(args.analyze, '*.yaml'))
        if not yaml_files:
            print(f"错误: 在 {args.analyze} 中未找到YAML文件")
            return
        analyze_results(yaml_files)
        generate_summary_report(yaml_files)
        
    elif args.api:
        # 完整模式（有API）
        yaml_files = demo_with_api(args.api)
        if yaml_files:
            analyze_results(yaml_files)
            generate_summary_report(yaml_files)
    
    else:
        # 演示模式（默认）
        print("\n💡 提示: 使用 --api YOUR_KEY 可以运行完整的文献搜索功能")
        print("💡 Tip: Use --api YOUR_KEY to run full literature search\n")
        yaml_files = demo_without_api()
        if yaml_files:
            analyze_results(yaml_files)
            generate_summary_report(yaml_files)
    
    print("\n" + "="*70)
    print("✅ 完整演示结束!")
    print("✅ Full demo completed!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
