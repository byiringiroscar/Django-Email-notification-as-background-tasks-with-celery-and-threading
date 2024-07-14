from django.contrib import admin
from .models import MessageBoard, Message

# Register your models here.


admin.site.register(MessageBoard)
admin.site.register(Message)