from django.apps import AppConfig
from django.utils.autoreload import restart_with_reloader
import threading


class AppConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'App'

	# def ready(self):
	# 	from .marejesho_scheduler import start
	# 	import os
	# 	if os.environ.get('RUN_MAIN', None) != 'true':  # Avoid double execution in debug mode
	# 		start()

	# def ready(self):
 #        from .scheduler import start
 #        start()