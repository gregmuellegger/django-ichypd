from django.conf.urls.defaults import *
from ichypd_tests.forms import PersonalDetailsForm

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
    url(r'^csv-export/$', 'ichypd.views.csv_export', {
        'model_form': PersonalDetailsForm,
    }),
)
