from django.views.generic import TemplateView, View
from django.contrib import messages
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


class GenericDataGridView(TemplateView):

    """
    GenericDataGridView Base view create pages with data grid

    Required properties:
        "model" Django model object need to be assigned whose data
        is rendered as Data grid table
        "list_display" is python tupple which contains "model" attributes
        to be shown as Data grid table columns
        "template_name" is template path for TemplateView



    Codes to be added in Templates:
    For include datagrid table need into template

    Options:
    1) Use date_range = True , for date range is required
    2) Use check_box = False to hide check box column in table

    3) Use action_column_dict to get actions feature
    in the last cloumn of generic data table
    Example: {'Add report': '/job/add_report/'}
    This functionality generates as below
    '/job/add_report/<UUID>' UUID is of model defined above
    """

    model = None
    template_name = None
    list_display = None
    title = ''
    sub_title = ''
    date_range = False
    detail_url_reverse = ''
    check_box = True
    action_dict = None
    # To do need to change this variable name "edit" to "action"
    edit = False
    action_column_name = ''
    action_column_dict = dict()

    def get_context_data(self, **kwargs):
        if self.model is None and self.list_display is None:
            raise ImproperlyConfigured(
                "GenericDataGridView requires a definition of "
                "'model' and 'list_display' ")
        context = super(GenericDataGridView, self).get_context_data(**kwargs)
        context['object_list'] = self.make_query()
        if not self.title:
            context['title'] = self.model._meta.verbose_name
        context['title'] = self.title
        context['sub_title'] = self.sub_title
        context['list_display'] = self.list_display
        # Add Date Query
        context['date_range'] = self.date_range
        # Detail URL
        context['detail_url_reverse'] = self.detail_url_reverse
        # For Check Box
        context['check_box'] = self.check_box
        # For Edit
        context['edit'] = self.edit
        # For name that appears in action column
        context['action_column_name'] = self.action_column_name
        # For dropdown action
        if self.action_dict is not None:
            context['action_dict'] = self.action_dict
            context['action'] = True
        else:
            context['action'] = False
        # For column actions
        if self.action_column_dict:
            context['action_column_dict'] = self.action_column_dict
        return context

    def make_query(self, **kwargs):
        """
        Override this method to send custom filtered object

        Example:
        def make_query(self):
            return self.models.objects.filter(created_at=<some_day>)
        """
        if self.model is None:
            raise ImproperlyConfigured(
                "Need specify 'model' ")
        return self.model.objects.all().order_by('-created_at').iterator()

    def post(self, request, *args, **kwargs):
        if 'go' in self.request.POST:
            print "GO"
            dispatch = request.POST['action']
            self.for_action_keys = request.POST.getlist('for_action')
            print "lenght {0}".format(len(self.for_action_keys))
            self.request.META['PATH_INFO']
            try:
                method = getattr(self, dispatch)
            except:
                raise AttributeError(
                    "GenericDataGridView has no method '{0}' defined."
                    "Please define method '{0}'".format(dispatch)
                )
            if len(self.for_action_keys) == 0:
                messages.error(
                    request,
                    "Error! Select atleast one item for action"
                )
                return HttpResponseRedirect(
                    self.request.META['PATH_INFO'])
            else:
                return method()
        else:
            context = self.get_context_data(**kwargs)
            context['object_list'] = self.make_date_query(
                request, raw_query=context['object_list'],
                *args, **kwargs)
            context['end_date'] = request.POST["end_date"]
            context['start_date'] = request.POST["start_date"]
            logger.debug("context:{0}".format(context))
            return self.render_to_response(context)

    def make_date_query(self, request, raw_query, *args, **kwargs):
        logger.debug('Making date_query')
        if type(raw_query) is QuerySet:
            logger.debug('Is raw data is QuerySet')
            from base.forms import DateRangeForm
            form = DateRangeForm(request.POST)
            if form.is_valid():
                logger.debug('DateRangeForm is valid')
                to_date = form.cleaned_data['end_date']
                from_date = form.cleaned_data['start_date']
                logger.info(
                    "Form is valid with {0}-{1}".format(from_date, to_date))
                if to_date <= timezone.now().date() and from_date <= timezone.now().date():
                    if to_date == from_date:
                        to_date = timezone.datetime.strptime(
                            request.POST["start_date"], "%m/%d/%Y")
                        object_list = raw_query.filter(
                            created_at__year=to_date.year,
                            created_at__month=to_date.month,
                            created_at__day=to_date.day).order_by(
                            '-created_at')
                        return object_list
                    else:
                        # some weired stuff need to add 24hr or day
                        date_range = [from_date,
                                      to_date + timezone.timedelta(hours=24)]
                        object_list = raw_query.filter(
                            created_at__range=date_range).order_by(
                            '-created_at')
                        return object_list
                    logger.debug(
                        "Date filtered objects: {0}".format(object_list))
                else:
                    logger.debug("Improper Date Range")
                    messages.warning(request,
                                     "Improper dates try other dates")
            else:
                logger.debug("Improper Date Range")
                messages.warning(request,
                                 "Improper dates try other dates")


