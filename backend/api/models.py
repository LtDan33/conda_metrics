from django.db import models
from rest_framework import serializers
from django.db import models
from django_pandas.managers import DataFrameManager


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


class Product(models.Model):
  product_name=models.TextField()
  objects = models.Manager()
  pdobjects = DataFrameManager()  # Pandas-Enabled Manager
