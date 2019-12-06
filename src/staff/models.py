from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from src.departments.models import Department


class CustomGroup(Group):

    class Meta:
        proxy = True


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    photo = models.ImageField(
        upload_to="profile/",
        max_length=255,
        null=True,
        blank=True,
        default="",
    )
    phone = models.CharField(max_length=20, blank=True, default="", null=True)
    bio = models.TextField(blank=True, default="", null=True)
    group = models.ManyToManyField(CustomGroup)
    role = models.CharField(max_length=30, default='')
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='department')

    def __str__(self):
        return self.user.username

    @classmethod
    def get_users_of_department(cls, id):
        return cls.objects.filter(department_id=id)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
