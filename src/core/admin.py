from django.contrib import admin
from .models import Course , User , Document , Flashcard
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Document)
admin.site.register(Flashcard)
