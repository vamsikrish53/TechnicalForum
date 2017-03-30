from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Tag_Question_Link)

