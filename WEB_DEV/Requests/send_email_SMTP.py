# SMTP - simple mail transfer protocol
import smtplib as smtp


my_email = "email-name@gmail.com"
psw = "password"

# create object from SMTP class
with smtp.SMTP("smtp.gmail.com") as connection:
    # tls - transport layour security. Encrypts email message.
    connection.starttls()

    connection.login(user=my_email, password=psw)

    # after "Subject" you need to write "\n\n" and then your message.
    connection.sendmail(from_addr=my_email,
                        to_addrs=my_email,
                        msg="Subject:Hello\n\nMessage to email was sent")

    connection.close()




