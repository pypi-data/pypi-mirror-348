# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         7/03/2025 2:59 p. m.
# Project:      zibanu-django
# Module Name:  __init__.py
# Description:  
# ****************************************************************
from django import template

from .zb_concat import zb_concat
from .zb_divide import zb_divide
from .zb_multiply import zb_multiply
from .zb_query_filter import zb_query_filter
from .zb_replace import zb_replace
from .zb_static_uri import zb_static_uri
from .zb_subtotal_dict import zb_subtotal_dict
from .zb_sum_dict import zb_sum_dict

register = template.Library()

register.simple_tag(func=zb_concat)
register.filter(name="zb_divide", filter_func=zb_divide)
register.filter(name="zb_multiply", filter_func=zb_multiply)
register.simple_tag(func=zb_query_filter)
register.filter(name="zb_replace", filter_func=zb_replace)
register.tag(name='zb_static_uri', compile_function=zb_static_uri)
register.simple_tag(func=zb_subtotal_dict)
register.simple_tag(func=zb_sum_dict)
