from django.contrib.auth.models import BaseUserManager
from django.utils.text import gettext_lazy as _
from datetime import datetime

class UserManager(BaseUserManager):
    """
    create_user for creating normal permission user
    create_superuser for creating admin user
    return_user_instance for returning user instance for testing in test_models 
    """
    def create_user(self, email, username, password, name=""):
        if not email:
            raise ValueError(_("If you want to create an account, You must enter an email."))
        elif not username:
            raise ValueError(_("If you want to create an account, You must enter a username."))
            
        user = self.model(email=self.normalize_email(email), username=username, name=name)
        user.set_password(password)
        user.save(using=self._db) 
        return user 

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def return_user_intance(self, email, username, password):
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        return user


class VerificationCodeManager(BaseUserManager):
    def nonexpired(self):
        return self.filter(expire_date__gt=datetime.now())