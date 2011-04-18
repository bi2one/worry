from django.db import models
from worry.document.models import Document
# Create your models here.


class File(models.Model) :
    def __unicode__(self) :
        return self.file_name
    document = models.ForeignKey(Document, null=True)
    file_type = models.PositiveSmallIntegerField()

    file_size = models.PositiveIntegerField()
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
