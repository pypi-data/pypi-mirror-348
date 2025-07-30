# extract_table.py

from importlib import resources
import re
import pandas as pd
from typing import List

def extract_tables_to_df(txt_path: str, header_str: str) -> pd.DataFrame:
    """
    从 txt 文件中提取所有以 header_str 为表头的表格，并合并成一个 DataFrame。

    :param txt_path: 文本文件路径
    :param header_str: 表头行的原始字符串（列名间空格须与文件中一致）
    :return: 合并后的 pandas.DataFrame，如果未找到则返回空 DataFrame
    """
    # 将 header_str 拆成列名列表
    columns = re.split(r'\s+', header_str.strip())
    # 构造一个严格匹配该表头的正则（忽略行首空格）
    header_pattern = re.compile(r'^\s*' + r'\s+'.join(re.escape(col) for col in columns) + r'\s*$')

    dfs: List[pd.DataFrame] = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if header_pattern.match(line):
            # 从下一行开始读取数据
            data_rows = []
            j = i + 1
            while j < n:
                l = lines[j].rstrip('\n')
                # 空行或非数字开头（假设数据行以数字开头）就结束
                if not l.strip() or not re.match(r'^\s*[\d\-\+\.]', l):
                    break
                # 按空白分割（任意多个空格或制表符）
                parts = re.split(r'\s+', l.strip())
                data_rows.append(parts)
                j += 1

            # 如果真的读到数据，转换为 DataFrame
            if data_rows:
                df = pd.DataFrame(data_rows, columns=columns)
                dfs.append(df)

            # 继续从 j 处寻找下一个表头
            i = j
        else:
            i += 1

    if dfs:
        # 合并并重置索引
        result = pd.concat(dfs, ignore_index=True)
        # 尝试把数值列转换为浮点
        for col in columns[1:]:
            result[col] = pd.to_numeric(result[col], errors='ignore')
        return result
    else:
        # 未发现任何表格
        return pd.DataFrame(columns=columns)


if __name__ == "__main__":
    # 示例用法
    df = extract_tables_to_df(
        "D:\\Document\\PythonScripts\\txt2csv\\src\\txt2csv\\node.lis",
        "NODE        X             Y             Z           THXY     THYZ     THZX"
    )
    print(df)
