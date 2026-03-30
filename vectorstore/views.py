from django.shortcuts import render
from vectorstore.embeddings import embed_query
from vectorstore.forms import QuestionForm
from vectorstore.pinecone_store import search_chunks

def ask_question(request):
    answer = None
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]
            result_chunk = search_chunks(question)
            
            texts = []
            for txt in result_chunk["matches"]:
                text = txt["metadata"]["text"]
                texts.append(text)
            context = "\n".join(texts)
    else:
        form = QuestionForm()

    return render(request, "ask.html", {"form": form, "answer": context})
        
        
        
    
    