from django.db import models
from django.contrib.auth.models import User
import datetime
from easy_thumbnails.fields import *

class UserProfile(models.Model):
  user = models.OneToOneField(User, unique=True)

  phone_number = models.CharField(max_length=200, blank=True)

  company_name = models.CharField(max_length=200, blank=True)
  address = models.CharField(max_length=200, blank=True)
  city = models.CharField(max_length=200, blank=True)
  state = models.CharField(max_length=200, blank=True)
  zipcode = models.CharField(max_length=200, blank=True)
  
  available_for_office_hours = models.CharField(max_length=200, blank=True)
  available_for_workshops = models.CharField(max_length=200, blank=True)

  has_parking_pass = models.BooleanField()
  has_office_key = models.BooleanField()
  has_elevator_fob = models.BooleanField()
  
  office_num = models.CharField(max_length=200, blank=True)
  skills = models.CharField(max_length=200, blank=True)
  
  notes = models.TextField(blank=True, help_text="These notes are not visible to members.")

  membership_starts_on = models.DateField(blank=True, null=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
  membership_ends_on = models.DateField(blank=True, null=True)
  membership_type = models.ForeignKey("MembershipType", blank=True, null=True)
  next_billing_date = models.DateField(auto_now_add = True)
  
  image = ThumbnailerImageField(
      upload_to='img/profile_images/%Y/%m/%d',
      resize_source=dict(size=(250, 250)),
      null=True, blank=True)

  def __str__(self): return self.user.username
  def __unicode__(self): return u'%s' % (self.user.username)  

  def cname(self):
    if self.user.first_name:
      if self.user.last_name:
        return self.user.first_name + " " + self.user.last_name
      else:
        return self.user.first_name
    else:
      return self.user.username
      
  def outstanding_bills(self): return Bill.objects.filter(user = self.user).filter(paid = False)
  def settled_bills(self): return Bill.objects.filter(user = self.user).filter(paid = True)
  def account_balance(self):
    total = 0
    try:
      bills = self.user.userprofile.outstanding_bills()
      for bill in bills: total = total + bill.amount
    except:
      pass
    return total

  def membership_is_current(self):
    today = datetime.date.today()
    if self.membership_starts_on:
      if (self.membership_ends_on == None) or (self.membership_ends_on > today):
        return True
      else: return False
    else: return False
    
  def get_absolute_url(self): return "/members/" + str(self.user.id)  
  def title(self): return self.user.get_full_name()




class MembershipType(models.Model):
  name = models.CharField(max_length=200)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  DURATION_CHOICES = (('mo', 'Monthly'),('dy', 'Daily'),('wk', 'Weekly'),('qu', 'Quarterly'),('ba', 'Bi-annually'),('yr', 'Yearly'),)
  duration = models.CharField(max_length=2, choices=DURATION_CHOICES)

  def __str__(self): return self.name
  def __unicode__(self): return u'%s' % (self.name)




class Bill(models.Model):
  user = models.ForeignKey(User)
  date_created = models.DateField(auto_now_add = True)
  collected_for = models.CharField(max_length=200, blank=True)
  amount = models.DecimalField(max_digits=5, decimal_places=2)
  notes = models.TextField(blank=True, null=True)
  paid = models.BooleanField()
  paid_on = models.DateField(blank=True, null=True)

  def __str__(self): return self.user.username + " (" + str(self.date_created) + ")"
  def __unicode__(self): return u'%s' % (self.user.username + " (" + str(self.date_created) + ")")




class BackgroundImage(models.Model):
    url = models.CharField(max_length=200, blank=True)
