from dataclasses import dataclass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


@dataclass
class Gmail(object):
    """Wrapper class to send emails from gmail account"""
    from_addr: str
    password: str
    server: smtplib.SMTP = smtplib.SMTP('smtp.gmail.com', 587)

    def __post_init__(self):
        """Called once new object is created"""
        self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def login(self):
        """Login into gmail server"""
        self.server.starttls()
        self.server.login(self.from_addr, self.password)

    def send(self, to_addr: str, subject: str, body: str,
             attachment: str = None):
        """Send an email using"""
        self.msg = MIMEMultipart()
        self.msg['From'] = self.from_addr
        self.msg['To'] = to_addr
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body, 'plain'))
        if attachment:
            payload = self.create_attachement(attachment)
            self.msg.attach(payload)
        text = self.msg.as_string()
        self.server.sendmail(self.from_addr, to_addr, text)

    def create_attachement(self, path: str):
        with open(path, 'rb') as f:
            content = f.read()
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(content)
            encoders.encode_base64(p)
            p.add_header('Content-Disposition',
                         "attachment; filename= %s" % f.name)
        return p

    def close(self):
        self.server.quit()
