from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response


class ErrorJSONType(type):
    def __getattr__(self, item):
        error_code = getattr(ErrorCode, item)
        return {
            'code': error_code[0],
            'message': error_code[1]
        }


class ErrorCode:
    DATA_FIELD_NOT_FOUND = ('data field not found', 1001)
    PRODUCT_COUNT_INVALID = ('product count is not valid', 1002)
    PRODUCT_INVALID_ORDER_TYPE = ('this product has not this order type', 1003)

    PRODUCT_NOT_FOUND = ('product not found', 2001)
    PRODUCT_ORDER_NOT_FOUND = ('product order type not found', 2002)
    CONSUME_LOCATION_NOT_FOUND = ('consume location not found', 2003)

    NOT_ITEM_IN_ORDER = ('No items in order', 3001)
    CHANGE_NOT_WAITING_ORDER = ('only can change waiting order', 3002)
    NOT_FOR_YOU = ('this order not for you', 3003)
    CANCEL_NOT_WAITING_ORDER = ('only can cancel waiting order', 3002)

    INVALID_DATA = ('invalid data', 9000)

    UNKNOWN = (9999, 'Unknown error')

    class dict(metaclass=ErrorJSONType):
        pass


def count(obj):
    if isinstance(obj, list) or isinstance(obj, QuerySet):
        return len(obj)
    elif isinstance(obj, str) or isinstance(obj, dict) or isinstance(obj, int) or isinstance(obj, bool):
        return 1
    elif obj is None:
        return 0
    else:
        raise ValueError("Can not count items of %s" % type(obj))


def ok(data=None, result_number=None, reason=None):
    if reason:
        return Response(dict(message=data or reason[1], error=True, result_number=reason[0]))
    if not result_number:
        result_number = count(data)
    return Response(dict(message=data, result_number=result_number, error=False))


def created(data=None, result_number=None, reason=None):
    if reason:
        return Response(dict(message=data or reason[1], error=True, result_number=reason[0]),
                        status=status.HTTP_201_CREATED)
    if not result_number:
        result_number = count(data)
    return Response(dict(message=data, error=False, result_number=result_number), status=status.HTTP_201_CREATED)


def accepted(data=None, result_number=None, reason=None):
    if reason:
        return Response(dict(message=data or reason[1], error=True, result_number=reason[0]),
                        status=status.HTTP_202_ACCEPTED)
    if not result_number:
        result_number = count(data)
    return Response(dict(message=data, error=False, result_number=result_number), status=status.HTTP_202_ACCEPTED)


def bad_request(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_400_BAD_REQUEST)


def unauthorized(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_401_UNAUTHORIZED)


def forbidden(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_403_FORBIDDEN)


def not_found(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_404_NOT_FOUND)


def not_acceptable(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_406_NOT_ACCEPTABLE)


def conflict(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_409_CONFLICT)


def internal_server_error(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bad_gateway(reason, message=None):
    return Response(dict(message=message or reason[1], error=True, result_number=reason[0]),
                    status=status.HTTP_502_BAD_GATEWAY)
