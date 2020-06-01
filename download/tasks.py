from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task

# Celery-progress
from celery_progress.backend import ProgressRecorder

# Task imports
import os, time, subprocess, re

@shared_task(bind=True)
def ProcessDownload(self, url):
	# Announce new task (celery worker output)
	print('Download: Task started')

	# Saved downloaded file with this name
	filename = 'file_download'
	# Wget command (5 seconds timeout)
	command = f'wget {url} -T 5 -O {filename}'

	# Start download process
	download = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# Read each output line and update progress
	update_progress(self, download)

	# Make sure wget process is terminated
	download.terminate()
	try:
		# Wait 100ms
		download.wait(timeout=0.1)
		# Print return code (celery worker output)
		print(f'Subprocess terminated [Code {download.returncode}]')
	except subprocess.TimeoutExpired:
		# Process was not terminated in the timeout period
		print('Subprocess did not terminate on time')

	# Check if process was successfully completed (return code = 0)
	if download.returncode == 0:
		# Delete file
		try:
			folder = os.getcwd()
			filepath = os.path.join(folder, filename)
			os.remove(filepath)
		except:
			print('Could not delete file')
		# Return message to update task result
		return 'Download was successful!'
	else:
		# Raise exception to indicate something wrong with task
		raise Exception('Download timed out, try again')

def update_progress(self, proc):
	# Create progress recorder instance
	progress_recorder = ProgressRecorder(self)

	while True:
		# Read wget process output line-by-line
		line = proc.stdout.readline()

		# If line is empty: break loop (wget process completed)
		if line == b'':
			break

		linestr = line.decode('utf-8')
		if '%' in linestr:
			# Find percentage value using regex
			percentage = re.findall('[0-9]{0,3}%', linestr)[0].replace('%','')
			# Print percentage value (celery worker output)
			print(percentage)
			# Build description
			progress_description = 'Downloading (' + str(percentage) + '%)'
			# Update progress recorder
			progress_recorder.set_progress(int(percentage), 100, description=progress_description)
		else:
			# Print line
			print(linestr)
			
		# Sleep for 100ms
		time.sleep(0.1)
		