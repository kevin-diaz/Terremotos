from .models import Terremoto
from django.db.models import fields
from rest_framework import serializers

class TerremotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terremoto
        fields = "__all__"