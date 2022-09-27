from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from django.db import connection
import time,jwt,json
import urllib.parse
import datetime
from .forms import user_form
cursor=connection.cursor()

google_api_key='AIzaSyCquryaYKeYy68RF9-_4B5Ln04S4DVuyqA'                 

def mk_token(load):
	token=jwt.encode(payload=load,key='12345678')
	return token

def dictfetchall(cursor):
    desc = cursor.description
    return [                                                              
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]


def add_reviews(x,rating):
	ra=x.split(',')
	ira=[]
	for i in ra:
		ira.append(int(i))
	if rating==1:
		ira[4]=ira[4]+1
	elif rating==2:
		ira[3]=ira[3]+1
	elif rating==3:
		ira[2]=ira[2]+1
	elif rating==4:
		ira[1]=ira[1]+1
	elif rating==5:
		ira[0]=ira[0]+1

	i=0
	s=0
	v=0
	while i<5:
		v=(5-i)*ira[i]+v
		s=s+ira[i]
		i=i+1
	avg=v/s

	rstr=''
	for i in ira:
		rstr=rstr+str(i)+','
	rstr=rstr[:-1]
	rv={'rstr':rstr,'avg':avg,'sum':s}
	return rv



def login_fun(request):
	if request.method!='POST':
		return render(request,'new_login.html')
	else:
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=users.objects.filter(username=username,password=password)
		d=0
		for i in user:
			user_id=i.id
			d=1
		if d==0:
			context={'res':'incorrect username or password'}
			return render(request,'new_login.html',context)
		
		if d==1:
			load={}
			load['user_id']=user_id
			load['username']=username
			load['exp']=time.time()+24*60*60
			token=mk_token(load)
			url_string='http://127.0.0.1:8000/home'
			response=redirect(url_string)
			response.set_cookie('token',token)
			print('login working')
			
			
			return response


def home_fun(request):
	global cursor
	if request.method=='GET':
		token=request.GET.get('token')
		try:
			new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])          
		except Exception:
			return render(request,'login_page.html')

	cursor.execute("SELECT * FROM main_app_products")
	data=dictfetchall(cursor)
	data=json.dumps(data)
	context={'token':token,'data':data}
	return render(request,'home_page.html',context)



def r_api_fun(request):
	if request.method=='GET':
		if request.GET.get('purpose')=='get_review':
			p_id=request.GET.get("products_id")
			print('opop',p_id)
			print('gandalf')
			q=comments.objects.filter(parent__id=p_id)
			data=[]
			for i in q:
				x= i.date_time.strftime('%d-%m-%y')
				
				r={'auther':i.auther,'Text':i.Text,'rating':i.rating,'date_time':x}
				data.append(r)
			#print(data[0])
			data=json.dumps(data)
			return JsonResponse(data,safe=False)

		
	if request.method=='POST':
		tex=datetime.datetime.now()
		print('sorom')

		
		rd=(request.body.decode('utf-8'))
		rd=json.loads(rd)
		if rd['purpose']=='post_reveiw':
			try:
				token=request.COOKIES.get('token')
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
				tn=time.time()
				tt=new_token['exp']
				if tn>tt:
					return render(request,'login_page.html')
			except Exception:
				return render(request,'login_page.html')
			p_id=rd['product_id']
			rating=rd['rating']
			comment=rd['comment']
			comment=comment.strip()
			username=new_token['username']
			comment=comment.replace('"','$%*')
			comment=comment.replace('\r\n','q@#r$')
			parent=Products.objects.get(id=p_id)
			r=parent.reviews
			rv=add_reviews(r,rating)
			rstr=rv['rstr']
			avg=rv['avg']           
			s=rv['sum']
			check=comments.objects.filter(auther=username,parent__id=p_id)
			if 1<=rating<=5 and len(check)==0:
				print('frodo')
				parent.reviews=rstr
				parent.average_ratings=avg
				parent.no_of_ratings=s
				print(rstr,avg,s)
				parent.save(update_fields=['reviews','average_ratings','no_of_ratings'])



			if comment and 1<=rating<=5:
				print('aragon')
				x=comments.objects.create(auther=username,Text=comment,parent=parent,date_time=tex,rating=rating)
			stex=time	
			t=tex.strftime('%d-%m-%y')
			data={'status':200,'auther':username,'date_time':t}
			print('1')
			return JsonResponse(data,safe=False)

