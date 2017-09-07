from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    date_of_birth = models.DateField('Your date of birth (YYYY-MM-DD)', blank=True, null=True)
    photo = models.ImageField('', upload_to='users/%Y/%m/%d', default='users/default-photo.jpg')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} folows {}'.format(self.user_from, self.user_to)

# Add following field to User dynamically
User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))