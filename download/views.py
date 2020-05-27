from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from .forms import DownloadForm
from .tasks import ProcessDownload

def demo_view(request):
	if request.method == 'POST':
		form = DownloadForm(request.POST)

		if form.is_valid():
			url = form.cleaned_data['url']
			print(f'Downloading: {url}')
			# Create Task
			task = ProcessDownload.delay(url)
			task_id = task.task_id
			print (f'Celery Task ID: {task_id}')

			return render(request, 'progress.html', {'form': form, 'task_id': task_id})
	else:
		form = DownloadForm()

		return render(request, 'progress.html', {'form': form})

@csrf_exempt
@never_cache
def success_view(request, task_id):
	print(f'Success View for [{task_id}]')
	if request.method == 'POST':
		response_json = request.POST
		response_json = json.dumps(response_json)
		data = json.loads(response_json)
		payload = json.loads(data['data'])

	if data:
		print(f'Processing success data: {data}')

	return render(request, 'progress.html', {'task_id': task_id})