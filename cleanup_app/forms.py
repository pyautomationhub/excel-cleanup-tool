from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Upload your Excel file (.xlsx)",
        help_text="The tool will automatically clean: multiple spaces, normalize numbers, detect and convert dates, remove duplicates."
    )
