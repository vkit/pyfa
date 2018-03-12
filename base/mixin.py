import datetime

from django.utils import timezone

from django.contrib import messages

from django.shortcuts import HttpResponseRedirect

from django.http import Http404

from django.core.exceptions import ImproperlyConfigured

import logging
logger = logging.getLogger(__name__)


class GeneralContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(GeneralContextMixin, self).get_context_data(**kwargs)
        context["username"] = self.request.user.username
        return context


class CustomRedirectMixin(object):

    app_url = None
    page_url = None

    def get_success_url(self):
        if self.app_url is None and self.page_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}{2}".format(
            self.app_url,
            self.kwargs.get('pk'),
            self.page_url)


class DeleteMixin(object):
    model = None
    app_url = None
    page_url = None
    object_name = None

    def post(self, request, *args, **kwargs):
        for_action = request.POST.getlist('for_action')
        objects = self.model.objects.filter(pk__in=for_action)
        if len(objects) == 0:
            messages.warning(
                request,
                "Select atleast one %s" % self.object_name)
            return HttpResponseRedirect(self.get_success_url())
        else:
            if 'delete' in request.POST:
                for x in objects:
                    x.delete()
                messages.warning(
                    request,
                    "Following %s are deleted %s" % (self.object_name, objects)
                )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.app_url is None and self.page_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}{2}".format(
            self.app_url,
            self.kwargs.get('pk'),
            self.page_url)


class DeleteLastObjectMixin(object):
    related_obj = None
    object_name = None
    app_url = None
    page_url = None
    model = None

    def get(self, request, *args, **kwargs):
        try:
            obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        except:
            raise Http404
        objs = getattr(obj, self.related_obj)
        if objs.last():
            objs.last().delete()
            messages.warning(
                        request,
                        "Deleted last %s" % (self.object_name)
                    )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.warning(
                        request,
                        "No roll"
                    )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.app_url is None and self.page_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}{2}".format(
            self.app_url,
            self.kwargs.get('pk'),
            self.page_url)



class DateQueryMixin(object):
    def post(self, request, *args, **kwargs):
        logger.debug("Its Post DateQuerying ")
        form = DateRangeForm(request.POST)
        if form.is_valid():
            to_date = form.cleaned_data['to_date']
            from_date = form.cleaned_data['from_date']
            logger.info("Form is valid with {0}-{1}".format(from_date, to_date))
            if to_date <= timezone.now().date() and from_date <= timezone.now().date():
                if to_date == from_date:
                    to_date = datetime.datetime.strptime(request.POST["to_date"],"%m/%d/%Y" )
                    self.object_list = self.model.objects.filter(
                    created_at__year = to_date.year,
                    created_at__month = to_date.month,
                    created_at__day = to_date.day).order_by('-created_at')
                else:
                    # some weired stuff need to add 24hr or day
                    date_range = [from_date,
                                  to_date+datetime.timedelta(hours=24)]
                    self.object_list = self.model.objects.filter(created_at__range=date_range).order_by('-created_at') 
            else:
                logger.debug("Improper Date Range")
                messages.warning(request,
                                 "Improper dates try other dates")
                return self.get(self, request, *args, **kwargs)
        else:
            logger.debug("Form is invalid {0}".format(form.errors))
            messages.warning(request, "Improper dates try other dates")
            return self.get(self, request, *args, **kwargs)

        context = self.get_context_data(
            to_date=request.POST["to_date"],
            from_date=request.POST["from_date"]
            )
        return self.render_to_response(context)


class DateQueryTemplateViewMixin(object):

    """
    This mixin Querys 'date_query_model' with given and returns context
    defined as  'query_context_object_name'  """

    date_query_model = None
    query_context_object_name = None

    def post(self, request, *args, **kwargs):
        logger.debug("Its Post DateQuerying ")
        form = DateRangeForm(request.POST)
        if form.is_valid():
            to_date = form.cleaned_data['to_date']
            from_date = form.cleaned_data['from_date']
            logger.info("Form is valid with {0}-{1}".format(from_date, to_date))
            if to_date <= timezone.now().date() and from_date <= timezone.now().date():
                if to_date == from_date:
                    to_date = datetime.datetime.strptime(request.POST["to_date"],"%m/%d/%Y" )
                    object_list = self.date_query_model.objects.filter(
                        created_at__year=to_date.year,
                        created_at__month=to_date.month,
                        created_at__day=to_date.day).order_by('-created_at')
                else:
                    # some weired stuff need to add 24hr or day
                    date_range = [from_date,
                                  to_date+datetime.timedelta(hours=24)]
                    object_list = self.date_query_model.objects.filter(created_at__range=date_range).order_by('-created_at')
            else:
                logger.debug("Improper Date Range")
                messages.warning(request,
                                 "Improper dates try other dates")
                return self.get(self, request, *args, **kwargs)
        else:
            logger.debug("Form is invalid {0}".format(form.errors))
            messages.warning(request, "Improper dates try other dates")
            return self.get(self, request, *args, **kwargs)
        filtered_list = self.get_more_filters(object_list)
        query_context_object_name = self.query_context_object_name
        context = self.get_context_data(
            to_date=request.POST["to_date"],
            from_date=request.POST["from_date"]
            )
        context[query_context_object_name] = filtered_list
        return self.render_to_response(context)

    def get_more_filters(self, object_list):
        return object_list


class ForActionMixin(object):
    model = None
    app_url = None
    page_url = None
    object_name = None

    def post(self, request, *args, **kwargs):
        for_action = request.POST.getlist('for_action')
        objects = self.model.objects.filter(pk__in=for_action)
        print "++++++++++++++++++++++"
        print objects
        print "++++++++++++++++++++++"
        if len(objects) == 0:
            messages.warning(
                request,
                "Select atleast one %s" % self.object_name)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.do_action(objects)

    def do_action(self, objects):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.app_url is None and self.page_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}{2}".format(
            self.app_url,
            self.kwargs.get('pk'),
            self.page_url)



# class BaseTemplateMixin(object):


#     def get(self, request, *args, **kwargs):
#         