import os
import sys
import uuid
import time
import logging
from django.utils.deprecation import MiddlewareMixin

def get_logging_config():
    """
    FAANG-style logging configuration - concise and meaningful
    """
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            },
            'clean_console': {
                'format': '{levelname} {asctime} {name} | {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'clean_console' if debug else 'json',
                'stream': sys.stdout,
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'loggers': {
            'django.server': {  # Keep Django's built-in request logs
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'validator': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

class RequestLoggingMiddleware(MiddlewareMixin):
    """FAANG-style request logging - ONE log per request with all context"""
    
    def process_request(self, request):
        request.start_time = time.time()
        request.request_id = str(uuid.uuid4())
        return None

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        logger = logging.getLogger('validator')
        
        logger.info(
            f"HTTP {request.method} {request.path} {response.status_code} | "
            f"{round(duration * 1000, 2)}ms | {getattr(request, 'request_id', '-')}"
        )
        
        response['X-Request-ID'] = getattr(request, 'request_id', '-')
        return response