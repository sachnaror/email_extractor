import re
import csv
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from io import StringIO, BytesIO

# Regular expression to find email addresses
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

def extract_emails(file_content):
    # Extract emails using regex and return a unique list
    emails = re.findall(EMAIL_REGEX, file_content)
    return sorted(set(emails))  # Removes duplicates and sorts them

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_extension = file.name.split('.')[-1].lower()

            # Read file content based on its type
            if file_extension in ['txt']:
                file_content = file.read().decode('utf-8')
            elif file_extension in ['csv']:
                file_content = file.read().decode('utf-8')
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file)
                file_content = df.to_string()

            # Extract emails
            email_list = extract_emails(file_content)

            # Provide options to download as text, csv, or xls
            context = {
                'emails': email_list
            }
            return render(request, 'extractor/results.html', context)

    else:
        form = FileUploadForm()

    return render(request, 'extractor/upload.html', {'form': form})

# Helper functions for download options
def download_as_txt(request):
    emails = request.GET.getlist('emails')
    response = HttpResponse("\n".join(emails), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="emails.txt"'
    return response

def download_as_csv(request):
    emails = request.GET.getlist('emails')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'
    writer = csv.writer(response)
    for email in emails:
        writer.writerow([email])
    return response

def download_as_xls(request):
    emails = request.GET.getlist('emails')
    df = pd.DataFrame(emails, columns=['Emails'])
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="emails.xlsx"'
    df.to_excel(response, index=False)
    return response
