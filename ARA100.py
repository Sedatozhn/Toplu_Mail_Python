import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import Tk, Label, Entry, Button, Text, END, filedialog
from tkinter.messagebox import showinfo, showerror

def attach_file():
    global attachment_path
    attachment_path = filedialog.askopenfilename(title="Dosya Seç", filetypes=(("PDF Dosyaları", "*.pdf"), ("Tüm Dosyalar", "*.*")))
    if attachment_path:
        showinfo("Dosya Seçildi", "Seçilen dosya: {attachment_path}")
    else:
        showerror("Hata", "Dosya seçimi iptal edildi.")

def send_email():
    try:
        sender = sender_email.get()
        password = sender_password.get()
        recipients = recipient_emails.get("1.0", END).strip().split(",")
        message_text = email_message.get("1.0", END).strip()

        # E-posta başlıkları ve içeriği
        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = recipient.strip()
            msg["Subject"] = "Yeni Mesaj"

            msg.attach(MIMEText(message_text, "plain"))

            # Eğer dosya seçilmişse ekle
            if 'attachment_path' in globals() and attachment_path:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment_path.split('/')[-1]}"
                    )
                    msg.attach(part)

            # E-posta gönder
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient.strip(), msg.as_string())
            server.quit()

        showinfo("Başarılı", "E-postalar başarıyla gönderildi!")
    except smtplib.SMTPAuthenticationError:
        showerror("Hata", "SMTP kimlik doğrulama hatası. Şifrenizi veya e-postanızı kontrol edin.")
    except FileNotFoundError:
        showerror("Hata", "Eklenecek dosya bulunamadı.")
    except Exception as e:
        print(f"Hata detayları: {e}")
        showerror("Hata", "Bir hata oluştu: {str(e)}")

# GUI oluştur
root = Tk()
root.title("Toplu E-posta Gönderici")
root.geometry("400x600")

attachment_path = None

Label(root, text="Gönderici E-Posta:").pack(pady=5)
sender_email = Entry(root, width=40)
sender_email.pack(pady=5)

Label(root, text="Şifre:").pack(pady=5)
sender_password = Entry(root, width=40, show="*")
sender_password.pack(pady=5)

Label(root, text="Alıcı E-Postalar (Virgülle Ayırın):").pack(pady=5)
recipient_emails = Text(root, width=40, height=5)
recipient_emails.pack(pady=5)

Label(root, text="Mesaj:").pack(pady=5)
email_message = Text(root, width=40, height=10)
email_message.pack(pady=5)

attach_button = Button(root, text="Dosya Ekle", command=attach_file)
attach_button.pack(pady=10)

send_button = Button(root, text="E-postaları Gönder", command=send_email)
send_button.pack(pady=20)

root.mainloop()