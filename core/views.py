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
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .repositories import TaskRepository
from .serializers import ProjectSerializer, TaskSerializer
from .services import TaskService


def health_check(request):
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})


def version(request):
    return JsonResponse({"version": "0.1.0"})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskRepository.get_queryset()
    serializer_class = TaskSerializer
    filterset_fields = ["status", "priority", "project"]
    ordering_fields = ["due_date", "created_at", "priority"]
    search_fields = ["title", "description"]

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        TaskService.mark_completed(task)
        return Response(self.get_serializer(task).data)

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        tasks = TaskService.tasks_overdue(self.get_queryset())
        page = self.paginate_queryset(tasks)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(tasks, many=True).data)