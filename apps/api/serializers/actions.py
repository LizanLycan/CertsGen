# from apps.api.helpers import CustomAPIException
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import check_password
# from rest_framework import serializers
# from apps.actions.models import ActionsModel, StaffActionsModel
# from apps.user_profile.models import Certifier
# from .staff import StaffSerializer
#
#
# class AttendanceStaffActionSerializer(serializers.ModelSerializer):
#     ci = serializers.SlugRelatedField(
#         queryset=Certifier.objects.all(),
#         many=False,
#         slug_field="ci",
#         write_only=True,
#         required=True
#     )
#     password = serializers.CharField(
#         required=True
#     )
#
#     class Meta:
#         model = StaffActionsModel
#         fields = '__all__'
#
#     def validate(self, attrs):
#         user = attrs["ci"].user
#         if not check_password(attrs["password"], user.password):
#             raise CustomAPIException(
#                 "Password Error",
#                 3000
#             )
#
#         return attrs
#
#
# class CreateStaffActionSerializer(serializers.ModelSerializer):
#     """
#     Custom serializer for Staff action
#     """
#     staff = serializers.SlugRelatedField(
#         queryset=Certifier.objects.all(),
#         many=False,
#         slug_field="user_id",
#         write_only=True,
#         required=True
#     )
#     action = serializers.CharField(
#         required=True
#     )
#     duration = serializers.DurationField(
#         required=False
#     )
#
#     class Meta:
#         model = StaffActionsModel
#         fields = '__all__'
#
#     def validate(self, attrs):
#         if attrs["action"] not in [type_a[0] for type_a in ActionsModel.TYPES]:
#             raise CustomAPIException(
#                 "Action does not exist.",
#                 2002
#             )
#
#         last_action = StaffActionsModel.objects.filter(
#             staff=attrs["staff"]
#         ).order_by("-action__created").first()
#
#         if last_action is not None:
#             if last_action.action.type == attrs["action"]:
#                 raise CustomAPIException(
#                     "Invalid Action",
#                     2001
#                 )
#
#         return attrs
#
#
# class ActionsSerializer(serializers.ModelSerializer):
#
#     """
#     Custom Serializer for User
#     """
#
#     class Meta:
#         model = ActionsModel
#         fields = ("id", "duration", "description", "type", "created")
#
#
# class StaffActionsSerializer(serializers.ModelSerializer):
#
#     """
#     Custom Serializer for User
#     """
#     staff = StaffSerializer()
#     action = ActionsSerializer()
#
#     class Meta:
#         model = ActionsModel
#         fields = ("id", "staff", "action")
