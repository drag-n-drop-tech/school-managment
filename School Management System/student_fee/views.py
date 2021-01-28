from django.shortcuts import render
from .models import fees_collection, fees_collection_items, fees_data

def fee_collection(request):
    return render(request,'fee_collection_template.html')

def save_fee_data(request):
    if request.method == 'POST':
        fee_type= request.POST['fee_type']
        description= request.POST['fee_description']
        amounts= request.POST['fee_amount']
        fees_data_instance = fee_amount.objects.create(fee_type=fee_type, fee_description=description, fee_amount=amounts)
        fees_data_instance.save()
        context={}
        context['fees_data'] = fees_data_instance
        return render(request, 'staff_template/add_result_template.html', context)