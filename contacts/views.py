from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from contacts.models import Contact
import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from contacts.models import Contact
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id= request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message,
                          user_id=user_id)

        contact.save()

        # Send mail
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
            'y.femi@gmail.com',
            [realtor_email, 'frankolayemi@gmail.com'], # email address here
            fail_silently=False
        )


        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)
    
def download_enquiry(request):
    # Get all the contacts from the database
    contacts = Contact.objects.all()

    # Generate a CSV file
    df = pd.DataFrame(list(contacts.values()))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enquiry_details.csv"'
    df.to_csv(path_or_buf=response, index=False)

    # Alternatively, generate a PDF file
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="enquiry_details.pdf"'
    # p = canvas.Canvas(response)
    # for i, contact in enumerate(contacts):
    #     p.drawString(100, 700 - (i * 50), f"Listing: {contact.listing}")
    #     p.drawString(100, 700 - (i * 50) - 20, f"Name: {contact.name}")
    #     p.drawString(100, 700 - (i * 50) - 40, f"Email: {contact.email}")
    #     p.drawString(100, 700 - (i * 50) - 60, f"Phone: {contact.phone}")
    #     p.drawString(100, 700 - (i * 50) - 80, f"Message: {contact.message}")
    #     p.drawString(100, 700 - (i * 50) - 100, f"Contact Date: {contact.contact_date}")
    #     p.drawString(100, 700 - (i * 50) - 120, f"User ID: {contact.user_id}")
    # p.showPage()
    # p.save()

    return response

@login_required
def download_enquiry(request):
    # Retrieve all enquiry details from the database
    enquiry_details = Contact.objects.all().values_list('id', 'listing', 'name', 'email', 'phone', 'contact_date')

    # Create a Pandas dataframe from the enquiry details
    df_enquiry_details = pd.DataFrame(enquiry_details, columns=['ID', 'Listing', 'Name', 'Email', 'Phone', 'Contact Date'])

    # Create a response object with the PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enquiry_details.pdf"'

    # Create the PDF document and add the table of enquiry details
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    table_data = [df_enquiry_details.columns.values.tolist()] + df_enquiry_details.values.tolist()
    table = Table(table_data, colWidths=[1.5 * inch, 2.5 * inch, 2 * inch, 2.5 * inch, 2 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    # Build the PDF document and return the response object
    doc.build(elements)
    return response
