from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from drf_yasg import openapi
from .models import UserProfile ,Job,Task
from .serializers import UserSerializer ,TaskSerializer,  JobSerializer,GetUserNameSerializer, TaskFilterSerializer,UpdeManyUser ,CreatedBySerializer
from django.http import Http404
from rest_framework_swagger import renderers
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.db import transaction
User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.utils.dateparse import parse_date
from django.db.models import Q
from drf_spectacular.utils import extend_schema,  OpenApiParameter,inline_serializer
from datetime import datetime
from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.types import OpenApiTypes
from drf_spectacular import openapi
from rest_framework import serializers
from django.db.models import Count
from django.shortcuts import get_object_or_404

@authentication_classes([])
@permission_classes([]) 
class CreateSuperUser(APIView):
   
    @extend_schema(
            summary="Create accounts without authentication",
    request = UserSerializer(),
        responses={201: "Created"},
    )
    def post(self, request, *args, **kwargs):
        print("crate_user")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,)) 
class UserCreateAPIView(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    @extend_schema(request=UserSerializer, responses={201: "Created"},)
    def post(self, request, *args, **kwargs):
        print("crate_user")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
        request=UpdeManyUser,
        responses={200: UpdeManyUser},
        parameters=[
            OpenApiParameter(
                name='pk',
                description='The primary key of the user to update',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def put(self, request):
        pk = request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'Missing user ID'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=pk)
        serializer = UpdeManyUser(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
        request=None,
        responses={204: None, 404: 'Not found'},
        parameters=[
            OpenApiParameter(
                name='id',
                description='The ID of the user to be deleted.',
                required=False,  
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'detail': 'Missing user ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    
@permission_classes((permissions.IsAuthenticated,)) 
class JobList(APIView):
    def get(self, request, format=None):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
    @extend_schema(request= JobSerializer)
    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticated,))
class JobDetail(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    
    @extend_schema(request= JobSerializer)
    def put(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((permissions.IsAuthenticated,))  
class TaskList(APIView):

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @extend_schema(request=TaskSerializer,
        responses={201: "Created"}, )
    def post(self, request, format=None):
        print("create_task")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.IsAuthenticated,))
class TaskDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    @extend_schema(request=TaskSerializer)
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((permissions.IsAuthenticated,))  
class TaskCreatteList(APIView):
    
    @extend_schema(request=TaskSerializer(many=True))
    def post(self, request, format=None):
        print("createt_tasklist")
        serializer = TaskSerializer(data=request.data , many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes((permissions.IsAuthenticated,)) 
class TaskBulkDelete(APIView):
    @extend_schema(
    request=inline_serializer(
        name="InlineFormSerializer",
        fields={"task_ids":serializers.ListField(child=serializers.IntegerField())
            # "str_field": serializers.CharField(),
            # "int_field": serializers.IntegerField(),
            # "file_field": serializers.FileField(),
        },
    ),
    )
    def post(self, request, format=None):
        task_ids = request.data.get('task_ids')
        if not task_ids:
            return Response({'error': 'No task_ids provided'}, status=status.HTTP_400_BAD_REQUEST)
        tasks = Task.objects.filter(id__in=task_ids)
        tasks_count = tasks.count()
        if tasks_count == 0:
            return Response({'error': 'No tasks found with the provided IDs'}, status=status.HTTP_404_NOT_FOUND)
        tasks.delete()
        return Response({'message': f'{tasks_count} tasks successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

@permission_classes((permissions.IsAuthenticated,))
class TaskFilter(APIView):
    @extend_schema(parameters=[
        OpenApiParameter(name='keyword', description='<description>',required=True, type=str),],description='More descriptive text') 

    def get(self, request, format=None):
        keyword = request.query_params.get('keyword', '')
        if keyword:
            tasks = Task.objects.filter(description__icontains=keyword)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No keyword provided'}, status=status.HTTP_400_BAD_REQUEST)
        
@permission_classes((permissions.IsAuthenticated,))      
class TaskFilterTwo(APIView):
    
    @extend_schema(parameters=[
        OpenApiParameter(name='startDate', description='The start date of the search range.', required=True, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='endDate', description='The end date of the search range.', required=True, type=str, location=OpenApiParameter.QUERY),
        ],
        description='More descriptive text') 
    
    def get(self, request):
        serializer = TaskFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        tasks = Task.objects.all()
        if start_date and end_date:
            print(start_date)
            tasks = tasks.filter(created_at__range=(start_date, end_date))
            print(tasks)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Debug: Invalid date format for {date_str}. Expected 'YYYY-MM-DD'.")
            return None

@permission_classes((permissions.IsAuthenticated,))  
class UserCreatedTasks(APIView):

    def get(self, request, username):
        try:
            user_profile = UserProfile.objects.get(username=username)
            created_tasks = Task.objects.filter(job__created_by=user_profile)
            serializer = TaskSerializer(created_tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

@permission_classes((permissions.IsAuthenticated,))      
class TaskAsUser(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all()
        data = GetUserNameSerializer(tasks, many=True)
        return Response(data.data)

@permission_classes((permissions.IsAuthenticated,))     
class TasksGroupedByCreatorView(APIView):
    def get(self, request):
        creators = Task.objects.values('created_by').annotate(total=Count('id')).order_by('created_by')
        response_data = []
        for creator in creators:
            tasks = Task.objects.filter(created_by=creator['created_by'])
            serializer = TaskSerializer(tasks, many=True)
            response_data.append({
                'created_by': creator['created_by'],
                'tasks': serializer.data,
                'total': creator['total']
            })

        return Response(response_data, status=status.HTTP_200_OK)