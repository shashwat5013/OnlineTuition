from django.contrib import admin
from .models import studentDetails, tutorDetails, tutorSubjectDetails, studentTeacherRelation, teacherStudentRelation
# Register your models here.

admin.site.register(studentDetails)
admin.site.register(tutorDetails)
admin.site.register(tutorSubjectDetails)
admin.site.register(studentTeacherRelation)
admin.site.register(teacherStudentRelation)
#admin.site.register(requestStudentToTeacher)
