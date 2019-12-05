# coding: utf-8

"""
多媒体文件，移植的 n.d.media
"""

from django.db import models

import os

class FileManager(models.Manager):
    pass

class AbstractFile(models.Model):
    class Meta:
        abstract = True

    objects = FileManager()

    STORAGE_ROOT = 'files'

    owner = models.ForeignKey('auth.User', models.SET_NULL, null=True)
    key = models.CharField(max_length=128, unique=True)
    local_path = models.TextField()
    filename = models.TextField()
    title = models.TextField()
    content_type = models.TextField()
    size = models.IntegerField()
    md5sum = models.TextField()
    bucket = models.TextField()
    deleted_at = models.DateTimeField(null=True)

    @classmethod
    def gen_local_path(cls, **kwargs):
        key = kwargs.get('key')
        filename = kwargs.get('filename')
        ext = os.path.splitext(filename)[1]
        return '%s/%s/%s' % (key[:2], key, ext)

    def url(self, request=None, absolute_uri=False):
        url = os.path.join(settings.MEDIA_URL, self.STORAGE_ROOT, self.bucket, self.local_path)
        return url if (not request or not absolute_uri) else request.build_absolute_uri(url)

    def download_url(self, request=None, absolute_uri=False):
        return None

    @property
    def local_abs_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.STORAGE_ROOT, self.bucket, self.local_path)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def serialize(self, to_dict=True, request=None, absolute_uri=False):
        data = dict(
                id = self.id,
                owner = dict(id=self.owner_id),
                key = self.key,
                filename = self.filename,
                title = self.title,
                content_type = self.content_type,
                size = self.size,
                md5sum = self.md5sum,
                bucket = self.bucket,
                url = self.url(request, absolute_uri),
                download_url = self.download_url(request, absolute_uri),
                )

        return data if to_dict else json.dumps(data, ensure_ascii=False)

class Image(AbstractFile):
    class Meta:
        db_table = 'y_media_image'

    STORAGE_ROOT = 'images'

    def download_url(self, request=None, absolute_uri=False):
        url = reverse('download-image', kwargs=dict(key=self.key))
        return url if (not request or not absolute_uri) else request.build_absolute_uri(url)
