from datetime import datetime
from django.contrib import admin
from django.utils.functional import update_wrapper
from ichypd.views import csv_export


class CSVExportAdmin(admin.ModelAdmin):
    change_list_template = 'ichypd/admin/csv_export_change_list.html'
    export_fields = None

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^export/csv/$',
                wrap(self.csv_export_view),
                name='%s_%s_export_csv' % info),
        ) + super(CSVExportAdmin, self).get_urls()
        return urlpatterns

    def csv_export_view(self, request):
        queryset = self.queryset(request)
        if self.export_fields is not None:
            fields = self.export_fields
        else:
            fields = self.list_display
            if fields[0] == 'action_checkbox':
                fields = fields[1:]
        filename = '%s_export_%s.csv' % (
            self.model._meta.object_name.lower(),
            datetime.now().strftime('%Y-%m-%d'))
        return csv_export(
            request,
            queryset=queryset,
            fields=fields,
            filename=filename)
