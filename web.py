import streamlit as st
import main
import datetime
from io import BytesIO
from PIL import Image

# Streamlit-Seitenkonfiguration
st.set_page_config(page_title="SiTra QR Code Generator", layout="centered")

# USB-Logo hinzufügen
logo_path = "assets/uhbs_logo_65_neg.png"
col1, col2 = st.columns([3, 1])
with col1:
    st.title("SiTra QR Code Generator")
with col2:
    try:
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True, caption=None)
    except FileNotFoundError:
        st.error(f"Logo '{logo_path}' nicht gefunden.")

# Beschreibung
st.write("Generieren Sie QR-Codes und PDFs für Blutprodukte mit anpassbaren Einstellungen.")

# Eingabefelder (Einstellungen)
st.subheader("Einstellungen")

col1, col2 = st.columns(2)
with col1:
    use_random_first = st.checkbox("Zufälliger Vorname", value=True)
    first_name = st.text_input("Vorname", placeholder="Vorname", value="" if use_random_first else "", disabled=use_random_first)
with col2:
    use_random_last = st.checkbox("Zufälliger Nachname", value=True)
    last_name = st.text_input("Nachname", placeholder="Nachname", value="" if use_random_last else "", disabled=use_random_last)

use_random_date = st.checkbox("Zufälliges Geburtsdatum", value=True)
birth_date = st.date_input("Geburtsdatum", value=datetime.date(1990, 1, 1), disabled=use_random_date)

use_random_product = st.checkbox("Zufälliges Blutprodukt", value=True)
blood_product = st.selectbox("Blutprodukt", options=["Bitte auswählen..."] + list(main.BLOOD_PRODUCTS.keys()), disabled=use_random_product)

use_random_blood_group = st.checkbox("Zufällige Blutgruppe", value=True)
blood_group = st.selectbox("Blutgruppe", options=["Bitte auswählen..."] + main.BLOOD_GROUPS, disabled=use_random_blood_group)

use_random_station = st.checkbox("Zufällige Stations-ID", value=True)
station_id = st.selectbox("Stations-ID", options=["Bitte auswählen..."] + main.STATION_IDS, disabled=use_random_station)

expiry_days = st.number_input("Ablaufzeit (Tage)", min_value=1, max_value=30, value=7)

# Vorschau- und PDF-Generierung
st.subheader("Aktionen")
if st.button("QR-Codes generieren"):
    with st.spinner("Generiere QR-Codes..."):
        errors = []

        # Validierung
        if not use_random_first and not first_name.strip():
            errors.append("Vorname darf nicht leer sein.")
        if not use_random_last and not last_name.strip():
            errors.append("Nachname darf nicht leer sein.")
        if not use_random_product and blood_product == "Bitte auswählen...":
            errors.append("Bitte ein gültiges Blutprodukt auswählen.")
        if not use_random_blood_group and blood_group == "Bitte auswählen...":
            errors.append("Bitte eine gültige Blutgruppe auswählen.")
        if not use_random_station and station_id == "Bitte auswählen...":
            errors.append("Bitte eine gültige Stations-ID auswählen.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            # Patientendaten generieren
            patient_data = main.generate_patient_data(
                first_name=first_name if not use_random_first else None,
                last_name=last_name if not use_random_last else None,
                blood_product=blood_product if not use_random_product else None,
                blood_group=blood_group if not use_random_blood_group else None,
                station_id=station_id if not use_random_station else None,
                birth_date=birth_date if not use_random_date else None,
                expiry_days=expiry_days
            )

            # QR-Code-Inhalte erstellen
            contents = main.generate_content_strings(patient_data)
            qr_codes = [main.generate_qr_code(content) for content in contents]

            # Titel für die QR-Codes
            titles = ["Bloodproduct Code", "Meona Code", "Patient Wristband"]

            # QR-Codes und Inhalte anzeigen
            # QR-Codes und Inhalte anzeigen
            st.subheader("Generierte QR-Codes")
            for i, (qr_code, content, title) in enumerate(zip(qr_codes, contents, titles)):
                col1, col2 = st.columns([1, 3])
                with col1:
                    # QR-Code-Bild in einem Byte-Stream speichern und anzeigen
                    buffer = BytesIO()
                    qr_code.save(buffer, format="PNG")
                    buffer.seek(0)
                    st.image(buffer, caption=title, use_container_width=True)  # Aktualisiert
                with col2:
                    # Inhalt des QR-Codes anzeigen
                    st.text_area(f"Inhalt von {title}", content, height=100, disabled=True)


            # PDF erstellen
            pdf_buffer = main.generate_pdf_from_qrcodes(qr_codes, patient_data)

            # PDF Download
            st.subheader("PDF Download")
            st.download_button(
                label="PDF herunterladen",
                data=pdf_buffer.getvalue(),
                file_name="sitra_qr_codes.pdf",
                mime="application/pdf"
            )

# Footer
st.write("---")
st.markdown(
    "Entwickelt von [Nikola Hadzic](https://github.com/hadzicni) für das Universitätsspital Basel (UHBS). Alle Rechte vorbehalten."
)
