from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    content = models.TextField(verbose_name='Article contents')
    img = models.ImageField(upload_to='blog_previews/', null=True, blank=True, verbose_name='Image')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    views_count = models.IntegerField(default=0, verbose_name='number of views')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.title}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
