from rest_framework import serializers
from .models import UserProfile, Job, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'full_name']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'created_at']
       
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
 
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'birth_date', 'hometown', 'school', 'avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('id', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.birth_date = validated_data.get('birth_date', None)
        user.hometown = validated_data.get('hometown', '')
        user.school = validated_data.get('school', '')
        user.avatar = validated_data.get('avatar', None)
        user.save()
        return user
    
class UpdeManyUser(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
   
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'birth_date', 'hometown', 'school', 'avatar')
        extra_kwargs = {'password': {'write_only': True}}
    def update(self, instance, validated_data):
        validated_data.pop('id', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='id',
        queryset=UserProfile.objects.all(),
        many=True 
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    # assigned_to = UserSerializer(many=True)
    class Meta:
        model = Task
        fields = ['id', 'job', 'title', 'description', 'assigned_to','created_by', 'created_at','updated_at']

    def create(self, validated_data):
        assigned_to = validated_data.pop('assigned_to', None)
        task = Task.objects.create(**validated_data)
        if assigned_to:
            task.assigned_to.set(assigned_to)
        task.save()
        return task
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.assigned_to.set(validated_data.get('assigned_to', instance.assigned_to.all()))
        instance.save()
        return instance

class GetUserNameSerializer(serializers.ModelSerializer):
    assigned_persion = serializers.SerializerMethodField() 
    def get_assigned_persion(self, obj):
        assigned_to_users = obj.assigned_to.all()
        return [user.username for user in assigned_to_users]
    class Meta:
        model = Task
        fields = ['id', 'job', 'title', 'description', 'assigned_to','assigned_persion', 'created_by','updated_at']

class TaskFilterSerializer(serializers.Serializer):
    startDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'])
    endDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'])


class CreatedBySerializer(serializers.Serializer):
    created_by = serializers.CharField()
    tasks = TaskSerializer(many=True)