from django.shortcuts import render, redirect
from vectorstore.forms import QuestionForm
from rag.pipeline import run_agent

def run_query(request):
    result = None
    chat_history = request.session.get("chat_history", [])
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data.get("question")
            result = run_agent(question, chat_history)
            chat_history.append({
                "role" : "user",
                "content" : question
            })
            chat_history.append({
                "role" : "AI",
                "content" : result
            })
            request.session["chat_history"] = chat_history
            print(chat_history)
    else :
        form = QuestionForm()
    return render(request, "chat.html", {'form' : form, 'answer' : result, 'chat_history' : chat_history})

def clear_chat(request):
    request.session["chat_history"] = []
    return redirect('ask')
