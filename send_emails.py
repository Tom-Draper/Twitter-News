import smtplib, sys, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    def _login(self, email, password):
        # Log in to email account.
        # Ensure your gmail account has "less secure app access" allowed in settings.
        print(f"Logging in to {email}...")
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(email, password)
        print("Log-in successful.\n")
        return smtpObj

    def _emailDetails(self):
        with open('email_details.json', 'r') as f:
            data = f.read()
        obj = json.loads(data)
        sender = obj['sender']
        return sender['email'], sender['password'], obj['mail-list']

    def sendEmails(self, subject, body):
        sender_email, sender_password, email_list = self._emailDetails()
        smtpObj = self._login(sender_email, sender_password)
        
        # Build email message to send
        message = MIMEMultipart('alternative')
        message['From'] = sender_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
                
        # Send out reminder emails.
        for i, reciever_email in enumerate(email_list):
            print(f"[{i}/{len(email_list)-1}] Sending email to {reciever_email}...")
            
            # Switch email sending to
            message['To'] = reciever_email
            
            sendmail_status = smtpObj.sendmail(sender_email, reciever_email, message.as_string())
            if sendmail_status != {}:
                print(f"There was a problem sending email to {reciever_email}: {sendmail_status}")
        
        smtpObj.quit()