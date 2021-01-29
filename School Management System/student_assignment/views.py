from django.shortcuts import render, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.urls import reverse
from django.contrib import messages
from django.http import Http404


from student_management_app.models import Classes, Subjects, Staffs
from .forms import assignmentFileForm
from .models import assignment, assignment_files



def add_assignment(request):
    context ={}
    try:

        teacher_id = Staffs.objects.get(admin=request.user)
    except:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        
        class_id = request.POST['class_id']
        try:
            class_instance = Classes.objects.get(id=class_id)
        except Classes.DoesNotExist:
            messages.error(request, 'select the right class')
        
        subject_id = request.POST['subject_id']
        try:
            sub_instance = Subjects.objects.get(pk=subject_id)
        except Subjects.DoesNotExist:
            messsages.error(request, 'Select the right Subject')
        title = request.POST['title']
        description = request.POST['description']
        assignments = assignment.objects.create(class_id=class_instance, teacher_id=teacher_id,subject_id=sub_instance, title=title, description=description )
        assignments.save()
        messages.success(request, 'Assignent Added successfully.')
        return HttpResponseRedirect(reverse('add_assignment_files', kwargs={'id': assignments.id}))


    context['classes'] = Classes.objects.all()
    context['subjects'] = Subjects.objects.all()
    context['assignments'] = assignment.objects.filter(teacher_id = teacher_id)

    return render(request,'add_assignment_template.html', context)


def edit_assignment(request, id):
    context = {}
    try:
        assinment_instance = assignment.objects.get(id=id)
    except assignment_files.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        
        class_id = request.POST['class_id']
        try:
            assinment_instance.class_id = Classes.objects.get(id=class_id)
        except Classes.DoesNotExist:
            messages.error(request, 'select the right class')
        
        subject_id = request.POST['subject_id']
        try:
            assinment_instance.subject_id = Subjects.objects.get(pk=subject_id)
        except Subjects.DoesNotExist:
            messsages.error(request, 'Select the right Subject')
        assinment_instance.title = request.POST['title']
        assinment_instance.description = request.POST['description']
        assinment_instance.save()
        messages.success(request, 'Assignent Added successfully.')
        return HttpResponseRedirect(reverse('add_assignment'))
    context['assinment_instance'] = assinment_instance
    context['classes'] = Classes.objects.all()
    context['subjects'] = Subjects.objects.all()
    return render(request, 'edit_assignment_template.html', context)


def delete_assignment(request, id):
    try:
        assinment_instance = assignment.objects.get(id=id).delete()
        messages.success(request,'Assignment deleted successful.')
        return HttpResponseRedirect(reverse('add_assignment'))
    except assignment_files.DoesNotExist:
        raise Http404()




def add_assignment_files(request, id):
    context = {}
    try:
        assinment_instance = assignment.objects.get(id=id)
    except:
        messages.error(request, 'Assignment Error')

    if request.method == 'POST':
        files = request.FILES.get('assignmnt_file') 
        assinment_file_instance = assignment_files.objects.create(assignment_id=assinment_instance, assignmnt_file=files)
        assinment_file_instance.save()
        messages.success(request, 'Assignmnt file Uploaded successfull.')
    context['files'] = assignment_files.objects.filter(assignment_id=assinment_instance)
    context['assignment'] = assinment_instance
    return render(request, 'add_assignment_file.html', context)


def delete_assignment_files(request, id):
    try:
        assignments = assignment_files.objects.get(id=id)
        ids = assignments.assignment_id.id
        assignments.delete()
        return HttpResponseRedirect(reverse('add_assignment_files', kwargs={'id': ids}))
    except assignment_files.DoesNotExist:
        raise Http404()



















