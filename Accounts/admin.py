from django.contrib import admin
from .models import studentDetails, tutorDetails, tutorSubjectDetails, studentTutorRelation, tutorStudentRelation, tutorRequestPending, studentRequestFulfilled
# Register your models here.

admin.site.register(studentDetails)
admin.site.register(tutorDetails)
admin.site.register(tutorSubjectDetails)
admin.site.register(studentTutorRelation)
admin.site.register(tutorStudentRelation)
admin.site.register(studentRequestFulfilled)
admin.site.register(tutorRequestPending)
