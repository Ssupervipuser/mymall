from rest_framework import serializers

from apps.areas.models import Area


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model=Area
        fields=['id','name']


class SubsSerializer(serializers.ModelSerializer):
    """详细地址序列化器"""
    subs=AreaSerializer(many=True)
    class Meta:
        model=Area
        fields=['id','name','subs']