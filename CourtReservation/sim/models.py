from django.db import models
# Create your models here.

class UserLogins(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_logins'

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.TextField()
    phone_number = models.CharField(max_length=255)
    email = models.OneToOneField(UserLogins, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'users'