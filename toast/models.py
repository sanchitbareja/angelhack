from django.db import models
from django.contrib.auth.models import User

class Toast(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField(max_length=200)
	timestap = models.DateTimeField(auto_now_add=True)