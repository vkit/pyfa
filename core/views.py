from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from base.mixin import GeneralContextMixin


class DashboardDispatcherView(GeneralContextMixin, TemplateView):

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('auth.add_user'):
            return HttpResponseRedirect(reverse('core:standardmodel'))
        elif self.request.user.has_perm('jobspec.add_jobspec'):
            return HttpResponseRedirect(reverse('core:admin_dashboard'))
        elif self.request.user.has_perm('routecard.add_routecardreport'):
            return HttpResponseRedirect(reverse('core:admin_dashboard'))
        else:
            return HttpResponseRedirect('/admin/')


class DashboardStandModView(GeneralContextMixin, TemplateView):
    template_name = 'dashboard.html'


class AdminDashboardView(GeneralContextMixin, TemplateView):
    template_name = 'dashboard_admin.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        return context


class OperatorDashboardView(GeneralContextMixin, TemplateView):
    template_name = 'dashboard_operator.html'


locals()['SupervisorDashboardView'] = type(
    'SupervisorDashboardView',
    (GeneralContextMixin, TemplateView),
    {
        'template_name': 'project_base/supervisor_base_dashboard.html'
    }
)

# For change password


@login_required
def change_password(request):
    username = request.user.username
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            request.user.set_password(request.POST['password1'])
            request.user.save()
            messages.success(request, "Password reset successful ")
            return HttpResponseRedirect("/dashboard_dispatcher/")
        else:
            messages.success(request, "Try again Error Password did not match")
            return render(request, 'change_password.html', {'username':username})
    else:
        return render(request, 'change_password.html', {'username':username})

