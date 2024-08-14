from django.contrib import admin
from .models import Course
from .models import Group
from .models import User
from .models import Level
from .models import Comment


# Register your models here.
admin.site.register(Course)
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Level)
admin.site.register(Comment)
