import re
import pdb
from TechnicalAnalysis.indicators import TA

CHARACTER_NUMBER_PATTERN = re.compile("([a-zA-Z]+)([0-9]+)")
AVAILABLE_TECHNICAL_INDICATORS = [k for k in TA.__dict__.keys() if k[0] not in "_"]


def get_strategies_from_text(input_text):
    strategies_info_list = []
    strategies_list = input_text.split('\n')
    for each_strategy in strategies_list:
        this_info_dict = {}
        indicator_string_1, relation, indicator_string_2, move = each_strategy.split()
        this_info_dict = {
                            'indicator1_info': indicator_string_splitter(indicator_string_1),
                            'relation': relation_identifier(relation),
                            'indicator2_info': indicator_string_splitter(indicator_string_2),
                            'move_info': move
                        }
        strategies_info_list.append(this_info_dict)
    return strategies_info_list


def indicator_string_splitter(input_string):
    print("input_string", input_string)
    if input_string.isnumeric():
        return {"threshold": input_string}
    if input_string.isalpha():
        return {"indicator": indicator_identifier(input_string)}
    if ("(" in input_string) and (")" in input_string):
        tech_indicator, rest_string = input_string.split("(")
        arg_list = [each_arg.strip() for each_arg in rest_string.split(")")[0].split(',')]
    else:
        [tech_indicator, window_size] = CHARACTER_NUMBER_PATTERN.match(input_string).groups()
        arg_list = [window_size]
    return {"indicator": indicator_identifier(tech_indicator), "arguments": arg_list}


def indicator_identifier(input_string):
    if input_string.upper() in AVAILABLE_TECHNICAL_INDICATORS:
        # pdb.set_trace()
        return f"TA.{input_string.upper()}"
    raise NotImplementedError(f"This Indicator is not implemented {input_string}")


def relation_identifier(input_string):
    if input_string.upper().strip() == 'CROSSOVER':
            return 'CROSSOVER'
    elif input_string in ['>', '<', '=', '>=', '<=']:
        return input_string
    else:
        raise NotImplementedError(f"The relation is not implemented {input_string}")
