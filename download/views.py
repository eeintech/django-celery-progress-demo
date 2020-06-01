from django.shortcuts import render

from .forms import DownloadForm
from .tasks import ProcessDownload

def demo_view(request):
	# If method is POST, process form data and start task
	if request.method == 'POST':
		# Get form instance
		form = DownloadForm(request.POST)

		if form.is_valid():
			# Retrieve URL from form data
			url = form.cleaned_data['url']

			print(f'Downloading: {url}')
			# Create Task
			download_task = ProcessDownload.delay(url)
			# Get ID
			task_id = download_task.task_id
			# Print Task ID
			print (f'Celery Task ID: {task_id}')

			# Return demo view with Task ID
			return render(request, 'progress.html', {'form': form, 'task_id': task_id})
		else:
			# Return demo view
			return render(request, 'progress.html', {'form': form})
	else:
		# Get form instance
		form = DownloadForm()
		# Return demo view
		return render(request, 'progress.html', {'form': form})
