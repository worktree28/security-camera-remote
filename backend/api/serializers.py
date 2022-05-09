from rest_framework import serializers
from .models import Snap


class SnapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snap
        fields = ('time', 'img_url')
