from django.db import models
from django.contrib.auth.models import User


class ForumType(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self): return self.name
  def __unicode__(self): return u'%s' % (self.name)




class Forum(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  forum_type = models.ForeignKey(ForumType)
  
  owners = models.ManyToManyField(User, related_name="forums_owned", blank=True, null=True)
  members = models.ManyToManyField(User, related_name="forums_joined", blank=True, null=True)

  locked = models.BooleanField()

  created_on = models.DateTimeField(auto_now_add = True)

  def __str__(self): return self.name
  def __unicode__(self): return u'%s' % (self.name)
  
  def total_replies(self): return Reply.objects.filter(thread__forum = self).count()
  
  def last_reply_on(self): return Reply.objects.filter(thread__forum = self).order_by('created_on')[:1][0].created_on



class Thread(models.Model):
  forum = models.ForeignKey(Forum)
  user = models.ForeignKey(User)
  
  subject = models.CharField(max_length=200)
  body = models.TextField(blank=True)
  
  locked = models.BooleanField()
  
  created_on = models.DateTimeField(auto_now_add = True)

  def __str__(self): return self.subject
  def __unicode__(self): return u'%s' % (self.subject)
  
  def postcount(self): return self.reply_set.count()
  def last_reply_on(self): return Reply.objects.filter(thread = self).order_by('created_on')[:1][0].created_on

  



class Reply(models.Model):
  thread = models.ForeignKey(Thread)
  
  body = models.TextField(blank=True)
  user = models.ForeignKey(User)

  created_on = models.DateTimeField(auto_now_add = True)
  
  def __str__(self): return self.body
  def __unicode__(self): return u'%s' % (self.body)

  class Meta:
      ordering = ["created_on"] 




class Event(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  forum = models.ForeignKey(Forum, null=True, blank=True)

  hosts = models.ManyToManyField(User, related_name="events_hosted", null=True, blank=True)
  attendees = models.ManyToManyField(User, related_name="events_attending", null=True, blank=True)

  starts_at = models.DateTimeField()
  ends_at = models.DateTimeField()

  def __str__(self): return self.name
  def __unicode__(self): return u'%s' % (self.name)

  def attendee_count(self): return self.attendees.count()


