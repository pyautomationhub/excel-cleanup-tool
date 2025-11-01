from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Import your messy excel file (.xlsx)")
