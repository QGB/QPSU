import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *
import PIL
from PIL import Image
import PIL.ExifTags
import PIL.ImageGrab
def read_exif(img):
	r=img._getexif()
	if r==None:
		return py.No('no exif')
	d={}
	for i,v in r.items():
		s=PIL.ExifTags.TAGS.get(i,py.str(i))
		d[U.IntRepr(i,repr=s)]=v
	
	return d
get_exif=read_exif	

def cut(img,rect):
	return img.crop(rect)

def black_white(img,threshold=127,background='white'):
	'''
threshold (thresh) value: 阈值
	
	'''
	if background=='white':
		fn = lambda x : 255 if x > threshold else 0 #白黑
	elif background=='black':
		fn = lambda x : 0 if x > threshold else 255 #黑白, 原图背景是黑色，相当于反色
	else:
		raise py.ArgumentError(background)
	r = img.convert('L').point(fn, mode='1')
	return r
bw=black_white	


def get_image_pixel(image,x,y):
	'''
image.load()	
:returns: An image access object.
:rtype: :ref:`PixelAccess` or :py:class:`PIL.PyAccess`	
'''	
	a=image.load()
	return a[x,y]
pixel=get_pixel_from_image=get_image_pixel	

	
def open(file):
	return PIL.Image.open(file)
	

def pil_image_to_bytes(img,format='png'):
	from io import BytesIO
	img_io = BytesIO()
	img.save(img_io, format)
	img_io.seek(0)
	bytes=img_io.read(-1)
	return bytes
	
def bytes_to_pil_image(b):
	# from PIL import Image
	import io
	bio=io.BytesIO(b)  
	return PIL.Image.open(bio)
b2im=b2img=bytes_to_pil_image	
	
def pil_to_cv2(img):
	import cv2,numpy
	return numpy.asarray(img)
	# return cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR) 
	
def cv2_image_to_bytes(img_numpy,format='png'):
	import cv2
	_, img_encode = cv2.imencode('.jpg', img_numpy)
	img_bytes = img_encode.tobytes()
	return img_bytes
def bytes_to_cv2_image(b):
	import cv2,numpy
	nparr = numpy.fromstring(b, numpy.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)	
	return img_np
	
def new_cv2_image(width,height,color=(255,255,255)):
	''' (255,0,0)      # (B, G, R)
	'''
	import numpy as np
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[:]=color
	return blank_image