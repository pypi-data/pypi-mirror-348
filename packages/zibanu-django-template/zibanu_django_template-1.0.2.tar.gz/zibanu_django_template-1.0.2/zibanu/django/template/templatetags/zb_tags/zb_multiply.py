# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         7/03/2025 4:08 p. m.
# Project:      zibanu-django
# Module Name:  zb_multiply
# Description:  
# ****************************************************************

def zb_multiply(value, arg):
    """
    Multiplication Operation.
    :param value: factor one.
    :param arg: factor two.
    :return: result.
    """
    try:
        return value * arg
    except TypeError:
        return None
