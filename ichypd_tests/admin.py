from django.contrib import admin
from ichypd.admin import CSVExportAdmin
from ichypd_tests.models import PersonalDetails


class PersonalDetailsAdmin(CSVExportAdmin):
    list_display = ('first_name', 'last_name', 'age', 'email',)
    date_hierarchy = 'created'


admin.site.register(PersonalDetails, PersonalDetailsAdmin)
