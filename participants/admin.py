from django.contrib import admin
from participants.models import Participant
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail



def invite_participants(modeladmin, request, queryset):
    for user in queryset:
        # user = user.user
        # print(user.user.pk)
        user.is_active = False
        current_site = get_current_site(request)
        mail_subject = 'Activate your online examinations account.'
        message = render_to_string('participants/acc_active_email.html', {
            'user': user.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email], reply_to=['onenfelix90@gmail.com'],
    headers={'Message-ID': 'foo'},
        )
        email.content_subtype = "html"
        email.send()

invite_participants.short_description = "Invite filtered participants for exams"

class ParticipantAdmin(admin.ModelAdmin):
    actions = [invite_participants]

admin.site.register(Participant, ParticipantAdmin)
