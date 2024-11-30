import smtplib

# Gönderici bilgileri
gönderen = "limongaming22@gmail.com"
şifresi = "eyxr yfro zrfs mhnk"

# Alıcıların listesi
alıcılar = ["catsltasfevzi@gmail.com", "sedatozhan001@gmail.com", " sedatozhan002@gmail.com"]

# Gönderilecek mesaj
mesaj = "Bu bir deneme mesajidir."

# SMTP sunucusuna bağlan
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Giriş yap
server.login(gönderen, şifresi)
print("Giriş Başarılı!")

# Her alıcıya mail gönder
for alıcı in alıcılar:
    server.sendmail(gönderen, alıcı, mesaj)
    print(f"Mail gönderildi: {alıcı}")

# Sunucudan çıkış yap
server.quit()
print("Tüm mailler başarıyla gönderildi!")