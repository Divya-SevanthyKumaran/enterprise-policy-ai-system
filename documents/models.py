from django.db import models

# Create your models here.
class PolicyDocument(models.Model):
    policy_title = models.CharField(max_length=50)
    department = models.CharField(max_length=30)
    file_reference = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.policy_title
    
class DocumentChunk(models.Model):
    policy_document = models.ForeignKey("documents.PolicyDocument", on_delete=models.CASCADE)
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    
    def __str__(self):
        return f"{self.policy_document} = Chunk {self.chunk_index}"