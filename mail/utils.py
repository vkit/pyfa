from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage


def send_emails(to=None):
    subject = 'Smart ERP, 100% Customized, Just what you need'
    from_email = 'amar@greendesignlabs.in'
    ctx = {}
    message = get_template('mail/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print "Email sent"
