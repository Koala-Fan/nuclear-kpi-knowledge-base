#!/usr/bin/env python3
"""
将支付宝账单CSV转换为Beancount格式的脚本
"""

import csv
from datetime import datetime
import sys


def convert_alipay_to_beancount(csv_file, output_file):
    """
    将支付宝账单CSV转换为Beancount格式
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # 读取所有交易记录
        transactions = []
        for row in reader:
            # 解析交易时间
            trans_time = datetime.strptime(row['交易时间'], '%Y-%m-%d %H:%M:%S')
            date = trans_time.strftime('%Y-%m-%d')
            
            # 获取交易信息
            payee = row['交易对方']
            narration = row['商品说明']
            amount = float(row['金额'])
            category = row['交易分类']
            
            # 确定借方和贷方账户
            if row['收/支'] == '支出':
                # 支出：从资产账户支出，计入费用账户
                expense_mapping = {
                    '星巴克': 'Expenses:Food:Coffee',
                    '外卖平台': 'Expenses:Food:Takeout',
                    '超市': 'Expenses:Shopping'
                }
                
                expense_account = expense_mapping.get(payee, f'Expenses:{category}')
                asset_account = 'Assets:Alipay'  # 假设使用支付宝账户
                
                posting = {
                    'date': date,
                    'payee': payee,
                    'narration': narration,
                    'postings': [
                        {'account': expense_account, 'amount': f'{amount:.2f} CNY'},
                        {'account': asset_account, 'amount': f'-{amount:.2f} CNY'}
                    ]
                }
            elif row['收/支'] == '收入':
                # 收入：计入收入账户，增加资产
                income_account = 'Income:Salary' if '工资' in narration else f'Income:{category}'
                asset_account = 'Assets:Alipay'
                
                posting = {
                    'date': date,
                    'payee': payee,
                    'narration': narration,
                    'postings': [
                        {'account': asset_account, 'amount': f'{amount:.2f} CNY'},
                        {'account': income_account, 'amount': f'-{amount:.2f} CNY'}
                    ]
                }
            
            transactions.append(posting)
    
    # 生成Beancount格式输出
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("; Generated from Alipay bill\n\n")
        for trans in transactions:
            f.write(f"{trans['date']} * \"{trans['payee']}\" \"{trans['narration']}\"\n")
            for posting in trans['postings']:
                f.write(f"  {posting['account']}  {posting['amount']}\n")
            f.write("\n")
    
    print(f"转换完成！输出文件：{output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python convert_alipay_to_beancount.py <input_csv> <output_beancount>")
        sys.exit(1)
    
    convert_alipay_to_beancount(sys.argv[1], sys.argv[2])