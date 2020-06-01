from django import forms

class DownloadForm(forms.Form):
	url = forms.CharField(max_length = 255, widget=forms.TextInput({
				'class':'form-control',
				'placeholder':'Enter URL to download...',
			}))