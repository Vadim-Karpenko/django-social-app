from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from sorl.thumbnail import delete as delete_thumbnails

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created')
    title = models.CharField(max_length=240)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True, db_index=True, blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    users_view = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_viewed',
                                        blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id])

    def clear_thumbnails(self):
        delete_thumbnails(self.image)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments_created')
    image = models.ForeignKey(Image, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.get_full_name, self.image)
