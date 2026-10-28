import csv
import json
import logging
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from core.models import Task

# Logger que guarda los mensajes en el archivo import.log
logger = logging.getLogger("import_tasks")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler("import.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)


class Command(BaseCommand):
    help = "Importa tareas desde múltiples proveedores (JSON, CSV, XML)"

    def handle(self, *args, **options):
        total = 0
        total += self._import_json("data/tasks_provider_a.json", source="proveedor_a")
        total += self._import_csv("data/tasks_provider_b.csv", source="proveedor_b")
        total += self._import_xml("data/tasks_provider_c.xml", source="proveedor_c")
        total += self._import_json("data/tasks_provider_d.json", source="proveedor_d")
        self.stdout.write(self.style.SUCCESS(f"Importación finalizada: {total} tareas cargadas"))

    def _import_json(self, path, source):
        count = 0
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                self._crear_task(item, source)
                count += 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error importando {path}: {e}")
        return count

    def _import_csv(self, path, source):
        count = 0
        try:
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self._crear_task(row, source)
                    count += 1
        except FileNotFoundError as e:
            logger.error(f"Error importando {path}: {e}")
        return count

    def _import_xml(self, path, source):
        count = 0
        try:
            tree = ET.parse(path)
            for task_el in tree.getroot().findall("task"):
                item = {
                    "title": task_el.find("title").text,
                    "priority": task_el.find("priority").text,
                    "status": task_el.find("status").text,
                }
                self._crear_task(item, source)
                count += 1
        except (FileNotFoundError, ET.ParseError) as e:
            logger.error(f"Error importando {path}: {e}")
        return count

    def _crear_task(self, item, source):
        if not item.get("title"):
            logger.warning(f"Item sin título, se ignora (proveedor: {source}): {item}")
            return
        Task.objects.create(
            title=item["title"],
            priority=item.get("priority", "media"),
            status=item.get("status", "pendiente"),
            source=source,
        )
