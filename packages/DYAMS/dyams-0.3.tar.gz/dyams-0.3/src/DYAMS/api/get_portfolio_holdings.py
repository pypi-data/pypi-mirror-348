import requests
import pandas as pd

field_mapping = {
    'date': 'date',
    'assetName': 'asset_name',
    'assetCode': 'asset_code',
    'securityType': 'security_type',
    'exchangeCd': 'trading_market',
    'netPrice': 'current_clean_price',
    'aiRate': 'accrued_interest',
    'chg': 'price_change',
    'amount': 'position_quantity',
    'marketValueLocal': 'position_market_value',
    'weight': 'position_weight_(net_assets)',
    'dailyProfitValueLocal': 'daily_profit_loss',
    'dailyProfitRate': 'daily_profit_loss_rate',
    'floatingProfitValueLocal': 'floating_profit_loss',
    'floatingProfitRate': 'floating_profit_loss_rate',
    'cumulativeProfitValueLocal': 'cumulative_profit_loss',
    'cumulativeProfitRate': 'cumulative_profit_loss_rate',
    'totalBuyCostLocal': 'position_cost',
    'realizedAiLocal': 'interest_income',
    'realizedProfitValueLocal': 'realized_profit_loss',
    'dueDate': 'maturity_date',
    'channel': 'trading_channel',
    'direction': 'position_direction',
    'price': 'latest_price',
    'weightTotal': 'position_weight_(total_assets)',
    'weightCost': 'position_weight_(total_cost)',
    'buyCost': 'cost_price',
    'cost': 'amortized_cost',
    'fxRate': 'valuation_exchange_rate',
    'positionTime': 'market_quotation_time',
    'holdDate': 'position_building_date',
    'partyFullName': 'issuing_entity',
    'yearToMaturity': 'remaining_maturity',
    'ytmByBrain': 'YTM_(Cost)',
    'nominalRatingInst': 'bond_rating_agency',
    'nominalRating': 'bond_rating',
    'margin': 'margin_requirement',
    'city': 'city',
    'province': 'province',
    'instRatingYY': 'issuer_rating_(YY)',
    'instRatingDate': 'issuer_rating_date',
    'instRating': 'issuer_rating',
    'nominalRatingDate': 'bond_rating_date',
    'instRatingInst': 'issuer_rating_agency'
}


def get_portfolio_holdings(client, account_code, start_date, end_date):
    url = f"{client.base_url}/lib/portfolio/v1/position"
    params = {
        'accountCode': account_code,
        'startDate': start_date,
        'endDate': end_date
    }
    headers = client.get_headers()
    try:
        response = requests.get(url, params=params, headers=headers)
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
        return df
    except Exception as e:
        raise e
