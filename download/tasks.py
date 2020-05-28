from celery import shared_task
from celery_progress.backend import ProgressRecorder

# Task imports
import os, time, threading, queue, subprocess, urllib.request, re

def output_reader(proc, outq):
	for line in iter(proc.stdout.readline, b''):
		outq.put(line.decode('utf-8'))

@shared_task(bind=True)
def ProcessDownload(self, url):
	print('Task started')
	print(f'Downloading URL: {url}')
	progress_recorder = ProgressRecorder(self)

	command = f'wget {url}'

	### Code below is based on:
	### https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/

	proc = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	outq = queue.Queue()
	t = threading.Thread(target=output_reader, args=(proc, outq))
	t.start()

	try:
		time.sleep(0.2)

		# 5 consecutive empty lines = kill the process
		timeout_count = 5
		percentage = 0

		while True:
			try:
				line = outq.get(block=False)
				if '%' in line:
					percentage = re.findall('[0-9]{0,3}%', line)[0].replace('%','')
					print(percentage)
					progress_recorder.set_progress(int(percentage), 100, description="Downloading")

				timeout_count = 5
			except queue.Empty:
				print('could not get line from queue')
				timeout_count -= 1
				if timeout_count <= 0:
					break

			time.sleep(0.5)
	finally:
		# This is in 'finally' so that we can terminate the child if something
		# goes wrong
		proc.terminate()
		try:
			proc.wait(timeout=0.2)
			print('== subprocess exited with rc =', proc.returncode)
		except subprocess.TimeoutExpired:
			print('subprocess did not terminate in time')

	t.join()

	print('Task completed')
	if proc.returncode == 0:
		# Delete file
		try:
			folder = os.getcwd()
			filename = url.split('/')[-1]
			filepath = os.path.join(folder, filename)
			os.remove(filepath)
		except:
			print('Could not delete file')
		return 'File was successfully downloaded!'
	else:
		raise Exception('Download timed out, try again')
