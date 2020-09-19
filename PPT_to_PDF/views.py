__author__ = 'Lachlan Attwood'

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
import convertapi
import subprocess as sp
import os


def validate_file(file, acceptable_extensions, max_size: int) -> None:
    """
    Modified:       14/09/2020
    Description:    Performs validation on a given file, checking that it does
                    not exceed the acceptable file size and contains the correct
                    file extension.
    :pre:            file such that it exists
    :post:           Raises Incorrect Extension if the extention is incorrect
                    Raises Incorrect Size if the the size exceeds the given limit
    """
    # Checks user-defined file extension
    if file.name.split('.')[-1] not in acceptable_extensions:
        raise Exception('Incorrect Extension')

    # Checks the file size is within acceptable limits
    if file.size > max_size * 10 ** 6:
        raise Exception('Incorrect Extension')


def convert_ppt_to_pdf(file_name: str):
    """
    Converts from a powerpoint file (.ppt or .pptx) into a pdf file using LibreOffice
    running through the servers commandline.
    """
    path = os.path.abspath('') + '/media/' + file_name
    output = os.path.abspath('') + '/media/'
    sp.call(['libreoffice', '--headless', '--convert-to', 'pdf', path, '--outdir', output])  # Converts .ppt to .pdf
    os.remove(path)


def myView(request):
    """
    Uploads a PowerPoint file with a max size of 30MB and an extension of .ppt

    :pre: document form is not empty
    :pre: the document is less than 30MB and has a .ppt or .pptx extension
    """
    # Uploads the users file
    if request.method == 'POST':
        # Handles MultiValueDictKeyError for when the file upload path is empty (pre-condition)
        try:
            uploaded_file = request.FILES['document']
        except MultiValueDictKeyError:
            print('\n' + '[ERROR] An empty file path was submitted' + '\n')
            return render(request, 'PPT_to_PDF.html', {})

        print(uploaded_file.name)
        validate_file(uploaded_file, ['ppt', 'pptx'], 30)  # Validates the file

        # Stores the file in /media/[file name].pdf
        fs = FileSystemStorage()
        try:
            name = fs.save(uploaded_file.name, uploaded_file)
        except MultiValueDictKeyError:
            print('There has been and error')
        convert_ppt_to_pdf(name)

        # Return pdf file
        pdf_location = '/media/' + name.strip('.pptx') + '.pdf'
        return redirect(pdf_location)  # Opens the pdf in the clients browser
    return render(request, 'PPT_to_PDF.html', {})  # Renders the page
