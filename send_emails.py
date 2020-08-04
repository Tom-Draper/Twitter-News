import smtplib, sys, json

class EmailSender():
    def _login(self, email, password):
        # Log in to email account.
        # Ensure your gmail account has "less secure app access" allowed in settings.
        print(f"Logging in to {email}...")
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(email, password)

    def _emailDetails(self):
        with open('email_details.json', 'r') as f:
            data = f.read()
        obj = json.loads(data)
        sender = obj['sender']
        return sender['email'], sender['password'], obj['mail-list']

    def sendEmails(self, subject, body):
        sender_email, sender_password, email_list = _emailDetails()
        smtpObj = _login(email, password)
        
        message = 'Subject: {}\n\n{}'.format(subject, body)
        
        # Send out reminder emails.
        for reciever_email in email_list:
            print(f"Sending email to {reciever_email}...")
            sendmail_status = smtpObj.sendmail(sender_email, reciever_email, message)
            if sendmail_status != {}:
                print(f"There was a problem sending email to {reciever_email}: {sendmail_status}")
        
        smtpObj.quit()

sender = EmailSender()
sender.sendEmails("Weekly News", "Hi")