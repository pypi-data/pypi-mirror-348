from django.utils.deprecation import MiddlewareMixin

from django_post_api.errors import MyError
from django_post_api.log import default_logger, debug_logger
from django_post_api.returns import error_return


class ErrorMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        debug_logger.exception(exception)
        if isinstance(exception, MyError):
            err_msg = getattr(exception, "err_msg", "")
            status_code = getattr(exception, "status_code", 500)
        else:
            default_logger.exception(exception)
            status_code = 500
            err_type = exception.__class__.__name__
            err_msg = f"{err_type}: {';'.join([str(i) for i in exception.args])}"

        return error_return(err_msg, status_code)
