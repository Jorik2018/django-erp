from cloudinary.models import CloudinaryField

from common.utils import INDUSTRYCHOICES
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


IMAGE_URL = "http://localhost/"


class User(AbstractUser):
    """
    Main user model for Django ERP.
    """

    ROLE_CHOICES = [
        ("A", "Admin"),
        ("M", "Manager"),
        ("T", "Teacher"),
        ("S", "Student"),
        ("H", "HR"),
        ("C", "Customer"),
        ("P", "Supplier"),
        ("E", "Employee"),
        ("F", "Founder"),
        ("X", "CEO"),
        ("K", "Accountant"),
    ]

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    username = None

    email = models.EmailField(
        unique=True,
    )

    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
    )

    # -------------------------------------------------------------------------
    # Personal information
    # -------------------------------------------------------------------------

    owner_name = models.CharField(
        verbose_name=_("Owner Name"),
        max_length=50,
        blank=True,
        default="",
    )

    address = models.CharField(
        max_length=512,
        blank=True,
        default="",
    )

    phone_regex = RegexValidator(
        regex=r"^(?:\+88|88)?(01[3-9]\d{8})$",
        message=(
            "Phone number must be entered in the format "
            "'+8801XXXXXX'."
        ),
    )

    mobile_number = models.CharField(
        validators=[phone_regex],
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    # -------------------------------------------------------------------------
    # Organization / Business
    # -------------------------------------------------------------------------

    organization_name = models.CharField(
        verbose_name=_("Organization Name"),
        max_length=50,
        blank=True,
        default="",
    )

    business = models.CharField(
        verbose_name=_("Business"),
        max_length=50,
        choices=INDUSTRYCHOICES,
        help_text=_("Select your business type:"),
        null=True,
        blank=True,
    )

    business_manager_name = models.CharField(
        verbose_name=_("Business Manager Name"),
        max_length=50,
        null=True,
        blank=True,
    )

    # -------------------------------------------------------------------------
    # Images
    # -------------------------------------------------------------------------

    brand_logo = CloudinaryField(
        "Brand Logo",
        null=True,
        blank=True,
    )

    photo_link = models.URLField(
        default=IMAGE_URL + "default.jpg",
        blank=True,
    )

    defaultURL = models.URLField(
        null=True,
        blank=True,
    )

    # -------------------------------------------------------------------------
    # Authentication / OTP
    # -------------------------------------------------------------------------

    otp = models.SmallIntegerField(
        help_text="One Time Password",
        null=True,
        blank=True,
    )

    token = models.CharField(
        verbose_name=_("Token"),
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        editable=False,
        help_text="Token for authentication",
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address"),
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_(
            "Designates whether this user has been verified. "
            "Unverified users cannot log in."
        ),
    )

    # -------------------------------------------------------------------------
    # ERP roles
    # -------------------------------------------------------------------------

    is_founder = models.BooleanField(
        _("founder"),
        default=False,
    )

    is_ceo = models.BooleanField(
        _("ceo"),
        default=False,
    )

    is_admin = models.BooleanField(
        _("admin"),
        default=False,
    )

    is_manager = models.BooleanField(
        _("manager"),
        default=False,
    )

    is_hr = models.BooleanField(
        _("hr"),
        default=False,
    )

    is_accountant = models.BooleanField(
        _("accountant"),
        default=False,
    )

    is_employee = models.BooleanField(
        _("employee"),
        default=False,
    )

    is_customer = models.BooleanField(
        _("customer"),
        default=False,
    )

    is_supplier = models.BooleanField(
        _("supplier"),
        default=False,
    )

    # -------------------------------------------------------------------------
    # Timestamps
    # -------------------------------------------------------------------------

    otp_created_time = models.DateTimeField(
        default=now,
        verbose_name=_("OTP created time"),
        editable=False,
    )

    password_changes_datatime = models.DateTimeField(
        verbose_name=_("Password changes datetime"),
        blank=True,
        null=True,
    )

    last_activity = models.DateTimeField(
        verbose_name=_("Last activity"),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        default=now,
        editable=False,
    )

    # -------------------------------------------------------------------------
    # Session
    # -------------------------------------------------------------------------

    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # -------------------------------------------------------------------------
    # Authentication configuration
    # -------------------------------------------------------------------------

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}".strip()

    def set_photo_link(self, name):
        self.photo_link = IMAGE_URL + name
        self.save(update_fields=["photo_link"])

    def is_completed(self):
        return bool(
            self.first_name
            and self.last_name
            and self.address
        )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"