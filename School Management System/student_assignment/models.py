from django.db import models
from student_management_app.models import Classes,Students,Staffs,Subjects

class assignment(models.Model):
    class_id = models.ForeignKey(Classes,on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class assignment_files(models.Model):
    assignment_id = models.ForeignKey(assignment,on_delete=models.CASCADE)
    assignmnt_file = models.FileField(upload_to='assignments/%Y-%m-%d')

class assignment_submission(models.Model):
    assignment_id = models.ForeignKey(assignment,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class assignment_submission_files(models.Model):
    assignment_submission_id = models.ForeignKey(assignment_submission,on_delete=models.CASCADE)
    assignmnt_file = models.FileField(upload_to='assignments_submissions/%Y-%m-%d')

