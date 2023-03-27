from django.db import models

# Create your models here.


class Bug(models.Model):

    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    text = models.TextField()
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return "/bug/%i" % self.id


class User(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return "/person/%i" % self.id

    def open_bug_count(self):
        return Bug.objects.filter(owner=self, closed=False).count()

    def __str__(self):
        return self.name
