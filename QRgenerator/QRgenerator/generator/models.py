from django.db import models
from django.core.validators import MinLengthValidator
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(null=False,blank=False, max_length=100)
    email = models.EmailField(null=False,blank=False)

# Create your models here.
class QRgenerate(models.Model):
    # MONTH=(
    #     ('01','January'),
    #     ('02','February'),
    #     ('03','March'),
    #     ('04','April'),
    #     ('05','May'),
    #     ('06','June'),
    #     ('07','July'),
    #     ('08','August'),
    #     ('09','September'),
    #     ('10','October'),
    #     ('11','November'),
    #     ('12','December'),

    # )
    batch= models.CharField(
        null=False,
        max_length=1
    )
    count= models.CharField(
        unique=True,
        null=False,
        max_length=5,
        default=''
    )
    uin= models.CharField(
        primary_key=True,
        null=False,
        max_length=17
    )
    class Meta:
        get_latest_by = ['uin']

class UinLinK(models.Model):
    date = models.DateField(
        default=datetime.now,
        null=False
    )
    imei = models.CharField(
        primary_key=True,
        max_length=15,
        verbose_name= 'IMEI',
        help_text="Enter the 15 digit IMEI",
        # error_messages={"IMEI already exists"},
        validators=[MinLengthValidator(15, "Invalid IMEI")]
        )
    iccid= models.CharField(
        unique=True,
        max_length=20,
        verbose_name= 'ICCID',
        help_text="Enter the 20 digit ICCID",
        # error_messages={"ICCID already exists"},
        validators=[MinLengthValidator(20, "Invalid ICCID")]
        )
    uin = models.ForeignKey(QRgenerate, on_delete=models.CASCADE,
        
        max_length=17,
        verbose_name= 'UIN',
        help_text=" Scan the QR / Enter the 17 digit UIN",
        # error_messages={"UIN already exists"},
        validators=[MinLengthValidator(17, "Invalid UIN")]
        )
    added_by = models.CharField(null=False,blank=False, max_length=100, default="Admin")



