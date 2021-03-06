from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from ichypd_tests.forms import PersonalDetailsForm
from ichypd_tests.models import PersonalDetails
from ichypd.views import show_form


class ViewTests(TestCase):
    urls = 'ichypd_tests.urls'

    def test_save(self):
        response = self.client.get('/icanhas-data-plz/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], PersonalDetailsForm))
        self.assertEqual(response.template.name, 'ichypd_tests/personaldetails_form.html')

        data = {
            'first_name': 'Captain',
            'last_name': 'Awesome',
            'email': 'captain.awesome@example.com',
            'age': '23',
        }
        response = self.client.post('/icanhas-data-plz/', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/icanhas-data-plz/thankz/')

        details = PersonalDetails.objects.get()
        self.assertEqual(details.first_name, 'Captain')
        self.assertEqual(details.last_name, 'Awesome')
        self.assertEqual(details.email, 'captain.awesome@example.com')
        self.assertEqual(details.age, 23)

        response = self.client.get('/icanhas-data-plz/thankz/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template.name, 'ichypd_tests/personaldetails_form_confirmation.html')
        self.assertEqual(response.context['object'], details)

    def test_confirmation_view_without_model_form_specified(self):
        data = {
            'first_name': 'Captain',
            'last_name': 'Awesome',
            'email': 'captain.awesome@example.com',
            'age': '23',
        }
        response = self.client.post('/confirmation-has-no-model-form/', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/confirmation-has-no-model-form/confirmation/')

        response = self.client.get('/confirmation-has-no-model-form/confirmation/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], None)


class CSVExportTests(TestCase):
    def test_csv_view(self):
        response = self.client.get('/csv-export/from-model-form/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, '')

        PersonalDetails.objects.create(
            first_name='Jack',
            last_name='Lumber',
            email='wood@example.com',
            age=42)
        PersonalDetails.objects.create(
            first_name='Rodrigo',
            last_name='Gonzales',
            email='rodrigo@example.com',
            age=28)
        response = self.client.get('/csv-export/from-model-form/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content,
            'Jack,Lumber,wood@example.com,42\r\n'
            'Rodrigo,Gonzales,rodrigo@example.com,28\r\n'
        )

    def test_csv_view_with_queryset(self):
        response = self.client.get('/csv-export/queryset/above-30/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, '')

        PersonalDetails.objects.create(
            first_name='Jack',
            last_name='Lumber',
            email='wood@example.com',
            age=42)
        PersonalDetails.objects.create(
            first_name='Rodrigo',
            last_name='Gonzales',
            email='rodrigo@example.com',
            age=28)
        PersonalDetails.objects.create(
            first_name='Lolo',
            last_name='Fernandez',
            email='lolo@example.com',
            age=35)
        response = self.client.get('/csv-export/queryset/above-30/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content,
            'wood@example.com,Jack,Lumber,42\r\n'
            'lolo@example.com,Lolo,Fernandez,35\r\n'
        )

    def test_custom_filename(self):
        response = self.client.get('/csv-export/myfilename.csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=myfilename.csv')

        response = self.client.get('/csv-export/your_filename/strange')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=your_filename/strange')


class AdminIntegrationTests(TestCase):
    def setUp(self):
        self.user = User(
            username='foo',
            email='foo@example.com',
            is_staff=True,
            is_superuser=True)
        self.user.set_password('bar')
        self.user.save()

    def test_admin_csv_export(self):
        self.client.login(username='foo', password='bar')

        PersonalDetails.objects.create(
            first_name='Jack',
            last_name='Lumber',
            email='wood@example.com',
            age=42)
        PersonalDetails.objects.create(
            first_name='Rodrigo',
            last_name='Gonzales',
            email='rodrigo@example.com',
            age=28)
        PersonalDetails.objects.create(
            first_name='Lolo',
            last_name='Fernandez',
            email='lolo@example.com',
            age=35)
        response = self.client.get('/admin/ichypd_tests/personaldetails/export/csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'],
            'attachment; filename=personaldetails_export_%s.csv' % (
                datetime.now().strftime('%Y-%m-%d')))
        self.assertEqual(response.content,
            'Jack,Lumber,42,wood@example.com\r\n'
            'Rodrigo,Gonzales,28,rodrigo@example.com\r\n'
            'Lolo,Fernandez,35,lolo@example.com\r\n'
        )
