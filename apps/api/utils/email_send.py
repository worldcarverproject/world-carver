from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from users.models.user import User

from .tokens import TokenGenerator

def send_verification_email(user: User, request):
    token_generator = TokenGenerator()
    token = token_generator.make_token(user)
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    # TODO: Prepare proper email template when frontend is ready
    message = render_to_string('users/verify_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': user.id,
        'token': token,
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()