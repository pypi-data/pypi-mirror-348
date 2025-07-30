import click
import os
from pathlib import Path
from txt2csv.functions import extract_tables_to_df

@click.group()
def cli():
    """txt2csv - 从文本文件中提取表格并转换为CSV格式的工具
    
    这个工具可以帮助您从文本文件中提取特定格式的表格数据，
    并将其转换为CSV格式保存。支持自定义表头和输入文件。
    """
    pass

@cli.command(name='extract', help='从文本文件中提取表格并保存为CSV文件')
@click.option('--input', '-i', 'input_file', 
              help='输入文件路径，默认为当前目录下的node.lis',
              default='node.lis')
@click.option('--header', '-h', 'header_str',
              help='表头字符串，默认为NODE表头',
              default='NODE        X             Y             Z           THXY     THYZ     THZX')
def extract(input_file: str, header_str: str):
    """从文本文件中提取表格并保存为CSV文件
    
    示例:
        txt2csv extract -i data.txt
        txt2csv extract -i data.txt -h "CUSTOM HEADER"
    """
    # 获取输入文件的绝对路径
    input_path = Path(input_file).resolve()
    
    if not input_path.exists():
        click.echo(f"错误：找不到输入文件 {input_file}", err=True)
        return
    
    # 提取表格
    df = extract_tables_to_df(str(input_path), header_str)
    
    if df.empty:
        click.echo("警告：未找到匹配的表格数据", err=True)
        return
    
    # 生成输出文件路径（与输入文件同目录，但扩展名改为.csv）
    output_path = input_path.with_suffix('.csv')
    
    # 保存为CSV
    df.to_csv(output_path, index=False)
    click.echo(f"成功：已将表格保存至 {output_path}")

@cli.command(name='version', help='显示当前版本信息')
def version():
    """显示当前版本信息"""
    click.echo("txt2csv version 1.0.0")

if __name__ == '__main__':
    cli()
