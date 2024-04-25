import random
import datetime
import names
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import date
import subprocess

# Blood_Product_Code

# PREFIX = P

# PATIENT_ID
random_PID = random.sample(range(0, 9), 7)
random_PID = ''.join(map(str, random_PID))

# VISIT_ID
random_VisitID = random.sample(range(0, 9), 8)
random_VisitID = ''.join(map(str, random_VisitID))

# CHARGE_ID
random_chargeID = random.sample(range(0, 9), 2)
random_chargeID = ''.join(map(str, random_chargeID))
chargeID_date = date.today().strftime('%Y%m%d')

# PRODUCT_ID
random_productID = random.sample(range(0, 9), 4)
random_productID = ''.join(map(str, random_productID))
productID_date = date.today().strftime('%y%m')
random_productID = random.sample(range(0, 9), 2)
random_productID = ''.join(map(str, random_productID))

# BLOODEXPIRATIONDATE
date_today = datetime.date.today()
bloodexpirationdate = date_today + datetime.timedelta(days=7)
formatted_date = bloodexpirationdate.strftime("%d.%m.%Y")

# bszPATIENT_ID
random_bluesID = random.sample(range(0, 9), 6)
random_bluesID = ''.join(map(str, random_bluesID))

# Meona_Code

# PREFIX = P

# PATIENTID_ID = random_PID

# ADMINISTRATION_ID
random_administrationID = random.sample(range(0, 9), 6)
random_administrationID = ''.join(map(str, random_administrationID))

# BLOODPRODUCT
bloodproduct = ["ERYTHROCYTE_CONCENTRATE", "FRESH_FROZEN_PLASMA", "FRESH_FROZEN_PLASMA_THAWED",
                "THROMBOCYTE_CONCENTRATE", "SPECIFIC_THROMTOCYTE_CONCENTRATE", "APHERESIS_THROMBOCYTE_CONCENTRATE"]

bloodgroup = ["Oneg|Oneg|", "Opos|Opos|", "Bneg|Bneg|", "Bpos|Bpos|", "Aneg|Aneg|", "Apos|Apos|", "ABneg|ABneg|", "ABpos|ABpos|"]


def selectRandom(names):
    return random.choice(names)


def selectBloodProductType(bloodproduct):
    if bloodproduct == "ERYTHROCYTE_CONCENTRATE":
        return "EK"
    elif bloodproduct in ["FRESH_FROZEN_PLASMA", "FRESH_FROZEN_PLASMA_THAWED"]:
        return "PL"
    else:
        return "TK"


bloodproduct = selectRandom(bloodproduct)
blood_product_type = selectBloodProductType(bloodproduct)
bloodgroup = selectRandom(bloodgroup)


# LAST_NAME
for i in range(1):
    (names.get_last_name())

# FIRST_NAME
for i in range(1):
    (names.get_first_name())


# BIRTH_DATE
def generate_random_birthdate():
    year = random.randint(1950, 2003)

    month = random.randint(1, 12)

    if month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    else:
        day = random.randint(1, 31)

    birthdate = datetime.date(year, month, day)

    return birthdate


# STATIONID
stationID = ["4050", "4100", "4120", "4130", "4140", "4150", "4161", "4170", "4180", "4310", "4410", "4411", "4600",
             "4610", "4620", "4640", "4650", "4660", "4670", "4690", "4700", "4710", "4750", "4770", "4790", "4800",
             "4920", "5010", "5040", "5810", "7777"]


def selectRandom(names):
    return random.choice(names)


# VISIT_ID = random_VisitID

# QRCODE

content1 = (
            "P|" + random_PID + "|00" + random_VisitID + "|" + blood_product_type + "|H00" + chargeID_date + random_chargeID + "|E" + productID_date + "V" + random_productID + "|" + bloodgroup + "|" + formatted_date + "|" + random_bluesID)
content2 = (
            "K^" + random_PID + "^" + random_administrationID + "^" + bloodproduct + "^" + "TEST-" + names.get_last_name() + "^" + names.get_first_name() + "^" + generate_random_birthdate().strftime(
        "%d.%m.%Y") + "^" + selectRandom(stationID))
content3 = (random_VisitID)

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 50, 700
qr_size = 100
text_x_offset = 50
font_size = 8
text_max_width = 400

qr1 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr1.add_data(content1)
qr1.make(fit=True)

qr2 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr2.add_data(content2)
qr2.make(fit=True)

