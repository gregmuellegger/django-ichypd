import csv
from StringIO import StringIO
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def _get_session_key(model_form):
    opts = model_form._meta.model._meta
    session_key = 'ichypd-%s-%s-saved' % (opts.app_label.lower(), opts.object_name.lower())
    return session_key


def show_form(request, model_form, success_url):
    opts = model_form._meta.model._meta
    template_name = '%s/%s_form.html' % (opts.app_label.lower(), opts.object_name.lower())
    if request.method == 'POST':
        form = model_form(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            request.session[_get_session_key(model_form)] = obj.pk
            return HttpResponseRedirect(success_url)
    else:
        form = model_form()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


def confirmation(request, model_form=None, template_name=None):
    assert model_form is not None or template_name is not None
    if model_form:
        model = model_form._meta.model
        opts = model_form._meta.model._meta
        if template_name is None:
            template_name = '%s/%s_form_confirmation.html' % (opts.app_label.lower(), opts.object_name.lower())
        try:
            obj_pk = request.session[_get_session_key(model_form)]
            obj = model._default_manager.get(pk=obj_pk)
        except (model.DoesNotExist, KeyError):
            obj = None
    else:
        obj = None
    return render_to_response(template_name, {
        'object': obj,
    }, context_instance=RequestContext(request))


def csv_export(request, queryset=None, model_form=None, fields=None,
    filename='export.csv'):
    assert queryset is not None or model_form is not None
    if queryset is not None:
        model = queryset.model
        if fields is None:
            fields = [field.name for field in model._meta.fields]
    elif model_form is not None:
        model = model_form._meta.model
        queryset = model._default_manager.all()
        if fields is None:
            fields = model_form.base_fields.keys()

    content = StringIO()
    writer = csv.writer(content)

    for obj in queryset.all():
        data = []
        for field in fields:
            data.append(getattr(obj, field))
        writer.writerow(data)

    content.seek(0)
    content = unicode(content.read())
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
