import csv, io, re
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from participants.models import Participant
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core import mail
from django.core.mail import send_mail
from django.urls import path
from django.shortcuts import render, redirect



def invite_participants(modeladmin, request, queryset):
    messages = []
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
        messages.append(email)
    connection = mail.get_connection(fail_silently=True)
    print(messages)
    connection.open()
    connection.send_messages(messages)
    # email.send(fail_silently=True)

invite_participants.short_description = "Invite filtered participants for exams"

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ParticipantAdmin(admin.ModelAdmin):
    actions = [invite_participants]

    change_list_template = "participants/participants_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
                return redirect("..")
            data_set = csv_file.read().decode('utf-8')
            csv_data = csv.reader(io.StringIO(data_set), delimiter=',')
            #email verification
            EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
            # io_string = io.StringIO(data_set)
            for line in csv_data:
                if len(line) != 3:
                    self.message_user(request, "Revise your csv file and re upload")
                    return redirect("..")
                firstname = line[0]
                print(firstname)
                lastname = line[1] 
                email = line[2]
                if not EMAIL_REGEX.match(email):
                    self.message_user(request, "put a valid email in the right column for user {} {}".format(firstname,lastname))
                    continue
                # if not ( email and firstname and lastname):
                #     raise ValueError(f'Invalid User data!')
                #     self.message_user(request, "You need to provide user email in your csv file")
                #     return redirect("..")
                username = firstname + '_' + lastname
                if User.objects.filter(username=username).exists():
                    self.message_user(request, "A user with the names {} {} already exists in the system ".format(firstname,lastname))
                    continue
                user_password = User.objects.make_random_password()
                user = User(username=username, first_name=firstname, last_name=lastname, password=user_password, email=email)
                user.save()
                # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

admin.site.register(Participant, ParticipantAdmin)
