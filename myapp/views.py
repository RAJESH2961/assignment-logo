import os
import tempfile
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def show_form(request):
    return render(request, 'form.html')

def generate_pdf(request):
    if request.method == 'POST' or request.GET.get('action') == 'preview':
        name = request.POST.get('name', '')
        rollnumber = request.POST.get('rollnumber', '')
        assignment = request.POST.get('assignment', '')
        subject_name = request.POST.get('subject_name', '')
        submission_date = request.POST.get('submission_date', '')
        submission_to = request.POST.get('submission_to', '')
        image = request.FILES.get('image', None)

        # Create a HttpResponse object with PDF content type
        response = HttpResponse(content_type='application/pdf')

        # Determine if the user wants to preview or download
        if request.GET.get('action') == 'preview':
            response['Content-Disposition'] = 'inline; filename="assignment_submission.pdf"'
        # Use f-string to include subject_name in the filename
            response['Content-Disposition'] = f'attachment; filename="assignment-{subject_name}.pdf"'


        # Create the PDF object using canvas and A4 size
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Add title
        pdf.setFont("Helvetica-Bold", 18)
        # pdf.drawString(100, height - 50, "Assignment Submission Form")

        # Add form data to the PDF
        pdf.setFont("Helvetica", 16)
        pdf.drawString(100, height - 380, f"Name: {name}")
        pdf.drawString(100, height - 420, f"Roll Number: {rollnumber}")
        pdf.drawString(100, height - 460, f"Assignment Number: {assignment}")
        pdf.drawString(100, height - 500, f"Subject Name: {subject_name}")
        pdf.drawString(100, height - 540, f"Submission Date: {submission_date}")
        pdf.drawString(100, height - 580, f"Submitted To: {submission_to}")

        # Add image to the PDF if available
        if image:
            # Create a temporary file to save the uploaded image
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            for chunk in image.chunks():
                temp_file.write(chunk)
            temp_file.close()

            # Add the image to the PDF
            # pdf.drawImage(temp_file.name, 180, height - 230, width=240, height=150)  # Adjust size and position as needed
            pdf.drawImage(temp_file.name, (width - 240) / 2, height - 230, width=240, height=150)  # Centered image


            # Clean up the temporary file
            os.remove(temp_file.name)

        # Close the PDF object
        pdf.showPage()
        pdf.save()

        # Get PDF data and write to response
        pdf_data = buffer.getvalue()
        buffer.close()
        response.write(pdf_data)

        return response
    else:
        return render(request, 'form.html')
