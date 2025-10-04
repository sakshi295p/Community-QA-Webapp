from django.contrib import admin
from QandA.models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Badges)
admin.site.register(Comments)
admin.site.register(PostHistory)
admin.site.register(PostLinks)
admin.site.register(Posts)
admin.site.register(Tags)
admin.site.register(Votes)