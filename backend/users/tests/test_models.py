from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# getting user model
User = get_user_model()

class UsersModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", username="test", name="abbas", password="test")

        # testing part

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.name, "abbas")
        self.assertNotEqual(user.password, "test")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)