import smtplib
from email.mime.text import MIMEText

def sendMail(subject, articleLink, violationList):
    sender = 'g29298@gmail.com'
    receivers = 'g25259@live.com'
    host = 'smtp.gmail.com'
    text = ''
    msg = MIMEText(text)
    msg['Subject'] = 'hello'
    msg['From'] = sender
    msg['To'] = receivers
    
    try:
        smtpObj = smtplib.SMTP(host)
        smtpObj.starttls()
        smtpObj.login(sender, 'fec572nst')
        smtpObj.sendmail(sender, [receivers], msg.as_string())
        smtpObj.quit()
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"
        return

sendMail('test', 'test', 'test')