def p_api_fun(request):
	if request.method=='GET':
		print('p_api_fun')
		p_id=request.GET.get('product_id')
		q=products.objects.get(id=p_id)
		data=[]
		child_text=q.related_products
		if child_text!='none':
			child=child_text.split(',')
			i=0
			while i<len(child):
				child[i]=int(child[i])
				i=i+1
			i=0
			while i<len(child):
				r=products.objects.get(id=child[i])
				f={'id':child[i],'name':r.name,'description':r.description,'image_url':r.image_url1}
				data.append(f)
				i=i+1
		return JsonResponse(data,safe=False)
	else:
		return HTTPresponse('error in loading')


def order_api_fun(request):
	if request.method=='GET':
		print('order')
		if request.GET.get('purpose')=='order':
			try:
				token=request.COOKIES.get('token')
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
				tn=time.time()
				tt=new_token['exp']
				if tn>tt:
					return render(request,'login_page.html')
			except Exception:
				return render(request,'login_page.html')
			username=new_token['username']
			user_id=new_token['user_id']
			p_id=request.GET.get('product_id')
			q=Products.objects.get(id=p_id)
			u=users.objects.get(id=user_id)
			u.order_history.add(q)
			v_id=q.vender_id

			t=datetime.datetime.now()
			orders.objects.create(product_id=p_id,vender_id=v_id,order_time=t,users_id=user_id)
			print('succesfully')
			data={'status':200,'mes':'order succesfully added to the list'}
			print(data)
			return JsonResponse(data,safe=False)


	
		if request.GET.get('purpose')=='cancel_order':
			print('cancel_order')
			p_id=request.GET.get('')
			try:
				token=request.COOKIES.get('token')
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
				tn=time.time()
				tt=new_token['exp']
				if tn>tt:
					return render(request,'login_page.html')
			except Exception:
				return render(request,'login_page.html')
			
			u_id=new_token['user_id']
			p_id=request.GET.get('product_id')
			p_id=int(p_id.replace('d',''))
			q=Products.objects.get(id=p_id)
			u=users.objects.get(id=u_id)
			u.order_history.remove(q)
			print('succesfully')
			data={'status':200,'mes':'order succesfully added to the list'}
			print(data)
			return JsonResponse(data,safe=False)



		if request.GET.get('purpose')=='cart':
			print('cart')
			try:
				token=request.COOKIES.get('token')
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
				tn=time.time()
				tt=new_token['exp']
				if tn>tt:
					return render(request,'login_page.html')
			except Exception:
				return render(request,'login_page.html')
			
			user_id=new_token['user_id']
			p_id=request.GET.get('product_id')
			q=users.objects.get(id=user_id)
			p=Products.objects.get(id=p_id)
			q.cart.add(p)


			data={'status':200,'mes':'product succesfully added to cart'}
			return JsonResponse(data,safe=False)
			pass
		
		if request.GET.get('purpose')=='remove_cart':
			try:
				token=request.COOKIES.get('token')
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
				tn=time.time()
				tt=new_token['exp']
				if tn>tt:
					return render(request,'login_page.html')
			except Exception:
				return render(request,'login_page.html')

			u_id=new_token['user_id']
			p_id=request.GET.get('product_id')
			p_id=p_id.replace('d','')
			q=users.objects.get(id=u_id)
			p=Products.objects.get(id=p_id)
			q.cart.remove(p)
			print('remove cart')
			data={'status':200,'mes':'product succesfully added to cart'}
			return JsonResponse(data,safe=False)
			pass


