from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class DecimalJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def base_return(return_data, status=200):
    return JsonResponse(return_data, status=status, encoder=DecimalJSONEncoder)


def success_return(data=None, status=200, **kwargs):
    if data is None:
        data = {}
    return_data = {
        "err_msg": "ok",
        "data": data,
    }
    if kwargs:
        return_data.update(**kwargs)
    return base_return(return_data, status=status)


def error_return(errmsg, status=500):
    return_data = {
        "err_msg": errmsg,
        "data": None,
    }
    return base_return(return_data, status=status)
