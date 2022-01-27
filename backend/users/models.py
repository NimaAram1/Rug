from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.text import gettext_lazy as _
from django.db.models import Q, F
from .managers import UserManager

class User(AbstractBaseUser):
    """
    A schema of User model
    """
    STATUS = (
        ('gr', 'green'),
        ('ye', 'yellow'),
        ('re', 'red'),
    )
    username = models.CharField(max_length=100, unique=True, verbose_name=_("Username"), help_text=_("Enter your favorite username"))
    email = models.EmailField(max_length=50, unique=True, verbose_name=_("Email"), help_text=_("Enter your email"))
    name = models.CharField(max_length=120, verbose_name=_("Name"), help_text=_("Enter your name"), blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS, verbose_name=_("Status"), help_text=_("Your activity status changed to colors!(green: active, yellow: away, red: busy)"), blank=True, default="gr")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} | {self.email}"

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin    

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["username", "status"]
        indexes = [
            models.Index(name="username_idx", fields=["username"]),
        ]
        constraints = [
             models.CheckConstraint(name="check_username_email_unique", check=~Q(username=F('email'))),
        ]    