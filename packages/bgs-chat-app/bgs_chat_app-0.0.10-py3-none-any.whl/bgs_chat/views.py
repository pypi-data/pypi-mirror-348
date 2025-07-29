from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bgs_chat.common.api_calls import DirectLineAPI
import json


# TODO: this currently uses CSRF exempt - should consider replacing or mitigating against CSSA if we're going to use these
@csrf_exempt
def init_conversation(request):
    if request.method == "POST":
        # needed?
        # body = json.loads(request.body)
        bot = DirectLineAPI()
        response = bot.init_conversation()
        return JsonResponse({"response": response}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def send_message(request):
    if request.method == "POST":
        decoded = request.body.decode('utf-8')
        body = json.loads(decoded)
        message = body.get('message')

        if not message:
            return JsonResponse({"error": "Missing message"}, status=400)

        bot = DirectLineAPI()
        result = bot.send_message(message)

        return JsonResponse({"status": "sent", "result": result})

    return JsonResponse({"error": "Method not allowed"}, status=405)


def get_messages(request):
    bot = DirectLineAPI()
    messages = bot.get_response()
    return JsonResponse({"messages": messages})