# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/02/23 19:46
# Project:      Zibanu Django Project
# Module Name:  sum_dict
# Description:
# ****************************************************************

def zb_sum_dict(source_list: list, key: str, format_string: str = None):
    """
    Template tag to get a sum from a list of dictionary records.

    Parameters
    ----------
    source_list : List with dict records.
    key : Key string name to make the sum.
    format_string : Format to be used at render template.

    Returns
    -------
    f_sum: String with formatted result of sum operation.
    """
    sum_result = 0
    if isinstance(source_list, list):
        if len(source_list) > 0 and isinstance(source_list[0], dict):
            if key in source_list[0].keys():
                for record in source_list:
                    if record.get(key) is not None and (type(record.get(key)) == int or float):
                        sum_result += record.get(key)

    if format_string is not None:
        format_string = "{0:" + format_string + "}"
        f_sum = format_string.format(sum_result)
    else:
        f_sum = f"{sum_result}"
    return f_sum
