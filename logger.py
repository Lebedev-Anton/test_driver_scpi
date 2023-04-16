LOG_FORMAT = '%(asctime)s : %(levelname)s : %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'std_out': {'format': LOG_FORMAT},
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'std_out',
        },
        'file': {
            'formatter': 'std_out',
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filename': 'telemetry.log'
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG'
    },
}

