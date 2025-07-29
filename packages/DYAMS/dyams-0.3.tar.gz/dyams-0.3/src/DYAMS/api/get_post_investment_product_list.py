import requests
import pandas as pd

field_mapping = {
    'accountName': 'post_investment_product_name',  # 产品名称
    'accountCode': 'post_investment_product_id',    # 产品代码
    'openDate': 'establishment_date',               # 成立日期
    'accountType': 'product_type',                  # 账户类型作为产品类型
    'benchmark': 'benchmark',                       # 参考基准
    'user': 'creator',                              # 用户作为创建人
    'netValueStartDate': 'NAV_start_date',          # 净值开始日期
    'netValueDate': 'latest_NAV_date',              # 最新净值日期
    'navFrequency': 'NAV_update_frequency'          # 净值更新频率
}


def get_post_investment_product_list(client, post_investment_product_id=None):

    url = f"{client.base_url}/lib/portfolio/v1/list"
    headers = client.get_headers()
    data = "[]"
    if post_investment_product_id:
        data = "[\"" + post_investment_product_id + "\"]"

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            response.raise_for_status()
        r = response.json()
        if r.get('code') == 'F00100':
            raise ValueError('rate limit')
        items = r.get('list')

        rows = []
        for item in items:
            row = {}
            for api_field, our_field in field_mapping.items():
                row[our_field] = item.get(api_field, None)
            rows.append(row)

        df = pd.DataFrame(rows)
        date_fields = ['establishment_date', 'NAV_start_date', 'latest_NAV_date']
        for field in date_fields:
            if field in df.columns:
                try:
                    df[field] = pd.to_datetime(df[field], errors='coerce').dt.strftime('%Y-%m-%d')
                except Exception:
                    pass
        return df
    except Exception as e:
        raise e
