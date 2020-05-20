from rest_framework import routers
from apps.users.views import UserViewSet
from apps.filemanager.views import DataViewSet
from apps.drivetime.views import DriveTimeViewSet



# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)
api.register(r'files', DataViewSet)
api.register(r'drivetime', DriveTimeViewSet, basename='drivetime')
