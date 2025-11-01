from django.shortcuts import render
from django.http import FileResponse
from .forms import UploadFileForm
from .utils import cleanup_excel
import os

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            cleaned_path = cleanup_excel(excel_file)
            response = FileResponse(open(cleaned_path, "rb"), as_attachment=True, filename="fisier_curatat.xlsx")
            os.remove(cleaned_path)  # opțional: ștergem fișierul temporar după descărcare
            return response
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