class GenericMultiDataGridView(TemplateView):

    """
    """
    model_matrix = None

    def get_context_data(self, **kwargs):
        if self.model_matrix is None:
            raise ImproperlyConfigured(
                "GenericMultiDataGridView requires a definition of "
                "'model_matrix' ")
        context = super(
            GenericMultiDataGridView, self).get_context_data(**kwargs)
        for model in self.model_matrix:
            if model.get('model_class', None) is None:
                raise ImproperlyConfigured(
                    "GenericMultiDataGridView requires a definition of "
                    "'model_class' in each dict elements of "
                    "'model_matrix' array"
                )
            # Default values
            if model.get('date_range', None) is None:
                model['date_range'] = False
            if model.get('check_box', None) is None:
                model['check_box'] = True
            model['action_dict'] = model.get('action_dict', None)
            model['query_method'] = model.get('query_method', None)
            #
            if model['query_method'] is None:
                model['object_list'] = self.make_query(
                    model=model['model_class'])
            else:
                try:
                    query_method = getattr(self, model['query_method'])
                except:
                    raise ImproperlyConfigured(
                        "GenericMultiDataGridView requires a definition of"
                        " '{0}' method".format(
                            model['query_method'])
                    )
                model['object_list'] = query_method()
        context['model_matrix'] = self.model_matrix
        return context

    def make_query(self, model, **kwargs):
        """
        """
        return model.objects.all().order_by('-created_at')

    def post(self, request, *args, **kwargs):
        if 'go' in self.request.POST:
            print "GO"
            dispatch = request.POST['action']
            self.for_action_keys = request.POST.getlist('for_action')
            print "lenght {0}".format(len(self.for_action_keys))
            self.request.META['PATH_INFO']
            try:
                method = getattr(self, dispatch)
            except:
                raise AttributeError(
                    "GenericDataGridView has no method '{0}' defined."
                    "Please define method '{0}'".format(dispatch)
                )
            if len(self.for_action_keys) == 0:
                messages.error(
                    request,
                    "Error! Select atlest one item for action"
                )
                return HttpResponseRedirect(
                    self.request.META['PATH_INFO'])
            else:
                return method()
        else:
            context = self.get_context_data(**kwargs)
            context['object_list'] = self.make_date_query(
                request, raw_query=context['object_list'],
                *args, **kwargs)
            context['end_date'] = request.POST["end_date"]
            context['start_date'] = request.POST["start_date"]
            logger.debug("context:{0}".format(context))
            return self.render_to_response(context)

    def make_date_query(self, request, raw_query, *args, **kwargs):
        logger.debug('Making date_query')
        if type(raw_query) is QuerySet:
            logger.debug('Is raw data is QuerySet')
            from base.forms import DateRangeForm
            form = DateRangeForm(request.POST)
            if form.is_valid():
                logger.debug('DateRangeForm is valid')
                to_date = form.cleaned_data['end_date']
                from_date = form.cleaned_data['start_date']
                logger.info(
                    "Form is valid with {0}-{1}".format(from_date, to_date))
                if to_date <= timezone.now().date() and from_date <= timezone.now().date():
                    if to_date == from_date:
                        to_date = timezone.datetime.strptime(
                            request.POST["start_date"], "%m/%d/%Y")
                        object_list = raw_query.filter(
                            created_at__year=to_date.year,
                            created_at__month=to_date.month,
                            created_at__day=to_date.day).order_by(
                            '-created_at')
                        return object_list
                    else:
                        # some weired stuff need to add 24hr or day
                        date_range = [from_date,
                                      to_date + timezone.timedelta(hours=24)]
                        object_list = raw_query.filter(
                            created_at__range=date_range).order_by(
                            '-created_at')
                        return object_list
                    logger.debug(
                        "Date filtered objects: {0}".format(object_list))
                else:
                    logger.debug("Improper Date Range")
                    messages.warning(request,
                                     "Improper dates try other dates")
            else:
                logger.debug("Improper Date Range")
                messages.warning(request,
                                 "Improper dates try other dates")


