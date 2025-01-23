import random
import datetime
from datetime import date
import names
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
import subprocess
import io
from PIL import Image
import os
import base64

# Constants
GITHUB_REPO_URL = "https://github.com/hadzicni/SiTra-QR-Code-Generator-UHBS"

BLOOD_PRODUCTS = {
    "ERYTHROCYTE_CONCENTRATE": "EK",
    "FRESH_FROZEN_PLASMA": "PL",
    "FRESH_FROZEN_PLASMA_THAWED": "PL",
    "THROMBOCYTE_CONCENTRATE": "TK",
    "SPECIFIC_THROMTOCYTE_CONCENTRATE": "TK",
    "APHERESIS_THROMBOCYTE_CONCENTRATE": "TK"
}

BLOOD_GROUPS = [
    "0neg|0neg|", "0pos|0pos|", "Bneg|Bneg|", "Bpos|Bpos|",
    "Aneg|Aneg|", "Apos|Apos|", "ABneg|ABneg|", "ABpos|ABpos|"
]

STATION_IDS = [
    "4050", "4100", "4120", "4130", "4140", "4150", "4161", "4170",
    "4180", "4310", "4410", "4411", "4600", "4610", "4620", "4640",
    "4650", "4660", "4670", "4690", "4700", "4710", "4750", "4770",
    "4790", "4800", "4920", "5010", "5040", "5810", "7777"
]

# Embedded USB logo
USB_LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAACgAAAAIKCAYAAADvIBbZAAAABmJLR0QA/wD/AP+gvaeTAAAgAElEQVR4nOzdeZwcdZ3/8fenuicnN8RIMtNVfYRBg4DEAxA0gAqs16p4sIKueK2K97nrD7xwPXbVVcRzFQS8V8RrFa9FFtRFwAODAn1U9wwIch8hk0x3fX5/TAKIAXJU"

def get_logo_image():
    """Get the USB logo as a PIL Image object."""
    logo_data = base64.b64decode(USB_LOGO_BASE64)
    return Image.open(BytesIO(logo_data))

def generate_random_number(length):
    numbers = random.sample(range(0, 9), length)
    return ''.join(map(str, numbers))

def generate_random_birthdate():
    year = random.randint(1950, 2003)
    month = random.randint(1, 12)
    
    if month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        max_day = 29 if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) else 28
    else:
        max_day = 31
        
    day = random.randint(1, max_day)
    return datetime.date(year, month, day)

def generate_patient_data(first_name=None, last_name=None, blood_product=None, blood_group=None, station_id=None, birth_date=None, expiry_days=7):
    """Generate random patient data."""
    today = datetime.date.today()
    
    # Generate random values for None inputs
    data = {
        'patient_id': generate_random_number(8),
        'visit_id': generate_random_number(8),
        'charge_date': today.strftime("%Y%m%d"),
        'charge_id': generate_random_number(4),
        'product_id': generate_random_number(8),
        'blood_expiration': (today + datetime.timedelta(days=expiry_days)).strftime("%d.%m.%Y"),
        'blues_id': generate_random_number(6),
        'administration_id': generate_random_number(6),
        'blood_product': blood_product if blood_product else random.choice(list(BLOOD_PRODUCTS.keys())),
        'blood_group': blood_group if blood_group else random.choice(BLOOD_GROUPS),
        'station_id': station_id if station_id else random.choice(STATION_IDS),
        'last_name': last_name if last_name else names.get_last_name(),
        'first_name': first_name if first_name else names.get_first_name(),
        'birth_date': birth_date if birth_date else generate_random_birthdate(),
        'expiry_days': expiry_days
    }
    return data

