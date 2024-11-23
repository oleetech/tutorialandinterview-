from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone



# কোম্পানি মডেল
class Company(models.Model):
    name = models.CharField(max_length=255)  # কোম্পানির নাম
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # কোম্পানি তৈরি হওয়ার সময়

    def __str__(self):
        return self.name


# বিষয় মডেল (Subject)
class Subject(models.Model):
    name = models.CharField(max_length=255)  # বিষয়ের নাম (যেমন: Python)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="subjects")  # কোম্পানির সাথে সম্পর্ক
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class TopicManager(models.Manager):
    def active(self):
        """Returns only the topics that are not deleted."""
        return self.filter(is_deleted=False)

    def deleted(self):
        """Returns only the topics that are marked as deleted."""
        return self.filter(is_deleted=True)
    
# টপিক মডেল (Topic)
class Topic(models.Model):
    name = models.CharField(max_length=255)  # টপিকের নাম (যেমন: Variables and Data Types)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")  # বিষয়ের সাথে সম্পর্ক
    created_at = models.DateTimeField(auto_now_add=True)
    # Soft delete fields
    is_deleted = models.BooleanField(default=False)  # Flag to indicate deletion
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp for soft deletion
    objects = TopicManager()  # Custom manager for active and deleted topics
    def soft_delete(self):
        """Mark the topic as deleted and set the deletion timestamp."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore the soft-deleted topic."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

class Tutorial(models.Model):
    title = models.CharField(max_length=255)  # টিউটোরিয়াল এর শিরোনাম
    level = models.CharField(  # প্রশ্নের লেভেল
        max_length=20,
        choices=[('Basic', 'Basic'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Basic'
    )
    content =  CKEditor5Field('Content')  # টিউটোরিয়াল এর মূল বিষয়বস্তু
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="tutorials")  # টপিকের সাথে সম্পর্ক
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="tutorials")  # কোম্পানির সাথে সম্পর্ক
    serial_number = models.FloatField()  # সিরিয়াল নম্বর
    created_at = models.DateTimeField(auto_now_add=True)  # তৈরি করার সময়
    # Attach SEO metadata to the model
    class Meta:
        ordering = ['serial_number']  # ডিফল্টভাবে সিরিয়াল নম্বর অনুযায়ী সাজানো হবে

    def __str__(self):
        return f"{self.serial_number}. {self.title} ({self.topic.name})"


# প্রশ্ন মডেল (Question)
class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('CODE', 'Code-based Question'),
        ('TEXT', 'Text-based Question'),
    ]

    title = models.TextField()  # প্রশ্নের টেক্সট
    question_type = models.CharField(  # প্রশ্নের ধরন
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        default='TEXT'
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")  # টপিকের সাথে সম্পর্ক
    tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, related_name="questions", null=True, blank=True)  # টিউটোরিয়াল এর সাথে সম্পর্ক

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="questions")  # কোম্পানির সাথে সম্পর্ক
    level = models.CharField(  # প্রশ্নের লেভেল
        max_length=20,
        choices=[('Basic', 'Basic'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Basic'
    )
    example_code = models.TextField(blank=True, null=True)  # কোড উদাহরণ (যদি থাকে)
    correct_answer = models.TextField(blank=True, null=True)  # সঠিক উত্তর বা সঠিক কোড
    tags = models.CharField(max_length=255, blank=True, null=True)  # প্রশ্নের ট্যাগ বা কীওয়ার্ড
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.topic.name})"

# উত্তর মডেল (Answer)
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")  # প্রশ্নের সাথে সম্পর্ক
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")  # ব্যবহারকারী (উত্তর দাতা)
    answer_text = models.TextField(blank=True, null=True)  # টেক্সট ভিত্তিক উত্তর (যেমন ব্যাখ্যা বা কোড)
    mcq_answer = models.CharField(max_length=255, blank=True, null=True)  # MCQ এর জন্য উত্তর
    is_correct = models.BooleanField(default=False)  # সঠিক উত্তর কিনা
    submitted_at = models.DateTimeField(auto_now_add=True)  # উত্তর জমা দেওয়ার সময়

    def __str__(self):
        return f"Answer by {self.user.username} for {self.question.title}"


# ব্যবহারকারীর প্রোফাইল মডেল (UserProfile)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # ডিফল্ট ব্যবহারকারী মডেলের সাথে সংযোগ
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")  # ব্যবহারকারীর কোম্পানি
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # ফোন নম্বর
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.company.name})"
