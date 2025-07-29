from canonical_transformer import get_mapping_of_column_pairs
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210

### IMPORTANT HOTFIX: 8186에는 몇개펀드가 누락됨. 2110으로 대체

def get_mapping_fund_names_mongodb(date_ref=None):
    mapping_codes_and_names = get_mapping_of_column_pairs(fetch_menu2210(date_ref=date_ref), key_col='펀드코드', value_col='펀드명')
    return mapping_codes_and_names

def get_mapping_fund_inception_dates_mongodb(date_ref=None):
    mapping_codes_and_dates = get_mapping_of_column_pairs(fetch_menu2210(date_ref=date_ref), key_col='펀드코드', value_col='설정일')
    return mapping_codes_and_dates
