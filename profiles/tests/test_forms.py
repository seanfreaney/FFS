from django.test import TestCase
from profiles.forms import UserProfileForm

class TestUserProfileForm(TestCase):
    def test_form_fields_are_explicit_in_form_metaclass(self):
        """Test that the correct fields are excluded in the form"""
        form = UserProfileForm()
        self.assertEqual(form.Meta.exclude, ('user',))

    def test_form_fields_are_present(self):
        """Test that the expected fields are present in the form"""
        form = UserProfileForm()
        expected_fields = [
            'default_phone_number',
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
            'default_street_address2',
            'default_county',
            'default_country',
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)