def generate_qr_code(content):
    """Generate a single QR code."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def generate_content_strings(data):
    blood_product_type = BLOOD_PRODUCTS[data['blood_product']]
    
    content1 = f"P|{data['patient_id']}|00{data['visit_id']}|{blood_product_type}|H00{data['charge_date']}{data['charge_id']}|E{data['product_id']}|{data['blood_group']}{data['blood_expiration']}|{data['blues_id']}"
    content2 = f"K^{data['patient_id']}^{data['administration_id']}^{data['blood_product']}^TEST-{data['last_name']}^TEST-{data['first_name']}^{data['birth_date'].strftime('%d.%m.%Y')}^{data['station_id']}"
    content3 = data['visit_id']
    
    return content1, content2, content3

def generate_qr_codes(first_name=None, last_name=None, blood_product=None, blood_group=None, station_id=None, birth_date=None, expiry_days=7):
    """Generate QR codes without creating a PDF."""
    # Generate patient data
    patient_data = generate_patient_data(first_name, last_name, blood_product, blood_group, station_id, birth_date, expiry_days)
    content1, content2, content3 = generate_content_strings(patient_data)
    contents = [content1, content2, content3]
    
    # Create QR codes
    qr_codes = []
    
    # Generate QR codes for each content
    for content in contents:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(content)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        qr_codes.append(img_byte_arr)
    
    return qr_codes

def generate_pdf_from_qrcodes(qr_codes, patient_data):
    """Generate a PDF with QR codes."""
    # Create PDF
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # QR code parameters
    x, y = 50, 700
    qr_size = 100
    text_x_offset = 50
    font_size = 8
    text_max_width = 400
    
    # Save QR codes to temporary files and add to PDF
    titles = ["Bloodproduct", "Meona Code", "Patient wristband (Fall-ID)"]
    contents = generate_content_strings(patient_data)
    y_positions = [y - 120, y - 320, y - 520]
    
    for i, (qr_code, title, content, y_pos) in enumerate(zip(qr_codes, titles, contents, y_positions)):
        # Save temporary file
        temp_file = f"temp_qr_{i}.png"
        with open(temp_file, "wb") as f:
            f.write(qr_code)
        
        # Add QR code and text to PDF
        pdf.drawInlineImage(temp_file, x, y_pos, width=qr_size, height=qr_size)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x + qr_size + 20, y_pos + 20, title)
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(x + qr_size + 20, y_pos - 5, content[:text_max_width])
        
        # Clean up temp file
        os.remove(temp_file)
    
    # Add logo
    logo_path = "usblogo.png"
    logo_width = 198
    logo_height = 41
    logo_x = letter[0] - logo_width - 20
    logo_y = letter[1] - logo_height - 20
    pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")
    
    # Add title
    title = "SiTra Test QR-Codes UHBS"
    title_x = 40
    title_y = letter[1] - 40
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, title_y, title)
    
    # Add creation time
    aktuelle_zeit = datetime.datetime.now()
    formatierte_zeit = aktuelle_zeit.strftime("%d.%m.%Y %H:%M:%S")
    created = "Erstellt am: " + formatierte_zeit
    created_x = 40
    created_y = letter[1] - 92
    pdf.setFont("Helvetica", 16)
    pdf.drawString(created_x, created_y, created)
    
    # Add expiration date
    date_today = datetime.date.today()
    expirationdate = date_today + datetime.timedelta(days=patient_data['expiry_days'])
    expirationdate = expirationdate.strftime("%d.%m.%Y")
    ablaufdatum = "Ablaufdatum: " + str(expirationdate)
    ablaufdatum_x = 40
    ablaufdatum_y = letter[1] - 75
    pdf.setFont("Helvetica", 16)
    pdf.drawString(ablaufdatum_x, ablaufdatum_y, ablaufdatum)
    
    # Add GitHub link
    github_x = 50
    github_y = 50
    pdf.setFont("Helvetica", 12)
    pdf.drawString(github_x, github_y, "GitHub Repository:")
    link_text_x = github_x
    link_text_y = github_y - 20
    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 1)
    pdf.drawString(link_text_x, link_text_y, GITHUB_REPO_URL)
    pdf.linkURL(GITHUB_REPO_URL, (link_text_x, link_text_y - 12, link_text_x + 120, link_text_y - 2))
    
    pdf.showPage()
    pdf.save()
    return pdf_buffer

def generate_pdf(first_name=None, last_name=None, blood_product=None, blood_group=None, station_id=None, birth_date=None, expiry_days=7):
    """Generate a PDF with QR codes."""
    # Generate patient data
    patient_data = generate_patient_data(first_name, last_name, blood_product, blood_group, station_id, birth_date, expiry_days)
    
    # Create PDF
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # QR code parameters
    x, y = 50, 700
    qr_size = 100
    text_x_offset = 50
    font_size = 8
    text_max_width = 400
    
    # Generate QR codes
    qr_codes = generate_qr_codes(
        first_name=first_name,
        last_name=last_name,
        blood_product=blood_product,
        blood_group=blood_group,
        station_id=station_id,
        birth_date=birth_date,
        expiry_days=expiry_days
    )
    
    # Save QR codes to temporary files and add to PDF
    titles = ["Bloodproduct", "Meona Code", "Patient wristband (Fall-ID)"]
    contents = generate_content_strings(patient_data)
    y_positions = [y - 120, y - 320, y - 520]
    
    for i, (qr_code, title, content, y_pos) in enumerate(zip(qr_codes, titles, contents, y_positions)):
        # Save temporary file
        temp_file = f"temp_qr_{i}.png"
        with open(temp_file, "wb") as f:
            f.write(qr_code)
        
        # Add QR code and text to PDF
        pdf.drawInlineImage(temp_file, x, y_pos, width=qr_size, height=qr_size)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x + qr_size + 20, y_pos + 20, title)
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(x + qr_size + 20, y_pos - 5, content[:text_max_width])
        
        # Clean up temp file
        os.remove(temp_file)
    
    # Add logo
    logo_path = "usblogo.png"
    logo_width = 198
    logo_height = 41
    logo_x = letter[0] - logo_width - 20
    logo_y = letter[1] - logo_height - 20
    pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")
    
    # Add title
    title = "SiTra Test QR-Codes UHBS"
    title_x = 40
    title_y = letter[1] - 40
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, title_y, title)
    
    # Add creation time
    aktuelle_zeit = datetime.datetime.now()
    formatierte_zeit = aktuelle_zeit.strftime("%d.%m.%Y %H:%M:%S")
    created = "Erstellt am: " + formatierte_zeit
    created_x = 40
    created_y = letter[1] - 92
    pdf.setFont("Helvetica", 16)
    pdf.drawString(created_x, created_y, created)
    
    # Add expiration date
    date_today = datetime.date.today()
    expirationdate = date_today + datetime.timedelta(days=expiry_days)
    expirationdate = expirationdate.strftime("%d.%m.%Y")
    ablaufdatum = "Ablaufdatum: " + str(expirationdate)
    ablaufdatum_x = 40
    ablaufdatum_y = letter[1] - 75
    pdf.setFont("Helvetica", 16)
    pdf.drawString(ablaufdatum_x, ablaufdatum_y, ablaufdatum)
    
    # Add GitHub link
    github_x = 50
    github_y = 50
    pdf.setFont("Helvetica", 12)
    pdf.drawString(github_x, github_y, "GitHub Repository:")
    link_text_x = github_x
    link_text_y = github_y - 20
    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 1)
    pdf.drawString(link_text_x, link_text_y, GITHUB_REPO_URL)
    pdf.linkURL(GITHUB_REPO_URL, (link_text_x, link_text_y - 12, link_text_x + 120, link_text_y - 2))
    
    pdf.showPage()
    pdf.save()
    return pdf_buffer

if __name__ == "__main__":
    pdf_buffer = generate_pdf()
    uhrzeit = datetime.datetime.now().strftime('%H-%M-%S')
    pdf_file_path = "sitra_qr_codes" + uhrzeit + ".pdf"
    with open(pdf_file_path, "wb") as f:
        f.write(pdf_buffer.getvalue())
    subprocess.Popen(["start", "", pdf_file_path], shell=True)