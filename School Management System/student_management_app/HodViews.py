from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from student_management_app.models import CustomUser,Parents, Staffs, Classes, Subjects, Students,  FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport
from .forms import AddStudentForm, EditStudentForm, NewStudentForm, day_option_form


def admin_home(request):
    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    class_count = Classes.objects.all().count()
    staff_count = Staffs.objects.all().count()

    # Total Subjects and students in Each class
    class_all = Classes.objects.all()
    class_name_list = []
    subject_count_list = []
    student_count_list_in_class = []

    for single_class in class_all:
        # subjects = Subjects.objects.filter(class_id=single_class.id).count()
        students = Students.objects.filter(ClassNo=single_class.id).count()
        class_name_list.append(single_class.class_name)
        # subject_count_list.append(subjects)
        student_count_list_in_class.append(students)
    
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        # single_class = Classes.objects.get(id=subject.class_id.id)
        # student_count = Students.objects.filter(ClassNo=single_class.id).count()
        subject_list.append(subject.subject_name)
        # student_count_list_in_subject.append(student_count)
    
    # For Saffs
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]

    staffs = Staffs.objects.all()
    for staff in staffs:
        # subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        # attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        # staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        # student_name_list.append(student.admin.first_name)


    context={
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "class_count": class_count,
        "staff_count": staff_count,
        "class_name_list": class_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_class": student_count_list_in_class,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')



def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')




def add_class(request):
    return render(request, "hod_template/add_class_template.html")


def add_class_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_class')
    else:
        single_class = request.POST.get('class_name')
        try:
            class_model = Classes(class_name=single_class)
            class_model.save()
            messages.success(request, "class Added Successfully!")
            return redirect('add_class')
        except:
            messages.error(request, "Failed to Add class!")
            return redirect('add_class')


def manage_class(request):
    classes = Classes.objects.all()
    context = {
        "classes": classes
    }
    return render(request, 'hod_template/manage_class_template.html', context)


def edit_class(request, class_id):
    single_class = Classes.objects.get(id=class_id)
    context = {
        "class": single_class,
        "id": class_id
    }
    return render(request, 'hod_template/edit_class_template.html', context)


def edit_class_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        class_id = request.POST.get('class_id')
        class_name = request.POST.get('class_name')

        try:
            single_class = Classes.objects.get(id=class_id)
            single_class.class_name = class_name
            single_class.save()

            messages.success(request, "class Updated Successfully.")
            return redirect('/edit_class/'+class_id)

        except:
            messages.error(request, "Failed to Update class.")
            return redirect('/edit_class/'+class_id)


def delete_class(request, class_id):
    single_class = Classes.objects.get(id=class_id)
    try:
        single_class.delete()
        messages.success(request, "class Deleted Successfully.")
        return redirect('manage_class')
    except:
        messages.error(request, "Failed to Delete class.")
        return redirect('manage_class')


def add_student(request):
    form = NewStudentForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = NewStudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # address = form.cleaned_data['address']
            # session_year_id = form.cleaned_data['session_year_id']
            # class_id = form.cleaned_data['class_id']
            # gender = form.cleaned_data['gender']

            # # Getting Profile Pic first
            # # First Check whether the file is selected or not
            # # Upload only if file is selected
            # if len(request.FILES) != 0:
            #     profile_pic = request.FILES['profile_pic']
            #     fs = FileSystemStorage()
            #     filename = fs.save(profile_pic.name, profile_pic)
            #     profile_pic_url = fs.url(filename)
            # else:
            #     profile_pic_url = None


            # try:
            #     user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            #     user.students.address = address

            #     class_obj = Classes.objects.get(id=class_id)
            #     user.students.class_id = class_obj


            #     user.students.gender = gender
            #     user.students.profile_pic = profile_pic_url
            #     user.save()
            # except:
            #     messages.error(request, "Failed to Add Student!")
            #     return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(id=student_id)
    form = EditStudentForm(request.POST or None, instance=student)
    if request.method == 'POST':
        print('I am her e')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage_student'))
        else:
            print(form.errors())
            return HttpResponse('Form is not valid')
    # Filling the form with Data from Database
    # form.fields['email'].initial = student.admin.email
    # form.fields['username'].initial = student.admin.username
    # form.fields['first_name'].initial = student.admin.first_name
    # form.fields['last_name'].initial = student.admin.last_name
    # form.fields['address'].initial = student.address
    # form.fields['class_id'].initial = student.class_id.id
    # form.fields['gender'].initial = student.gender
    # form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "name": student.full_name,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            class_id = form.cleaned_data['class_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                clindividual_class = Classes.objects.get(id=class_id)
                student_model.class_id = clindividual_class


                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(id=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    classes = Classes.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "classes": classes,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)



def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')
        try:
            subject = Subjects(subject_name=subject_name)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    context = {
        "subject": subject,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)



def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    classes = Classes.objects.all()
    context = {
        "classes": classes,
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    class_no = request.POST.get("ClassNo")
    # session_year = request.POST.get("session_year_id")
    print(class_no)
    # Students enroll to class, class has Subjects
    # Getting all data from subject model based on subject_id
    class_model = Classes.objects.get(id=class_no)

    list_data = []
    attendance = Attendance.objects.filter(ClassNo = class_model) 
    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date)}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def staff_profile(request):
    pass


def student_profile(requtest):
    pass

def addParent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone=request.POST['phone']
        password=request.POST['password']
        parent_name=request.POST['parent_name']
        photo=request.FILES.get('photo')
        address=request.POST['address']
        occupation=request.POST['occupation']
        if len(phone) == 0 or len(password) == 0:
            messages.error(request, 'Phone Number and password compulsory')
            return redirect('newParent')
        if len(phone) != 10:
            messages.error(request, 'Phone Number is not valid')
            return redirect('newParent')
        parent=CustomUser.objects.create_user(username=phone, password=password)
        parent= Parents(parent_email=email, user=parent, parent_name=parent_name, photo=photo, address=address, occupation=occupation)
        parent.save()
        messages.success(request, 'New Parent added successfuly.')


    return render(request, 'hod_template/addparent.html')




def addStudent(request):
    if request.method == 'POST':
        pass

    return render(request, 'hod_template/addStudent.html')

def add_timetable(request):
    context ={
        'form': day_option_form()
    }
    context['classes'] = Classes.objects.all()
    context['subjects'] = Subjects.objects.all()
    context['staffs'] = Staffs.objects.all()
    return render(request,'hod_template/student_timetable_add_template.html', context)





