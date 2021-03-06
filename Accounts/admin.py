from django.contrib import admin
from .models import studentDetails, tutorDetails, tutorSubjectDetails, studentTutorRelation, tutorStudentRelation, tutorRequestPending, studentRequestFulfilled
from .models import studentRequestPendingPayment, studentRequestRejected, teacherReview, newStudentTable, newTutorTable
# Register your models here.

admin.site.register(studentDetails)
admin.site.register(tutorDetails)
admin.site.register(tutorSubjectDetails)
admin.site.register(studentTutorRelation)
admin.site.register(tutorStudentRelation)
admin.site.register(studentRequestFulfilled)
admin.site.register(tutorRequestPending)
admin.site.register(studentRequestRejected)
admin.site.register(studentRequestPendingPayment)
admin.site.register(teacherReview)
admin.site.register(newStudentTable)
admin.site.register(newTutorTable)
