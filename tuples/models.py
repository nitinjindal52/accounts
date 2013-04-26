from django.db import models

class account_level(models.Model):
    account_level = models.CharField(max_length=6)
    def __unicode__(self):
        return self.account_type

class account_type(models.Model):
    account_type = models.CharField(max_length=30)
    def __unicode__(self):
        return self.account_type
    
    
class Status(models.Model):
    status = models.CharField(max_length=20)
    def __unicode__(self):
        return self.status
    
class Product(models.Model):
    product = models.CharField(max_length=45)

    
class Project(models.Model):
    project = models.CharField(max_length=45)

class Cost_Centre(models.Model):
    cost_centre = models.CharField(max_length=45)
                
class Account(models.Model):
    account_level = models.CharField(max_length=6)
    account_number = models.CharField(max_length=5,unique=True )
    parent_account = models.CharField(max_length=15,null=True, blank=True)
    account_name = models.CharField(max_length=30)
    account_desc = models.CharField(max_length=60,null=True, blank=True)
    account_type = models.ForeignKey(account_type)
    account_start_date = models.DateField()
    account_end_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status)
    gl_acct = models.CharField(max_length=45, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    cost_centre = models.ForeignKey(Cost_Centre, null=True, blank=True)
    company = models.CharField(max_length=45,null=True, blank=True)
    department = models.CharField(max_length=45,null=True, blank=True)
    created_date = models.DateField(null=True,blank=True)
    updated_date = models.DateTimeField(null=True,blank=True)
    def __unicode__(self):
        return self.account_name
    class Meta:
        unique_together = ('account_number','status','account_type')
    
class Sub_Accountt(models.Model):
    sub_account_number = models.CharField(max_length=10)
    sub_account_name = models.CharField(max_length=30)
    parent_account_number = models.CharField(max_length=5)
    sub_account_desc = models.CharField(max_length=100,null=True, blank=True)
    created_date = models.DateField()
    start_date = models.DateField()
    status = models.ForeignKey(Status)
    updated_date = models.DateTimeField(null=True,blank=True)
    def __unicode__(self):
        return self.sub_account_name    

class Budget(models.Model):
    account = models.ForeignKey(Account)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.IntegerField()
    def __unicode__(self):
        return self.account.account_name
    
class accounting_period(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    def __unicode__(self):
        return self.year
    class Meta:
        unique_together = ('month','year')
    
class Budget1(models.Model):
    account  = models.ForeignKey(Account,blank=True,null=True)
    sub_account = models.ForeignKey(Sub_Accountt,blank=True,null=True)
    accounting_period = models.ForeignKey(accounting_period)
    amount = models.IntegerField()
    class Meta:
        unique_together = ('account','accounting_period')

class Actual(models.Model):
    account = models.ForeignKey(Account,blank=True,null=True)
    sub_account = models.ForeignKey(Sub_Accountt,blank=True,null=True)
    accounting_period = models.ForeignKey(accounting_period)
    amount = models.IntegerField()
# Create your models here.
