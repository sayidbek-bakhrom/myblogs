from django.db import models
from django.contrib.auth.models import User
import random
from PIL import Image

avatars = ['image1', 'image2', 'image3']
random_avatar = random.choice(avatars)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField('Profile Image', upload_to='avatars/', default=f'{random_avatar}.png')

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
