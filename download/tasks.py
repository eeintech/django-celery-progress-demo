from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task

# Celery-progress
from celery_progress.backend import ProgressRecorder

# Task imports
import os, time, subprocess, re

@shared_task(bind=True)
def ProcessDownload(self, url):
	print('Download: Task started')

	# Build command
	command = f'wget {url}'

	# Start download process
	download = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	update_progress(self, download)

	download.terminate()
	try:
		download.wait(timeout=0.2)
		print(f'Subprocess terminated [Code {download.returncode}]')
	except subprocess.TimeoutExpired:
			print('Subprocess did not terminate on time')

	if download.returncode == 0:
		# Delete file
		try:
			folder = os.getcwd()
			filename = url.split('/')[-1]
			filepath = os.path.join(folder, filename)
			os.remove(filepath)
		except:
			print('Could not delete file')
		return 'Download was successfull!'
	else:
		raise Exception('Download timed out, try again')

def update_progress(self, proc):
	progress_recorder = ProgressRecorder(self)

	while True:
		line = proc.stdout.readline()

		if line == b'':
			break

		linestr = line.decode("utf-8")
		if '%' in linestr:
			percentage = re.findall('[0-9]{0,3}%', linestr)[0].replace('%','')
			print(percentage)
			progress_recorder.set_progress(int(percentage), 100, description="Downloading")
		else:
			print(linestr)

		time.sleep(0.5)