# from rest_framework import mixins, serializers, status, viewsets
# from rest_framework.response import Response
#
# from apps.api.helpers import CustomAPIException
# from apps.api.serializers import (
#     CreateStaffActionSerializer,
#     StaffActionsSerializer,
#     AttendanceStaffActionSerializer
# )
# from apps.user_profile.models import Certifier
# from apps.actions.models import ActionsModel, StaffActionsModel
#
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from apps.api.helpers.permission import IsAdmin
#
#
# class AttendanceStaffActionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = AttendanceStaffActionSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data, context={"request": request}
#         )
#
#         try:
#             if serializer.is_valid(raise_exception=True):
#                 staff = serializer.validated_data["ci"]
#                 last_action = StaffActionsModel.objects.filter(
#                     staff=staff
#                 ).order_by("-action__created").first()
#
#                 if last_action is not None:
#                     action = ActionsModel.objects.create(
#                         description="",
#                         type=ActionsModel.ARRIVAL
#                         if last_action.action.type == ActionsModel.DEPARTURE
#                         else ActionsModel.DEPARTURE
#                     )
#                 else:
#                     action = ActionsModel.objects.create(
#                         description="",
#                         type=ActionsModel.ARRIVAL
#                     )
#
#                 staff_action = StaffActionsModel.objects.create(
#                     staff=staff,
#                     action=action
#                 )
#
#                 serializer = StaffActionsSerializer(staff_action)
#                 return Response(
#                     serializer.data, status=status.HTTP_201_CREATED
#                 )
#
#         except serializers.ValidationError as e:
#             errors = dict()
#
#             if "error" in e.args[0]:
#                 raise e
#
#             for error in e.args[0].items():
#                 if error[1][0].code == "required":
#                     if "required" not in errors:
#                         errors["required"] = list()
#
#                     errors["required"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 elif error[1][0].code == "blank":
#                     if "blank" not in errors:
#                         errors["blank"] = list()
#
#                     errors["blank"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 elif error[1][0].code == "invalid":
#                     if "invalid" not in errors:
#                         errors["invalid"] = list()
#
#                     errors["invalid"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 if error[1][0].code == "null":
#                     if "null" not in errors:
#                         errors["null"] = list()
#
#                     errors["null"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#             if "blank" in errors:
#                 raise CustomAPIException(
#                     "{} can't be empty.".format(errors["blank"]),
#                     2005,
#                     fields=errors["blank"]
#                 )
#
#             if "required" in errors:
#                 raise CustomAPIException(
#                     "{} are required.".format(errors["required"]),
#                     2006,
#                     fields=errors["required"]
#                 )
#
#             if "invalid" in errors:
#                 raise CustomAPIException(
#                     "The email is invalid.".format(errors["invalid"]),
#                     2009,
#                     fields=errors["invalid"]
#                 )
#
#             if "null" in errors:
#                 raise CustomAPIException(
#                     "{} isn't valid.".format(errors["null"]),
#                     2010,
#                     fields=errors["null"]
#                 )
#
#             raise e
#
#
# class CreateStaffActionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, IsAdmin]
#     serializer_class = CreateStaffActionSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = CreateStaffActionSerializer(
#             data=request.data, context={"request": request}
#         )
#
#         try:
#             if serializer.is_valid(raise_exception=True):
#                 staff = Certifier.objects.get(
#                     user_id=request.data["staff"]
#                 )
#                 action = ActionsModel.objects.create(
#                     description="",
#                     type=request.data["action"],
#                     # duration
#                 )
#
#                 staff_action = StaffActionsModel.objects.create(
#                     staff=staff,
#                     action=action
#                 )
#
#                 serializer = StaffActionsSerializer(staff_action)
#                 return Response(
#                     serializer.data, status=status.HTTP_201_CREATED
#                 )
#
#         except serializers.ValidationError as e:
#             errors = dict()
#
#             if "error" in e.args[0]:
#                 raise e
#
#             for error in e.args[0].items():
#                 if error[1][0].code == "required":
#                     if "required" not in errors:
#                         errors["required"] = list()
#
#                     errors["required"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 elif error[1][0].code == "blank":
#                     if "blank" not in errors:
#                         errors["blank"] = list()
#
#                     errors["blank"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 elif error[1][0].code == "invalid":
#                     if "invalid" not in errors:
#                         errors["invalid"] = list()
#
#                     errors["invalid"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#                 if error[1][0].code == "null":
#                     if "null" not in errors:
#                         errors["null"] = list()
#
#                     errors["null"].append(
#                         {"field": error[0], "message": error[1][0]}
#                     )
#
#             if "blank" in errors:
#                 raise CustomAPIException(
#                     "{} can't be empty.".format(errors["blank"]),
#                     2005,
#                     fields=errors["blank"]
#                 )
#
#             if "required" in errors:
#                 raise CustomAPIException(
#                     "{} are required.".format(errors["required"]),
#                     2006,
#                     fields=errors["required"]
#                 )
#
#             if "invalid" in errors:
#                 raise CustomAPIException(
#                     "The email is invalid.".format(errors["invalid"]),
#                     2009,
#                     fields=errors["invalid"]
#                 )
#
#             if "null" in errors:
#                 raise CustomAPIException(
#                     "{} isn't valid.".format(errors["null"]),
#                     2010,
#                     fields=errors["null"]
#                 )
#
#             raise e
#
#
# class UserStaffActionView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = StaffActionsSerializer
#
#     def get_queryset(self):
#         filters = {
#             "action__type": self.request.query_params.get("type", None),
#             "staff__user_id": self.request.query_params.get("user", None),
#             "action__created__gte": self.request.query_params.get("from", None),
#             "action__created__lte": self.request.query_params.get("to", None),
#         }
#
#         return StaffActionsModel.objects.filter(
#             **dict(
#                 (key, value)
#                 for key, value in filters.items()
#                 if value is not None
#             )
#         )