def product_fun(request):
	try:
		token=request.COOKIES.get('token')
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
		tn=time.time()
		tt=new_token['exp']
		if tn>tt:
			return render(request,'login_page.html')
	except Exception:
		return render(request,'login_page.html')

	u_id=new_token['user_id']
	if request.method=='GET':

		p_id=request.GET.get('products_id')
		u=users.objects.get(id=u_id)
		q=Products.objects.get(id=p_id)
		u.b_history.add(q)


		img=imges.objects.filter(parent=q)
		url_array=''

		for i in img:
			url_array=url_array+i.img.url+','
		print(url_array)
		context={'d':q.description,'id':p_id,'img':url_array,'name':q.name,'price':q.price,'vender':q.vender.name,'vender_id':q.vender.id,'rating':q.average_ratings}

		return render(request,'test.html',context)
		pass
	pass



def sign_up_fun(request):
	if request.method=='POST':
		form=user_form((request.POST))
	
		if form.is_valid():
			d=users.objects.filter(username=request.POST['username'])
			if len(d)!=0:
				new_form=user_form()
				context={'form':user_form,'msg':'username already taken try different name'}
				return render(request,'sign_up.html',context)
			else:
				form.save()

	form=user_form()
	context={'form':form}
	return render(request,'sign_up.html',context)


def new_home_fun(request):
	if request.method=='GET':
		alas=product_class.objects.filter(parent=0)
		context={'data':alas}
		return render(request,'new_home.html',context)
	else:
		return HttpResponse('Invalid access atempt')

def p_list_fun(request):
	if request.method=='GET':
		print('p_list')
		p_id=request.GET.get('products_id')
		p_id=int(p_id)
		print(p_id)
		c=product_class.objects.get(id=p_id)
		data=Products.objects.filter(pclass__id=p_id)
		departments=product_class.objects.filter(parent=p_id)
		d_array=[]
		for i in departments:
			a='d'+str(i.id)
			x={'id':a,'name':i.name}
			d_array.append(x)
		
		context={'data':data,'d_array':d_array,'c':c}
		return render(request,'test2.html',context)
		

																											
		pass
	pass
	

def vender_fun(request):
	if request.method=="GET":
		v_id=request.GET.get("vender_id")
		p=Products.objects.filter(vender__id=v_id)
		v=vender.objects.get(id=v_id)
		data=p
		context={'data':data,'vender':v}
		return render(request,'vender.html',context)


def bh_fun(request):
	try:
		token=request.COOKIES.get('token')
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
		tn=time.time()
		tt=new_token['exp']
		if tn>tt:
			return render(request,'login_page.html')
	except Exception:
		return render(request,'login_page.html')

	u_id=new_token['user_id']
	q=users.objects.get(id=u_id)
	broused_products=q.b_history.all()
	context={'data':broused_products}
	return render(request,'b_history.html',context)
	
def oh_fun(request):
	try:
		token=request.COOKIES.get('token')
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
		tn=time.time()
		tt=new_token['exp']
		if tn>tt:
			return render(request,'login_page.html')
	except Exception:
		return render(request,'login_page.html')
	
	u_id=new_token['user_id']
	q=users.objects.get(id=u_id)
	ordered_product=q.order_history.all()
	context={'data':ordered_product,'main_heading':"Your Orders",'button_heading':"Cancel Order"}
	return render(request,'o_history.html',context)


def cart_fun(request):
	try:
		token=request.COOKIES.get('token')
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
		tn=time.time()
		tt=new_token['exp']
		if tn>tt:
			return render(request,'login_page.html')
	except Exception:
		return render(request,'login_page.html')
	
	u_id=new_token['user_id']
	q=users.objects.get(id=u_id)
	cart_product=q.cart.all()
	context={'data':cart_product,'main_heading':"Your cart",'button_heading':"Remove"}
	return render(request,'o_history.html',context)


def vs_fun(request):
	return render(request,'vender_login.html')
	
