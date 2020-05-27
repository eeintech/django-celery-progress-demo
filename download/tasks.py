from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time

@shared_task(bind=True)
def ProcessDownload(self, url):
	print('Task started')
	print(f'Downloading URL: {url}')

	### TEST ONLY
	progress_recorder = ProgressRecorder(self)
	result = 0
	print('Start')
	for i in range(5):
		time.sleep(1)
		result += i
		progress_recorder.set_progress(i + 1, 5, description="Downloading")
		print(i)
	print('End')
	return i