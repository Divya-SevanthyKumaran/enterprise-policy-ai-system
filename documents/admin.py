from django.contrib import admin
from .models import PolicyDocument
from .models import DocumentChunk

admin.site.register(PolicyDocument)
admin.site.register(DocumentChunk)
# Register your models here.
