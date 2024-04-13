from django.urls import path
from .views import ( UserCreateAPIView, 
                 
                    TaskList , 
                    TaskDetail , 
                    JobList,
                    JobDetail,
                    TaskCreatteList,
                    TaskBulkDelete , 
                    TaskFilter,TaskFilterTwo, 
                    UserCreatedTasks, 
                    TaskAsUser,
                    CreateSuperUser,
                    TasksGroupedByCreatorView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
urlpatterns = [
    path('api/v1/users/', UserCreateAPIView.as_view(), name='user-list'),
    path('api/v1/create-accout/', CreateSuperUser.as_view(), name='create-superuser'),
    path('api/v1/jobs/', JobList.as_view(), name='job-list'),
    path('api/v1/jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'),
    path('api/v1/tasks/', TaskList.as_view(), name='task-list'),
    path('api/v1/tasks/bulk/', TaskCreatteList.as_view(), name='task-bulk-list'),
    path('api/v1/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('api/v1/tasks/delete/', TaskBulkDelete.as_view(), name='task-bulk-delete'),
    path('api/v1/tasks-filter/', TaskFilter.as_view(), name='task-filter'),
    path('api/v1/filter-two/', TaskFilterTwo.as_view(), name='filter-two'),
    path('api/v1/create_tasks/', TasksGroupedByCreatorView.as_view(), name='user-crate-tasks'),
    path('api/v1/tasks_as_user/', TaskAsUser.as_view(), name='user-crate-tasks'),
    path('api/v1/1users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]
