# interview/admin.py
from django.contrib import admin
from .models import Company,Subject, Topic,Tutorial, Question, Answer

admin.site.register(Company)
admin.site.register(Subject)
admin.site.register(Topic)

admin.site.register(Question)
admin.site.register(Answer)

from .forms import TutorialForm

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    form = TutorialForm  # কাস্টম ফর্ম ব্যবহার করা হচ্ছে
    list_display = [ 'title','serial_number', 'topic','level', 'company', 'created_at']  # ফিল্ড প্রদর্শন
    list_filter = ['topic', 'company']  # ফিল্টার যোগ করা
    search_fields = ['title', 'topic__name', 'company__name']  # অনুসন্ধান সক্ষম