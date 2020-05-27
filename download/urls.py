from django.urls import path, include

from .views import demo_view, success_view

app_name = 'download'

urlpatterns = [
	# Default view with empty form
	path('', demo_view, name='demo'),
	# Success view
	path('<str:task_id>/', success_view, name='success'),
]