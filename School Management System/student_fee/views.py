from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import fees_collection, fees_collection_items, fees_data


def fee_collection(request):
    return render(request,'fee_collection_template.html')

def fee_list(request):
    context = {}
    context['feeTable'] = fees_data.objects.all()

    return render(request, 'student_fee/fee_data_tamplete.html', context)


def new_fee_data(request):
    context = {}
    if request.method == 'POST':
        fee_type= request.POST['fee_type']
        description= request.POST['fee_description']
        amounts= request.POST['fee_amount']
        fees_data_instance = fees_data.objects.create(fee_type=fee_type, fee_description=description, fee_amount=amounts)
        fees_data_instance.save()
        context={}
        context['fees_data'] = fees_data_instance
        messages.success(request, 'New Fee added successful.')

    return render(request, 'student_fee/new_fee_data.html', context)



def update_fee_data(request, id): 
    context={}

    try:
        fee_instance = fees_data.objects.get(pk=id)
        context['fee'] = fee_instance
        print(fee_instance.fee_type)
        if request.method == 'POST':
            fee_instance.fee_type= request.POST.get('fee_type', fee_instance.fee_type)
            fee_instance.fee_description= request.POST.get('fee_description', fee_instance.fee_description)
            fee_instance.fee_amount= request.POST.get('fee_amount', fee_instance.fee_amount)
            # print(fee_instance.amount)
            fee_instance.save()
        
            messages.success(request, 'Fees updated successfully.')
            return HttpResponseRedirect(reverse('fee_list'))
    except fees_data.DoesNotExist:
        messages.error('Data does not matches.')
    
    return render(request, 'student_fee/edit_fee_data.html', context)



def delete_fee_data(request, id):
    try:
        fee_instance = fees_data.objects.get(pk=id).delete()
        messages.success(request, 'Delete Successfull')
        # return render(request, 'base.html')
    except fees_data.DoesNotExist:
        messages.error(request, 'Data does not matches.')

    return HttpResponseRedirect(reverse('fee_list'))

    

def create_fees_collection(request):
    if request.method == 'POST':
        pass
    return HttpResponse('')
