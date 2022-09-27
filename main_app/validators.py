from django.core.exceptions import ValidationError

def validate_pincode(value):
	try:
		a=int(value)
		if len(value)==6:
			return value
		else:
			raise ValidationError("Enter valid pin code")
	except Exception:
		raise ValidationError("Enter valid pin code")

def validate_lat_longitude(value):
	x=value.split(',')
	if len(x)==2:
		i=0
		while i<2:
			try:
				a=float(x[i])
			except Exception:
				raise ValidationError("location coordinates nor correct")
				
			i=i+1
		return value
	else:
		raise ValidationError("location coordinates not correct")
		



