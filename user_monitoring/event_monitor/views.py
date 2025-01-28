import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .alert_checker import check_alerts


@csrf_exempt
def event_handler(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            action_type = data.get("type")
            amount = float(data.get("amount"))
            timestamp = data.get("time")

            # Check action for potential alerts
            alerts = check_alerts(user_id, action_type, amount, timestamp)

            response_data = {
                "alert": bool(alerts),
                "alert_codes": alerts,
                "user_id": user_id,
            }
            return JsonResponse(response_data, status=200)

        except (json.JSONDecodeError, KeyError, ValueError):
            return JsonResponse({"error": "Invalid input data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