class GenericModalCreateView(View):

    form_class = None
    success_url = None
    object_name = None
    error_url = None

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and
        calls form_check() method to process form
        """
        print "+++++++++++++++"
        print "I am in post"
        print "++++++++++++++++"
        if self.form_class is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires a definition of "
                "'form_class'")
        return self.form_init(request, *args, **kwargs)

    def form_init(self, request, *args, **kwargs):
        """
        Instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.form_class(request.POST)
        print "+++++++"
        print form
        print "+++++++"
        return self.form_check(form, *args, **kwargs)

    def form_check(self, form, *args, **kwargs):
        if form.is_valid():
            logger.debug("Form is valid")
            return self.form_valid(form)
        else:
            logger.debug("Form is invalid %s " % form.errors)
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        msg = form.errors
        print msg
        logger.debug(self.request.POST)
        messages.warning(self.request, msg)
        return HttpResponseRedirect(self.get_error_url())

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print "Form valid"
        form.save()
        msg = "Succesfully created new {0} {1}".format(
            self.object_name, form.instance)
        print "Form Saved"
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url' or get_success_url method")
        return self.success_url

    def get_error_url(self):
        if self.error_url is None:
            return self.get_success_url()
        else:
            return self.error_url


class CustomRedirection(GenericModalCreateView):

    # Obsolete not to be used to further views 15/09/2016

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


class GenericModalUpdateView(CustomRedirection):
    form_class = None
    object_name = None
    model = None

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            msg = "{0} {1} is updated".format(
                self.object_name, form.instance)
            messages.success(self.request, msg)
        else:
            print form.errors
            print "form is invalid"
            msg = "{0}".format(form.errors)
            messages.warning(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())


class CustomSelfRedirection(GenericModalCreateView):
    app_url = None
    page_url = None
    pk_id = 0

    def form_valid(self, form):
        instance = form.instance
        instance.save()
        instance_id = instance.id
        self.pk_id = instance_id
        msg = "Succesfully created new {0} {1}".format(
            self.object_name, form.instance)
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.app_url is None and self.page_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}{2}".format(
            self.app_url, self.pk_id, self.page_url)


class GenericSelfRedirection(GenericModalCreateView):

    """
    This can used to create objects and redirect to the detail
    page of created object

    *Required
    'url_pattern_list' is list of url patter
    Ex:
    url_pattern_list = ['foo', 'bar'] which returns urlpattern
    as 'foo/bar/<UUID>'
    """

    url_pattern_list = None
    pk_id = None

    def form_valid(self, form):
        instance = form.instance
        instance.save()
        instance_id = instance.id
        self.pk_id = instance_id
        msg = "Succesfully created new {0} {1}".format(
            self.object_name, form.instance)
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.url_pattern_list is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        url_pattern = '/'.join(self.url_pattern_list)
        return "/{0}/{1}".format(
            url_pattern, self.pk_id)


class BaseDeleteView(
    PermissionRequiredMixin, View
):
    """
        This view fetches the current object's
        pk supplied from url and delete the entire object
        and its related sub-objects.
    """
    permission_required = None
    model = None
    success_url = None

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        msg = "Succesfully Deleted {0}".format(obj)
        obj.delete()
        messages.warning(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


class CustomRedirection1(GenericModalCreateView):
    """
    works same as customredirection without containing 
    page_url 

    """

    app_url = None

    def get_success_url(self):
        if self.app_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return "{0}{1}".format(
            self.app_url,
            self.kwargs.get('pk')
        )


class GenericDynamicEditFormView(TemplateView):
    model = None
    form = None
    object_name = ''
    success_url = None
    template_name = 'base/edit_form.html'

    def get_context_data(self, **kwargs):
        """
        This method handles ajax call and
        send a form with and instance received as
        context which will be loaded inside the editmodal
        """
        print "+++++++++++++++++"
        print "I  am coming here"
        print "+++++++++++++++++"
        context = super(
            GenericDynamicEditFormView, self).get_context_data(**kwargs)
        post_text = self.request.GET['obj_id']
        print "++++++++++++++++++++++++"
        print post_text
        print "++++++++++++++++++++++++"
        obj = self.model.objects.get(
            pk=post_text)
        print "++++++++++++++++++++"
        print obj
        print "++++++++++++++++++++"
        context['form'] = self.form(instance=obj)
        return context

    def post(self, request, *args, **kwargs):
        """
        This handles post request once the redered form is posted"""
        obj_id = request.POST['obj_id']
        obj = self.model.objects.get(pk=obj_id)
        form = self.form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            msg = "{0} {1} is updated".format(
                self.object_name, form.instance)
            messages.success(self.request, msg)
        else:
            print form.errors
            print "form is invalid"
            msg = "{0}".format(form.errors)
            messages.warning(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url is None:
            raise ImproperlyConfigured(
                "GenericModalCreateView requires either a definition of "
                "'success_url'")
        return self.success_url
