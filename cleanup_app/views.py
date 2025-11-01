from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from .forms import UploadFileForm
from .utils import cleanup_excel
import os

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            try:
                cleaned_path = cleanup_excel(excel_file)
                # Save file path in session for later download
                request.session['cleaned_file_path'] = cleaned_path
                return redirect('success')
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                form = UploadFileForm()
        else:
            messages.error(request, "Please select a valid Excel file (.xlsx)")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def success(request):
    return render(request, "success.html")

def download_file(request):
    if 'cleaned_file_path' in request.session:
        cleaned_path = request.session['cleaned_file_path']
        if os.path.exists(cleaned_path):
            try:
                file_handle = open(cleaned_path, "rb")
                response = FileResponse(file_handle, as_attachment=True, filename="cleaned_file.xlsx")
                # Remove path from session
                del request.session['cleaned_file_path']
                
                # Add callback to delete file after response is sent
                def cleanup_file():
                    try:
                        file_handle.close()
                        if os.path.exists(cleaned_path):
                            os.remove(cleaned_path)
                    except:
                        pass
                
                # Use response.close for cleanup
                original_close = response.close
                def close_with_cleanup():
                    original_close()
                    cleanup_file()
                response.close = close_with_cleanup
                
                return response
            except Exception as e:
                # In case of error, try to delete the file
                try:
                    if os.path.exists(cleaned_path):
                        os.remove(cleaned_path)
                except:
                    pass
                del request.session['cleaned_file_path']
                messages.error(request, f"Error downloading file: {str(e)}")
                return redirect('upload_file')
        else:
            del request.session['cleaned_file_path']
    return redirect('upload_file')
