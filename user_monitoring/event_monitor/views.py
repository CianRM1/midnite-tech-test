# from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def event_handler(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action_type = data.get("type")
            amount = float(data.get("amount"))
            timestamp = data.get("time")
            user_id = data.get("user_id")

            alerts = []
            if action_type == "withdraw" and amount > 100:
                alerts.append(1100)

            response_data = {
                "alert": bool(alerts),
                "alert_codes": alerts,
                "user_id": user_id,
            }
            return JsonResponse(response_data, status=200)

        except (json.JSONDecodeError, KeyError, ValueError):
            return JsonResponse({"error": "Invalid input data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
