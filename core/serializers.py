from datetime import date
from rest_framework import serializers
from .models import Project, Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description",
            "priority", "status", "due_date", "tags", "created_at",
        ]

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("La fecha límite no puede ser en el pasado.")
        return value

    def validate(self, data):
        # Regla 1: completada requiere fecha límite
        if data.get("status") == "completada" and not data.get("due_date"):
            raise serializers.ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )

        # Regla 2: en_progreso requiere al menos una tarea completada en el proyecto
        status = data.get("status", self.instance.status if self.instance else None)
        project = data.get("project", self.instance.project if self.instance else None)

        if status == "en_progreso" and project:
            completadas = Task.objects.filter(project=project, status="completada")
            if self.instance:
                completadas = completadas.exclude(pk=self.instance.pk)
            if not completadas.exists():
                raise serializers.ValidationError(
                    "No se puede poner en progreso una tarea si el proyecto no tiene ninguna tarea completada todavía."
                )

        return data


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]

