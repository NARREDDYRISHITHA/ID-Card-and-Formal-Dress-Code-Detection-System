import os
import smtplib
import zipfile
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ✅ Email Credentials
email_address = "ambatijayacharan18@gmail.com"
email_password = "jnzu ewoa orde weyx"  # Use App Password for security
recipient_email = "99220040144@klu.ac.in"

# ✅ Define the folder to send
violations_folder = "Violations"
zip_filename = "Violations.zip"

# ✅ Ensure the folder exists before proceeding
if not os.path.exists(violations_folder):
    print(f"❌ Error: Folder '{violations_folder}' does not exist.")
    exit()

# ✅ Compress the folder into a ZIP file
def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    print(f"✅ Folder '{folder_path}' compressed into '{zip_path}'")

zip_folder(violations_folder, zip_filename)

# ✅ Create and send the email with the ZIP file attached
def send_email():
    msg = MIMEMultipart()
    msg["From"] = email_address
    msg["To"] = recipient_email
    msg["Subject"] = "🚨 Violations Report - ID Card & Formal Dress Check 🚨"

    # Attach the ZIP file
    with open(zip_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={zip_filename}")
        msg.attach(part)

    # ✅ Send email via Gmail SMTP server
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, recipient_email, msg.as_string())
        server.quit()
        print(f"📩 Email sent successfully to {recipient_email} with '{zip_filename}' attached!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

send_email()

# ✅ Optional: Remove the ZIP file after sending
os.remove(zip_filename)
print("🗑️ Temporary ZIP file deleted.")
