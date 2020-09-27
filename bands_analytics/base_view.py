import functools
from django.db import transaction
from django.http import HttpResponse, JsonResponse

JSON_DUMPS_PARAMS = {
    'indent': 2,
    'ensure_ascii': False
}


def ret(result, status=200):
    if isinstance(result, (dict, list)):
        return JsonResponse(
            result,
            status=status,
            safe=not isinstance(result, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )
    else:
        return HttpResponse(
            result,
            status=status
        )


def error_response(exception):
    result = f'Something gone wrong. Try again later.<br>Details: {str(exception)}'
    return ret(result, status=500)


def base_view(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                res = func(request, *args, **kwargs)
                if isinstance(res, HttpResponse):
                    return res
                else:
                    return ret(res)
        except Exception as e:
            return error_response(e)

    return inner
