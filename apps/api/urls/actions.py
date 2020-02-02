# from django.urls import path, include
# from apps.api.views import (
#     CreateStaffActionViewSet,
#     UserStaffActionView,
#     AttendanceStaffActionViewSet
# )
# from rest_framework import routers
#
# router = routers.SimpleRouter()
# router.register(
#     r"staff_action", CreateStaffActionViewSet, base_name="staff_action"
# )
# router.register(
#     r"staff_action/list", UserStaffActionView, base_name="staff_action_list"
# )
# router.register(
#     r"attendance", AttendanceStaffActionViewSet, base_name="attendance"
# )
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]
