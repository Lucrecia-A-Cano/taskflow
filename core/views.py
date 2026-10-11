from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})

def version(request):
       return JsonResponse({"version": "0.1.0"})

