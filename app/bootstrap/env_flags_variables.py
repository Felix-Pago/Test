ENV_FLAGS_VARIABLES = [
    {
        'name': 'env',
        'type': str,
        'description': 'Environment where the application will run'
    },
    {
        'name': 'config_path',
        'type': str,
        'description': 'Configuration relative files path'
    },
    {
        'name': 'google_application_credentials',
        'type': str,
        'description': 'GCP application credentials relative file path',
        'optional': True
    },
    {
        'name': 'reload',
        'type': bool,
        'description': 'FastAPI Hot Reload Flag',
        'default': False
    },
]
