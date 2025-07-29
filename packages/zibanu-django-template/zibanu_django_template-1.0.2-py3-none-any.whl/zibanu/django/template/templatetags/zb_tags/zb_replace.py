# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         28/03/2025 8:42 a. m.
# Project:      zibanu-django
# Module Name:  replace
# Description:  
# ****************************************************************

def zb_replace(value, arg):
    """
    Replacing filter.
    Use `{{ "aaa"|replace:"a|b" }}`
    :param value: String to modify
    :param arg: String to replace.
    :return: string
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)
