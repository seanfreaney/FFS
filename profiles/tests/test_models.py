from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import UserProfile

class TestUserProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_str_method(self):
        """Test the string representation of the UserProfile model"""
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_created_on_user_creation(self):
        """Test that a UserProfile is automatically created when a User is created"""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123'
        )
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())

    def test_profile_fields_are_optional(self):
        """Test that all profile fields except user are optional"""
        self.assertIsNone(self.profile.default_phone_number)
        self.assertEqual(self.profile.default_country.code, None)
        self.assertIsNone(self.profile.default_postcode)
        self.assertIsNone(self.profile.default_town_or_city)
        self.assertIsNone(self.profile.default_street_address1)
        self.assertIsNone(self.profile.default_street_address2)
        self.assertIsNone(self.profile.default_county)