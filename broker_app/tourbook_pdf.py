from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import TourBook
from django.shortcuts import get_object_or_404, render


@login_required
def tourbook_pdf_view(request, pk):
    tour_book = get_object_or_404(TourBook, pk=pk)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tourbook{}.pdf"'.format(pk)

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 700, "Hello world. You printed this for tour book {}".format(tour_book.tour_title))

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
