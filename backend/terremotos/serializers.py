from .models import Terremoto
from rest_framework import serializers

class TerremotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terremoto
        fields = "__all__"