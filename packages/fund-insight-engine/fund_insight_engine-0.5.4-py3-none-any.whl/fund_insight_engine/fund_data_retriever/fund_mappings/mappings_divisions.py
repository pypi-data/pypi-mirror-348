from fund_insight_engine.fund_data_retriever.fund_codes.divisions import get_mapping_fund_names_by_division
from .mapping_consts import KEYWORDS_FOR_MAIN
from .mapping_utils import exclude_keywords_from_mapping

def get_mapping_fund_names_division_01(date_ref=None, keywords_to_exclude=None, option_main=True):
    mapping_fund_names_division_01 = get_mapping_fund_names_by_division('division_01', date_ref=date_ref)
    if option_main:
        mapping_fund_names_division_01 = exclude_keywords_from_mapping(mapping_fund_names_division_01, KEYWORDS_FOR_MAIN)
    if keywords_to_exclude:
        mapping_fund_names_division_01 = exclude_keywords_from_mapping(mapping_fund_names_division_01, keywords_to_exclude)
    return mapping_fund_names_division_01

def get_mapping_fund_names_division_02(date_ref=None, keywords_to_exclude=None):
    mapping_fund_names_division_02 = get_mapping_fund_names_by_division('division_02', date_ref=date_ref)
    mapping_fund_names_division_02 = exclude_keywords_from_mapping(mapping_fund_names_division_02, KEYWORDS_FOR_MAIN)
    if keywords_to_exclude:
        mapping_fund_names_division_02 = exclude_keywords_from_mapping(mapping_fund_names_division_02, keywords_to_exclude)
    return mapping_fund_names_division_02