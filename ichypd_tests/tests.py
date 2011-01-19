from mock import Mock
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
