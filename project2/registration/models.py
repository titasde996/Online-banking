from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
#from djangotoolbox.fields import ListField
#from .forms import StringListField
# Create your models here.
# class accField(ListField):
#     def formfield(self, **kwargs):
#         return models.Field.formfield(self, StringListField, **kwargs)
class Transac(models.Model):
    transaction_type=models.CharField(max_length=120)
    amount=models.DecimalField(max_digits=22, decimal_places=2)
    Date_time=models.DateTimeField()
    oppo_acc=models.CharField(max_length=50,null=True,blank=True)

class Accounts(models.Model) :
    account_type=models.CharField(max_length=120)
    account_no=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transactions=models.ManyToManyField(Transac,blank=True,null=True)
    balance=models.DecimalField(max_digits=22, decimal_places=2)
    creation_date=models.DateTimeField()
    Maturity_amount=models.DecimalField(max_digits=22, decimal_places=2)
    interest_rate=models.DecimalField(max_digits=3, decimal_places=2)
    Duration=models.DecimalField(max_digits=3, decimal_places=2)
    username=models.CharField(max_length=120,null=True,blank=True)
    def _str_(self) :
        return self.account_no  
class Scheme(models.Model):
    name= models.CharField(max_length=120)
    entry_age=models.DecimalField(max_digits=3, decimal_places=0,null=True)
    Annual_premium=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    description=models.CharField(max_length=350)
    in_image = models.ImageField(upload_to='images',null=True,blank=True)
    
class Accounts_list(models.Model):
    name= models.CharField(max_length=120)
    Date_of_birth= models.DateField(null=True)
    marital_status=models.BooleanField(null=True)
    Address=  models.CharField(max_length=500,null=True)
    aadhar=models.DecimalField(max_digits=12, decimal_places=0,unique=True,null=True)
    username=models.CharField(max_length=120,null=True)
    password=models.CharField(max_length=120,null=True)
    secret_question=models.CharField(max_length=120,null=True)
    accounts=models.ManyToManyField(Accounts,blank=True,null=True)
    email=models.EmailField(max_length=254,null=True)
    Mobile_number=models.BigIntegerField(null=True)
    is_phone_verified=models.BooleanField(default=False,null=True,blank=True)
    otp=models.CharField(max_length=6,null=True,blank=True)
    image = models.ImageField(upload_to='images',null=True,blank=True)
    schemes=models.ManyToManyField(Scheme,null=True,blank=True) 
    count=models.DecimalField(max_digits=10, decimal_places=0,default=0,null=True,blank=True)
    loan_paid=models.BooleanField(null=True,blank=True)
  
    # def save(self, *args, **kwargs):
    #         self.password = make_password(self.password)
    #         self.secret_question = make_password(self.secret_question)
    #         super(Accounts, self).save(*args, **kwargs)
    def _str_(self) :
        return self.name       


