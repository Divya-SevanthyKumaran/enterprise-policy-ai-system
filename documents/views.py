from django.shortcuts import render, redirect, get_object_or_404
from documents.processor import split_documents, store_chunks, load_extract
from documents.models import PolicyDocument, DocumentChunk
from documents.forms import PolicyForm

def upload_document(request):
    form = PolicyForm()
    if request.method=='POST':
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
           uploaded_document = form.save()
           document = uploaded_document.file_reference.path
           load = load_extract(document)
           split = split_documents(load)
           store_chunks(split, uploaded_document)
           
           return redirect('upload_policy')
    return render(request, 'upload_policy.html', {'form' : form} )
       
def list_documents(request):
    queryset = PolicyDocument.objects.all()         
    context = {
        "documents" : queryset
    }
    return render(request, 'view_policies.html', context)

def delete_document(request, pk):
    document = get_object_or_404(PolicyDocument, pk=pk)
    DocumentChunk.objects.filter(policy_document=document).delete()
    document.delete()
    return redirect('view_policies')          
    
def update_document(request, pk):
    document = get_object_or_404(PolicyDocument, pk=pk)
    form = PolicyForm(instance=document)
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
           updated_document = form.save()
           DocumentChunk.objects.filter(policy_document = document).delete()
           file_path = updated_document.file_reference.path
           load = load_extract(file_path)
           split = split_documents(load)
           store_chunks(split, updated_document)
           return redirect('view_policies') 
    return render(request, 'update_document.html', {'form' : form} )            
