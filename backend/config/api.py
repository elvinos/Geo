from rest_framework import routers
from apps.drivetime.views import DriveTimeViewSet, DriveTimeAnalysisView, DTAMethodsView
from apps.filemanager.views import DataViewSet
from apps.users.views import UserViewSet

api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)
api.register(r'files', DataViewSet)
api.register(r'drivetime', DriveTimeViewSet, basename='drivetime')
api.register(r'drive', DTAMethodsView, basename='drive')
