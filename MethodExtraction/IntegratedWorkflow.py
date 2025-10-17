"""
IntegratedWorkflow.py

整合文献检索和约束提取的完整工作流
Integrated workflow combining literature search and constraint extraction
"""

import os
import sys
import time
from typing import List, Optional

# 添加父目录到路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from LiteratureSearch import Advanced_Research, Global_Journal
from MethodExtraction import ExtractConstraints


def search_and_extract_constraints(
    keyword: str,
    api_keys: List[str],
    year_start: int = 2020,
    year_end: int = 2024,
    max_papers: int = 10,
    journals: Optional[List[str]] = None,
    output_dir: str = "./constraints_output"
):
    """
    完整工作流：搜索文献并提取约束条件
    Complete workflow: search literature and extract constraints
    
    Args:
        keyword: 搜索关键词 / Search keyword
        api_keys: SerpAPI密钥列表 / List of SerpAPI keys
        year_start: 起始年份 / Start year
        year_end: 结束年份 / End year
        max_papers: 最大文献数 / Maximum number of papers
        journals: 期刊列表 / List of journals
        output_dir: 输出目录 / Output directory
    """
    
    print("=" * 60)
    print("文献检索与约束提取工作流")
    print("Literature Search and Constraint Extraction Workflow")
    print("=" * 60)
    
    # 1. 准备期刊列表
    if journals is None:
        journals = Global_Journal.ACS_second  # 使用默认期刊列表
    
    # 2. 搜索文献
    print(f"\n步骤 1/3: 搜索关键词 '{keyword}' 的文献...")
    print(f"Step 1/3: Searching for '{keyword}'...")
    
    try:
        # 创建搜索结果目录
        os.makedirs('./search_results', exist_ok=True)
        os.makedirs('./search_logs', exist_ok=True)
        
        # 执行搜索
        filename = Advanced_Research.search_online(
            key_words_fun1=[keyword],
            Journal_list=journals,
            Api_list_fun=api_keys,
            year_start=year_start,
            year_end=year_end,
            Journal_name='_method_extraction',
            Demo=True,  # 限制数量以节省API调用
            STDOUT=sys.stdout
        )
        
        print(f"✓ 搜索完成，结果保存在: ./search_results/{filename}.csv")
        print(f"✓ Search completed, results saved in: ./search_results/{filename}.csv")
        
    except Exception as e:
        print(f"✗ 搜索失败: {str(e)}")
        print(f"✗ Search failed: {str(e)}")
        return
    
    # 3. 检查是否有下载的PDF文本
    raw_pdf_dir = "./RawFromPDF"
    if not os.path.exists(raw_pdf_dir):
        print(f"\n注意: 未找到 {raw_pdf_dir} 目录")
        print(f"Note: {raw_pdf_dir} directory not found")
        print("请先下载并转换PDF文件到文本格式，或手动创建该目录并放入txt文件")
        print("Please download and convert PDFs to text first, or manually create the directory with txt files")
        
        # 创建示例目录
        os.makedirs(raw_pdf_dir, exist_ok=True)
        print(f"已创建目录: {raw_pdf_dir}")
        print(f"Created directory: {raw_pdf_dir}")
        return
    
    # 4. 提取约束条件
    print(f"\n步骤 2/3: 从文献中提取约束条件...")
    print(f"Step 2/3: Extracting constraints from literature...")
    
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 批量提取
        yaml_files = ExtractConstraints.batch_extract_constraints(
            input_folder=raw_pdf_dir,
            output_folder=output_dir,
            keyword=keyword.replace(' ', '_'),
            max_papers=max_papers
        )
        
        print(f"\n✓ 提取完成! 共生成 {len(yaml_files)} 个YAML文件")
        print(f"✓ Extraction completed! Generated {len(yaml_files)} YAML files")
        
        # 5. 显示结果
        print(f"\n步骤 3/3: 生成的文件列表:")
        print(f"Step 3/3: Generated files:")
        for yaml_file in yaml_files:
            print(f"  - {yaml_file}")
        
    except Exception as e:
        print(f"✗ 提取失败: {str(e)}")
        print(f"✗ Extraction failed: {str(e)}")
        return
    
    print("\n" + "=" * 60)
    print("工作流完成!")
    print("Workflow completed!")
    print("=" * 60)


def main():
    """
    主函数
    Main function
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='整合文献检索和约束提取',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法 / Example usage:
    
    python IntegratedWorkflow.py -k "computational fluid dynamics" -a YOUR_API_KEY
    
    python IntegratedWorkflow.py -k "机器学习" -a KEY1 KEY2 -y 2020 2023 -m 5
        """
    )
    
    parser.add_argument('--keyword', '-k', required=True, 
                       help='搜索关键词 / Search keyword')
    parser.add_argument('--api', '-a', nargs='+', required=True,
                       help='SerpAPI密钥（可以提供多个）/ SerpAPI keys (can provide multiple)')
    parser.add_argument('--year', '-y', nargs=2, type=int, default=[2020, 2024],
                       metavar=('START', 'END'),
                       help='年份范围 / Year range (default: 2020 2024)')
    parser.add_argument('--max', '-m', type=int, default=10,
                       help='最大文献数 / Maximum number of papers (default: 10)')
    parser.add_argument('--output', '-o', default='./constraints_output',
                       help='输出目录 / Output directory (default: ./constraints_output)')
    
    args = parser.parse_args()
    
    # 执行工作流
    search_and_extract_constraints(
        keyword=args.keyword,
        api_keys=args.api,
        year_start=args.year[0],
        year_end=args.year[1],
        max_papers=args.max,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
