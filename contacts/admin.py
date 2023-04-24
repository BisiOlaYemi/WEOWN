from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Contact

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date', 'download_button')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 25

    def download_button(self, obj):
        url = reverse('download_enquiry')
        return format_html('<a href="{}?id={}">Download</a>', url, obj.id)

    download_button.short_description = 'Download'

    def download_enquiry(self, request):
        contact_id = request.GET.get('id')
        if not contact_id:
            return HttpResponse('Invalid request')
        contact = Contact.objects.filter(id=contact_id).first()
        if not contact:
            return HttpResponse('Contact not found')
        enquiry_details = [(contact.id, contact.listing, contact.name, contact.email, contact.phone, contact.contact_date)]
        df_enquiry_details = pd.DataFrame(enquiry_details, columns=['ID', 'Listing', 'Name', 'Email', 'Phone', 'Contact Date'])
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="enquiry_{contact.id}.pdf"'
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
        doc.build(elements)
        return response

    download_enquiry.allowed_permissions = ('view',)
    download_enquiry.url_name = 'download_enquiry'
    download_enquiry.description = 'Download enquiry as PDF'

admin.site.register(Contact, ContactAdmin)

