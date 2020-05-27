from django import forms

class DownloadForm(forms.Form):
	url = forms.CharField(max_length = 255)