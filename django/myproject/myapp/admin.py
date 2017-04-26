from django.contrib import admin
from myproject.myapp.models import RFSN, RecordingModel, SessionModel
admin.site.register(RFSN)
admin.site.register(RecordingModel)
admin.site.register(SessionModel)
# Register your models here.
