from django.views.generic import TemplateView

from mail.forms import EmailForm


class EmailView(TemplateView):
    template_name = 'mail/email.html'

    def get_context_data(self, **kwargs):
        context = super(EmailView, self).get_context_data(**kwargs)
        context['form'] = EmailForm()
        return context
