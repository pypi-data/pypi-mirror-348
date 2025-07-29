# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         7/03/2025 3:44 p. m.
# Project:      zibanu-django
# Module Name:  zb_query_filter
# Description:  
# ****************************************************************
from django.db.models import QuerySet


def zb_query_filter(queryset: QuerySet, **kwargs):
    """
    Filter a queryset
    :param queryset:  type argument queryset.
    :param kwargs: Arguments for which the queryset will be filtered.
    :return: queryset.
    """
    order = kwargs.pop("order", None)
    try:
        qs = queryset.filter(**kwargs)
        if order is not None:
            qs = qs.order_by(order)
    except AttributeError:
        qs = None
    return qs
