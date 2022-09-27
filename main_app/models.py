from django.db import models
from .validators import validate_pincode,validate_lat_longitude


	



class vender(models.Model):
	name=models.CharField(max_length=50)
	address=models.TextField(default='none')
	image_url=models.CharField(max_length=300,default='https://imgs.search.brave.com/Wmgf1m-wbgzOgdfoZcSGBb5C7baYyA-_V99Okq6dyro/rs:fit:256:225:1/g:ce/aHR0cHM6Ly90c2U0/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5m/TWVtTUdKTklQZDVm/TFRJNlR3SndRSGFI/YSZwaWQ9QXBp')
	city=models.CharField(max_length=30,default='none')
	state=models.CharField(max_length=30,default='none')
	pin_code=models.CharField(max_length=10,default='none')
	lat_longitude=models.CharField(max_length=30,default='none')
	

	def __str__(self):
		return self.name

class product_class(models.Model):
	name=models.CharField(max_length=100)
	parent=models.IntegerField()
	class_img_url=models.URLField(max_length=300, null=True,blank=True)

	def __str__(self):
		return self.name


                                                 
class Products(models.Model):
	name=models.CharField(max_length=250)
	price=models.IntegerField()
	description=models.TextField()
	vender=models.ForeignKey(vender, on_delete=models.CASCADE)
	pclass=models.ManyToManyField(product_class, null=True,blank=True)
	date_time=models.DateTimeField()
	Availability=models.BooleanField("Is_avilable",default=True)
	p_img=models.ImageField(upload_to="images",null=True,blank=True)
	reviews=models.CharField(max_length=30,default='0,0,0,0,0')
	average_ratings=models.DecimalField(max_digits=5, decimal_places=2,default=0)
	no_of_ratings=models.IntegerField(default=0)

	def __str__(self):
		return self.name



class users(models.Model):
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=50)
	address=models.TextField()
	city=models.CharField(max_length=30,default='none')
	state=models.CharField(max_length=30,default='none')
	pin_code=models.CharField(max_length=10,default='none')
	lat_longitude=models.CharField(max_length=30,default='none')
	order_history=models.ManyToManyField(Products,null=True,blank=True,related_name='orders_h')
	b_history=models.ManyToManyField(Products,null=True,blank=True,related_name='brouser_h')
	cart=models.ManyToManyField(Products,null=True,blank=True)

	def __str__(self):
		return self.username
	


class comments(models.Model):
	auther=models.CharField(max_length=50)
	Text=models.TextField()
	parent=models.ForeignKey( Products, on_delete=models.CASCADE)
	likes=models.IntegerField(default=0)
	date_time=models.DateTimeField()
	rating=models.IntegerField(default=5)
	

	def __str__(self):
		return self.auther

class orders(models.Model):
	product_id=models.IntegerField()
	vender_id=models.IntegerField()
	users_id=models.IntegerField()
	order_time=models.DateTimeField()
	




class chat(models.Model):
	users_id=models.IntegerField()
	username=models.CharField(max_length=50)
	vender_id=models.IntegerField(null=True)
	Text=models.CharField(max_length=300)
	date_time=models.CharField(max_length=30,default='none')

class imges(models.Model):
	parent=models.ForeignKey(Products, on_delete=models.CASCADE)
	img=models.ImageField(upload_to='images')






