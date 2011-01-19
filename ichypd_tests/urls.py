from django.conf.urls.defaults import *
from django.contrib import admin
from ichypd_tests.forms import PersonalDetailsForm
from ichypd_tests.models import PersonalDetails


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^icanhas-data-plz/$', 'ichypd.views.show_form', {
       'model_form': PersonalDetailsForm,
       'success_url': '/icanhas-data-plz/thankz/',
    }, name='show-form'),
    url(r'^icanhas-data-plz/thankz/$', 'ichypd.views.confirmation', {
       'model_form': PersonalDetailsForm,
    }, name='confirmation'),

    # confirmation page has no model_form specified
    url(r'^confirmation-has-no-model-form/$', 'ichypd.views.show_form', {
       'model_form': PersonalDetailsForm,
       'success_url': '/confirmation-has-no-model-form/confirmation/',
    }),
    url(r'^confirmation-has-no-model-form/confirmation/$', 'ichypd.views.confirmation', {
        'template_name': 'ichypd_tests/personaldetails_form_confirmation.html',
    }),

    # csv stuff
    url(r'^csv-export/from-model-form/$', 'ichypd.views.csv_export', {
        'model_form': PersonalDetailsForm,
    }),
    url(r'^csv-export/queryset/above-30/$', 'ichypd.views.csv_export', {
        'queryset': PersonalDetails.objects.filter(age__gte=30),
        'fields': ('email', 'first_name', 'last_name', 'age'),
    }),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