qr3 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr3.add_data(content3)
qr3.make(fit=True)

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 100, 600
qr_size = 150

content1 = (
            "P|" + random_PID + "|00" + random_VisitID + "|" + blood_product_type + "|H00" + chargeID_date + random_chargeID + "|E" + productID_date + "V" + random_productID + "|" + str(bloodgroup) + formatted_date + "|" + random_bluesID)
content2 = (
            "K^" + random_PID + "^" + random_administrationID + "^" + bloodproduct + "^" + "TEST-" + names.get_last_name() + "^" + "TEST-" + names.get_first_name() + "^" + generate_random_birthdate().strftime(
        "%d.%m.%Y") + "^" + selectRandom(stationID))
content3 = (random_VisitID)

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 50, 700
qr_size = 100
text_x_offset = 50
font_size = 8
text_max_width = 400

qr1 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr1.add_data(content1)
qr1.make(fit=True)

qr2 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr2.add_data(content2)
qr2.make(fit=True)

qr3 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr3.add_data(content3)
qr3.make(fit=True)

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 100, 600
qr_size = 150
text_x_offset = 10

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 100, 600
qr_size = 150
text_x_offset = 10

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

x, y = 50, 700
qr_size = 100
text_x_offset = 50
font_size = 8
text_max_width = 400

name1 = "Bloodproduct"
name2 = "Meona Code"
name3 = "Patient wristband (Fall-ID)"

y_shift = 120

pdf.drawInlineImage(qr1.make_image(fill_color="black", back_color="white"), x, y - y_shift, width=qr_size,
                    height=qr_size)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(x + qr_size + 20, y + 20 - y_shift, name1)
pdf.setFont("Helvetica", font_size)
pdf.drawString(x + qr_size + 20, y - 5 - y_shift, content1[:text_max_width])

pdf.drawInlineImage(qr2.make_image(fill_color="black", back_color="white"), x, y - 200 - y_shift, width=qr_size,
                    height=qr_size)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(x + qr_size + 20, y - 180 - y_shift, name2)
pdf.setFont("Helvetica", font_size)
pdf.drawString(x + qr_size + 20, y - 205 - y_shift, content2[:text_max_width])

pdf.drawInlineImage(qr3.make_image(fill_color="black", back_color="white"), x, y - 400 - y_shift, width=qr_size,
                    height=qr_size)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(x + qr_size + 20, y - 380 - y_shift, name3)
pdf.setFont("Helvetica", font_size)
pdf.drawString(x + qr_size + 20, y - 405 - y_shift, content3[:text_max_width])

logo_path = "usblogo.png"
logo_width = 198
logo_height = 41
logo_x = letter[0] - logo_width - 20
logo_y = letter[1] - logo_height - 20

pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")

title = "SiTra Test QR-Codes UHBS"
title_x = 40
title_y = letter[1] - 40
pdf.setFont("Helvetica-Bold", 22)
pdf.drawString(title_x, title_y, title)

aktuelle_zeit = datetime.datetime.now()

formatierte_zeit = aktuelle_zeit.strftime("%d.%m.%Y %H:%M:%S")
print("Erstellt am: " + formatierte_zeit)

created = "Erstellt am: " + formatierte_zeit
created_x = 40
created_y = letter[1] - 92
pdf.setFont("Helvetica", 16)
pdf.drawString(created_x, created_y, created)

date_today = datetime.date.today()
expirationdate = date_today + datetime.timedelta(days=7)
expirationdate = expirationdate.strftime("%d.%m.%Y")

ablaufdatum = "Ablaufdatum: " + str(expirationdate)
ablaufdatum_x = 40
ablaufdatum_y = letter[1] - 75
pdf.setFont("Helvetica", 16)
pdf.drawString(ablaufdatum_x, ablaufdatum_y, ablaufdatum)

pdf.showPage()
pdf.save()

uhrzeit = datetime.datetime.now().strftime('%H-%M-%S')

pdf_file_path = "testcodes/sitra_qr_codes" + uhrzeit + ".pdf"

with open(pdf_file_path, "wb") as f:
    f.write(pdf_buffer.getvalue())

subprocess.Popen(["start", "", pdf_file_path], shell=True)

with open("sitra_qr_codes" + uhrzeit + ".pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())

with open(pdf_file_path, "wb") as f:
    f.write(pdf_buffer.getvalue())

subprocess.Popen(["start", "", pdf_file_path], shell=True)