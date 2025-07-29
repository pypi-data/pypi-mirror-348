from canonical_transformer import get_mapping_of_column_pairs
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210
from .divisions_consts import MAPPING_DIVISION
from .main_fund_filter import filter_fund_codes_by_main_filter
from .aum_fund_filter import filter_fund_codes_by_aum_filter

def get_mapping_fund_names_by_division(key_for_division, date_ref=None):
    df = fetch_menu2210(date_ref=date_ref)
    managers = MAPPING_DIVISION[key_for_division]
    df = df[df['매니저'].isin(managers)]
    COLS_TO_KEEP = ['펀드코드', '펀드명']
    df = df[COLS_TO_KEEP]
    return get_mapping_of_column_pairs(df, key_col='펀드코드', value_col='펀드명')

def get_mapping_fund_names_division_01(date_ref=None):
    return get_mapping_fund_names_by_division('division_01', date_ref=date_ref)

def get_mapping_fund_names_division_02(date_ref=None):
    return get_mapping_fund_names_by_division('division_02', date_ref=date_ref)

def get_fund_codes_division_01(date_ref=None):
    return list(get_mapping_fund_names_division_01(date_ref=date_ref).keys())

def get_fund_codes_division_02(date_ref=None):
    return list(get_mapping_fund_names_division_02(date_ref=date_ref).keys())

def get_fund_codes_division_01_main(date_ref=None):
    fund_codes_division_01 = get_fund_codes_division_01(date_ref=date_ref)
    fund_codes = filter_fund_codes_by_main_filter(fund_codes_division_01, date_ref=date_ref)
    return fund_codes

def get_fund_codes_division_02_main(date_ref=None):
    fund_codes_division_02 = get_fund_codes_division_02(date_ref=date_ref)
    fund_codes = filter_fund_codes_by_main_filter(fund_codes_division_02, date_ref=date_ref)
    return fund_codes

def get_fund_codes_division_01_aum(date_ref=None):
    fund_codes_division_01 = get_fund_codes_division_01(date_ref=date_ref)
    fund_codes = filter_fund_codes_by_aum_filter(fund_codes_division_01, date_ref=date_ref)
    return fund_codes

def get_fund_codes_division_02_aum(date_ref=None):
    fund_codes_division_02 = get_fund_codes_division_02(date_ref=date_ref)
    fund_codes = filter_fund_codes_by_aum_filter(fund_codes_division_02, date_ref=date_ref)
    return fund_codes