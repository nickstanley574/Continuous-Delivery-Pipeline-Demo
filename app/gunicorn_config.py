# gunicorn_config.py
workers = 4
timeout = 15
bind = "0.0.0.0:8080"
accesslog = "-"  # Log to stdout
