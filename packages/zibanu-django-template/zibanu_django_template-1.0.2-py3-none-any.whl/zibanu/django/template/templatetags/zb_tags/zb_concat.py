# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         7/02/23 18:56
# Project:      Zibanu Django Project
# Module Name:  string_concat
# Description:
# ****************************************************************

def zb_concat(first_arg, *args):
    """
    Simple tag to concatenate one string with strings tuple.
    :param first_arg: Base string to concatenate
    :param args: arguments tuple
    :return: Concatenated string
    """
    concat = str(first_arg)
    for arg in args:
        concat += str(arg)
    return concat
