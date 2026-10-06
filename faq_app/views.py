from django.http import JsonResponse
from django.shortcuts import render

from .chatbot import get_answer


def chat_page(request):
    return render(request, "faq_app/chat.html")


def ask(request):
    question = request.GET.get("q", "").strip()
    if not question:
        return JsonResponse({"answer": "Please type a question."})
    answer, score = get_answer(question)
    return JsonResponse({"answer": answer})