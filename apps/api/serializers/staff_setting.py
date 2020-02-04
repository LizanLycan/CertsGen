from django.contrib.auth.models import User
from rest_framework import serializers


class StaffSettingSerializer(serializers.Serializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        many=False,
        slug_field="id",
        write_only=True,
        required=True
    )
    # def validate(self, attrs):
    #     try:
    #         User.objects.get(id=attrs[user])
    #     return attrs

    def update(self, instance, validated_data):
        instance.staffmodel.is_admin = not instance.staffmodel.is_admin
        return instance
