# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         7/03/2025 3:59 p. m.
# Project:      zibanu-django
# Module Name:  zb_divide
# Description:  
# ****************************************************************

def zb_divide(value, arg):
    """
    Division Operation.
    :param value: dividend int.
    :param arg: divisor int.
    :return: result.
    """
    try:
        return value / arg
    except (ValueError, ZeroDivisionError, TypeError):
        return None
