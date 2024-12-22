from django.shortcuts import render
from .conn_postgre import conn_postgre
import pandas as pd
import numpy as np

def index(request):
    """
    渲染 ETF 排行榜
    """
    df_last_six = get_last_30_rows()
    sorted_etf_returns = calculate_sorted_30_day_avg_return(df_last_six)
    # 只取前20筆資料，並直接生成列表
    etf_list = [
        {"name": k, "avg_return": round(v * 100, 2)}
        for k, v in list(sorted_etf_returns.items())[:20]
    ]
    return render(request, './etf_rank/index.html', {'etf_list': etf_list})

def get_last_30_rows():
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM all_etf_close
    ORDER BY date DESC
    LIMIT 30;
    """
    df = pd.read_sql(query, conn)
    df = df.sort_values(by="date").reset_index(drop=True)
    conn.close()
    return df

def calculate_sorted_30_day_avg_return(df):
    # 移除所有列為 NaN 的欄位
    df = df.dropna(axis=1, how="all")
    
    # 定義禁止列表
    prohibited_list = ["00632R"]
    
    # 計算每日報酬率
    daily_returns = df.set_index("date").pct_change()
    
    # 計算最後 30 天的平均報酬率
    thirty_day_avg_returns = daily_returns.tail(30).mean()
    
    # 排序平均報酬率（由大到小）
    sorted_avg_returns = thirty_day_avg_returns.sort_values(ascending=False)
    # 清理欄位名稱，去掉 "_close"
    sorted_avg_returns.index = sorted_avg_returns.index.str.replace("_close", "")
    # 過濾掉禁止列表中的代號
    sorted_avg_returns = sorted_avg_returns[~sorted_avg_returns.index.isin(prohibited_list)]
    
    # 將結果轉為字典並返回
    return sorted_avg_returns.to_dict()







