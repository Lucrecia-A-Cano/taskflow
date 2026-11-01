#from django.http import JsonResponse
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
#from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.shortcuts import get_object_or_404

#def health_check(request):
#    return JsonResponse({"status": "ok", "service": "TaskFlow API"})


#def version(request):
#    return JsonResponse({"version": "0.1.0"})


#@api_view(["GET"])
#def project_list(request):
#    projects = Project.objects.all()
#    serializer = ProjectSerializer(projects, many=True)
#   return Response(serializer.data)


#def task_list(request):
#    tasks = Task.objects.select_related("project").prefetch_related("tags").all()
#    serializer = TaskSerializer(tasks, many=True)
#    return Response(serializer.data)

#@api_view(["GET"])
#def project_detail(request, project_id):
#    project = get_object_or_404(Project, pk=project_id)
#    serializer = ProjectSerializer(project)
#    return Response(serializer.data)

from django.http import JsonResponse
from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


def health_check(request):
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})


def version(request):
    return JsonResponse({"version": "0.1.0"})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("project").prefetch_related("tags").all()
    serializer_class = TaskSerializer