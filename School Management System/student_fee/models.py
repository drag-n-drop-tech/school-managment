from django.db import models
from student_management_app.models import Students

class fees_data(models.Model):
    fee_type = models.CharField(max_length=100)
    fee_description = models.TextField(null=True,blank=True)
    fee_amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fee_type

def generateInvNumber():
    import datetime
    now = datetime.datetime.now()
    uid = fees_collection.objects.aggregate(Max('id'))
    uid = uid['id__max'] 
    if uid == None:
        uid = 0
    return 'INV'+ str(now.year) +'-'+ str(uid+1)

class fees_collection(models.Model):
    inv_number = models.CharField(max_length=25,default=generateInvNumber)
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    total_amt=models.DecimalField(max_digits=10,decimal_places=2)
    payment_type = models.CharField(max_length=10)
    payment_mode = models.CharField(max_length=10)
    tax_percent = models.DecimalField(max_digits=10,decimal_places=2)
    tax_amt = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    net_amount = models.DecimalField(max_digits=10,decimal_places=2)
    paid_amt = models.DecimalField(max_digits=10,decimal_places=2)
    balance_amt = models.DecimalField(max_digits=10,decimal_places=2)
    payment_status = models.CharField(max_length=10,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=25,default="Anonymous")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=25,default="Anonymous")

class fees_collection_items(models.Model):
    fees_collection_id = models.ForeignKey(fees_collection,on_delete=models.CASCADE)
    fee_type = models.ForeignKey(fees_data,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=25,default="Anonymous")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=25,default="Anonymous")



    