import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *
import PIL
from PIL import Image
from PIL.ImageColor import colormap
import PIL.ExifTags
import PIL.ImageGrab

color10=[
 [(0  , 0  , 0  ), '0x00_00_00 #black'],
 [(0  , 0  , 255), '0x00_00_ff #blue'],
 [(0  , 255, 0  ), '0x00_ff_00 #lime'],
 [(0  , 255, 255), '0x00_ff_ff #cyan'],
 [(128, 0  , 128), '0x80_00_80 #purple'],
 [(128, 128, 128), '0x80_80_80 #gray'],
 [(255, 0  , 0  ), '0xff_00_00 #red'],
 [(255, 0  , 255), '0xff_00_ff #magenta'],
 [(255, 255, 0  ), '0xff_ff_00 #yellow'],
 [(255, 255, 255), '0xff_ff_ff #white']]


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

def iterate_image_by_row(image,):
	'''row_index=True,color=True '''
	a=image.load()
	col_indexs=U.range(image.width)
	for y in py.range(image.height):
		yield y,[a[x,y] for x in col_indexs]
iter_img_row=iterate_image_by_row	
	
def iterate_image_by_column(image,):
	'''row_index=True,color=True '''
	a=image.load()
	row_indexs=U.range(image.height)
	for x in py.range(image.width):
		yield x,[a[x,y] for y in row_indexs]
iter_img_col=iterate_image_by_col=iterate_image_by_column		
	
def iterate_image_all(image,xy=False,color=True,stop_point=None):
	''' 原点在左上角 ，从左至右，从上至下
iter include stop_point	
	'''
	if not color and not xy:raise py.ArgumentError(color,xy)
	if color:a=image.load()
	for y in py.range(image.height):
		for x in py.range(image.width):
			if stop_point and x>stop_point[0] and y>stop_point[1]:return
		
			if color and  not xy:yield a[x,y]
			if not color and  xy:yield x,y
			if color and  xy:yield x,y,a[x,y]
	
	# return
iter_img_xy=iter_img=iter_img_all=iter_image=iterate_all_image=iterate_one_image_all=iterate_image_all

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
	
def dataURL_to_pil_image(s):
	s64=T.sub(s,'data:image/png;base64,')
	if not s64:raise NOT_PNG
	b=T.base64_to_bytes(s64)    
	return bytes_to_pil_image(b)
base64_to_img=dataURL_to_img=dataURL_to_pil_image

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
	if not format.startswith('.'):format='.'+format
	_, img_encode = cv2.imencode(format, img_numpy)
	img_bytes = img_encode.tobytes()
	return img_bytes
	
def write_cv2_image(fn,a,format='png'):
	b=cv2_image_to_bytes(a,format=format)
	return F.write(fn,b)
	
def bytes_to_cv2_image(b):
	import cv2,numpy
	nparr = numpy.fromstring(b, numpy.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)	
	return img_np
	
def new_numpy_image(width,height,color=(255,255,255)):
	''' (255,0,0)      # (B, G, R)  color_bgr
	
(height,width,3)
长 宽 高	
	'''
	import numpy as np
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[:]=U.color_to_bgr_tuple(color)
	return blank_image
new_cv2_image=new_numpy_image	
	
def cv2_draw_text(img,text,
xy = (0,50),#x,y+font_height
font                   = U.IntRepr(0,repr='cv2.FONT_HERSHEY_SIMPLEX'),
fontScale              = 1                       ,
fontColor              = (255,255,255)           ,
thickness              = 1                       ,
lineType               = 2                       ,
								**ka):
	'''[(i,getattr(cv2,i),) for i in dir(cv2) if i.startswith('FONT_')]
Out[471]:
[('FONT_HERSHEY_COMPLEX', 3),
 ('FONT_HERSHEY_COMPLEX_SMALL', 5),
 ('FONT_HERSHEY_DUPLEX', 2),
 ('FONT_HERSHEY_PLAIN', 1),
 ('FONT_HERSHEY_SCRIPT_COMPLEX', 7),
 ('FONT_HERSHEY_SCRIPT_SIMPLEX', 6),
 ('FONT_HERSHEY_SIMPLEX', 0),
 ('FONT_HERSHEY_TRIPLEX', 4),
 ('FONT_ITALIC', 16)]

0-9 char not  break bottom
[ ] char will break bottom
'''	
	import cv2
	xy=U.get_duplicated_kargs(ka,'bottomLeftCornerOfText','xy','coordinate','coordi',default=xy)
	
	cv2.putText(img,text, 
		xy, 
		font, 
		fontScale,
		fontColor,
		thickness,
		lineType)
	return img
	
def get_string_image(text,size=48,font='simsunb.ttf',w=None,h=None):
	'''
('simsunb.ttf',48) a[5+1行][0:5+37+5]==【5个0，37个1，5个0】  
第6列 【5个0，37+2个1，3个0】 一个方框字符黑色尺寸 37*39

Image.new(mode='P',"L", "RGB"	
	If you have an L mode image, that means it is a single channel image - normally interpreted as greyscale. 
	
simsun.ttc 宋体 常规
simhei.ttf 黑体 常规	
	'''
	from PIL import Image, ImageFont, ImageDraw
	if not w:w=100
	if not h:h=100
	font=ImageFont.truetype(font,size)     
	image = Image.new('L', (w, h), color='white')
	drawing = ImageDraw.Draw(image)
	drawing.text((0,0), text, font=font)
	return image
get_font_img=font_to_img=char_to_img=new_font_img=get_char_image=get_string_image
	
def get_all_font_list(only_name=False):
	''' 不去重 [374, 207] 去重后 
c:/windows/fonts/ 有两个出现一次，其他的都因为路径大小写问题 最多重复两次
	'''
	import matplotlib.font_manager
	fs=matplotlib.font_manager.fontManager.ttflist
	if only_name:
		return [f.name for f in matplotlib.font_manager.fontManager.ttflist]	
	return fs	

def get_font_by(fname='',name='',style='',variant='',weight='',stretch='',size='',**ka):
	''' FontEntry(fname='C:\\Windows\\Fonts\\segoeui.ttf', name='Segoe UI', style='normal', variant='normal', weight=400, stretch='normal', size='scalable')]
'''
	fname=U.get_duplicated_kargs(ka,'path','file','f',default=fname)
	fname=F.auto_path(fname).lower()
	fs=get_all_font_list()
	for f in fs:
		if F.auto_path(f.fname).lower()==fname:
			return f
			
		if fname   and fname  ==f.fname  :return f
		if name    and name   ==f.name   :return f
		if style   and style  ==f.style  :return f
		if variant and variant==f.variant:return f
		if weight  and weight ==f.weight :return f
		if stretch and stretch==f.stretch:return f
		if size    and size   ==f.size   :return f
	return py.No('not found font')
get_font=get_font_by
	
def all_font_html(p,fs=None):
	# fn=get_all_font_list(only_name=True)
	# "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)
	if not fs:
		fs=[]
		for f in get_all_font_list():
			file=T.sub_last(f.fname,'\\',)
			fs.append([file,f])
	if U.len(fs[0]) < 2:
		fs=[[f.name,f] for f in fs]
		
	fs.sort(key=lambda row:row[0])
	hs=[]
	for n,(file,f) in py.enumerate(fs):
		h=f"""
<p style='color:red;'>{'%03i '%n}{f.fname[3:]}: 
	<span style='font-family:{f.name}; font-size: 24px;color:black;float:right;'>0123456789{f.name}
</p>"""
			# for font in sorted(fn)])
		hs.append(h)

	html="<div style='column-count: 1;'>{}</div>".format("\n".join(hs))
	
	return N.html(p,html,remove_tags=0)
font_html=all_font_html	

def get_image_non_white_range(image,color=255):
	pil=py.from_qgb_import('pil')
	
	nw=0
	nw0=nw1=None
	mx=image.width-1
	for x,c in pil.iter_img_col(image,):
		if [i for i in c if i!=color]:
			if nw0==None:nw0=x
			if x==mx:nw1=mx+1
			else:    nw1=None
			nw+=1
		else:
			if nw0!=None and nw1==None:nw1=x
	nh=0
	nh0=nh1=None
	my=image.height-1
	for y,c in pil.iter_img_row(image,):
		if [i for i in c if i!=color]:
			if nh0==None:nh0=y
			if y==my:nh1=my+1
			else:    nh1=None
			nh+=1
		else:
			if nh0!=None and nh1==None:nh1=y
	#        print(y,'|')

	if nw0!=None and nh0!=None and (nw1-nw0!=nw or nh1-nh0!=nh):
		print(nw,nw0,nw1 ,'n_height:',nh,nh0,nh1  )
		nneeee
	return nw,nh	
get_non_range=get_img_non_range=get_image_non_white_range	

def cv2_draw_rect(a,rect,color):
	x,y,x1,y1=rect
	
	a[y,x:x1]=color
	a[y1,x:x1]=color
	
	a[y:y1,x]=color
	a[y:y1,x1]=color
	return a
	
	
def read_file_as_cv2_image(file):
	'''
IMREAD_ANYDEPTH : 输入具有相应深度时返回 16 位/32 位图像，否则将其转换为 8 位。
只有IMREAD_ANYDEPTH，返回8位 0-255 灰度图
	'''
	import cv2

	image = cv2.imread(file, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
	return image
	
read_cv2_image=read_file_as_cv2_image	

def trim_cv2_image(a,condition=None,direction='x',margin=2):
	'''
In [496]: z
array([[ 0,  0,  0,  0],
       [ 1,  2,  3,  4],
       [ 5,  6,  7,  8],
       [ 9, 10, 11, 12]])

In [497]: np.where((z <11).all(axis=1))
Out[497]: (array([0, 1, 2], dtype=int64),)

In [498]: np.where((z <11).all(axis=0))
Out[498]: (array([0, 1], dtype=int64),)



'''	
	
	from qgb import np as Y
	import numpy
	# 获取边界
	# def get_edge(m,)

	if 'x' in direction:
		m=a.shape[1]
		n0=0
		for n in range(m):
			ah=a[:,:n]
			if not condition(ah).all():
				n0=n
				break

		n1=m-1
		for n in range(m-1,0,-1):
			ae=a[:,n:]
			if not condition(ae).all():
				n1=n
				break
				
		#cols=numpy.where(condition.all(axis=0).all(axis=1))[0]
		n0=py.max(0,n0-margin)
		n1=py.min(m-1,n1+margin)

		a= a[:,n0:n1]
	if 'y' in direction:
		m=a.shape[0]
		n0=0
		for n in range(m):
			ah=a[:n,]
			if not condition(ah).all():
				n0=n
				break

		n1=m-1
		for n in range(m-1,0,-1):
			ae=a[n:,:]
			if not condition(ae).all():
				n1=n
				break
				
		n0=py.max(0,n0-margin)
		n1=py.min(m-1,n1+margin)
		a= a[n0:n1]		
	return a.copy()
strip_cv2_image=cv2_image_strip=trim_cv2_image

def expand_grey_to_rgb(grey):
	''' grey 2d int 
return.shape x,y,3	
	'''
	import numpy
	return numpy.stack([grey, grey,grey], axis=-1)  # 这个增加维度 对任意shape的都适用
	#下面 只能从 2d 到 3d ?
	return numpy.dstack((grey, numpy.zeros_like(grey), numpy.zeros_like(grey)))# [22,0,0]
	return numpy.dstack((grey, grey,grey))# [22,22,22]
	
def match_char(image,char,show=False):
	import cv2,numpy,numpy as np
	from qgb import pil
	U.set_gst('C:/test/cv2',cd=1)

	img=pil.new_font_img(char,size=12,w=6,h=12)
	t2d=pil.pil_to_cv2(img)
	# image = cv2.imread('large.png')
	#image=image[0:60,0:30-6]

	ts=t2d.shape
	t=numpy.full(shape=(*ts,3),fill_value=255).astype('u1')
	mask=numpy.zeros(shape=ts).astype('u1')
	for x,y in np.ndindex(ts):
		if t2d[x,y]!=255:
			mask[x,y]=255
			t[x,y]=0


	print(image.shape, image.dtype)	
	print(t2d.shape, t2d.dtype)
	print(mask.shape, mask.dtype)
	trows,tcols = template.shape[:2]
	result = cv2.matchTemplate(image, t, cv2.TM_SQDIFF, None, )

	import numpy
	import numpy as np
	a,b=np.min(result),np.max(result)
	de=b-a
	ts=result.shape
	t=numpy.full(shape=(*ts,3),fill_value=255).astype('u1')
	tc=t.copy()
	mask=numpy.zeros(shape=ts).astype('u1')
	for x,y in np.ndindex(ts):
		di=result[x,y]-a
		tc[x,y]=t[x,y]=round( (di/de)*255)
		if np.all(t[x,y]<20):
			cv2.rectangle(image, (y,x),(y+tcols,x+trows),(0,0,255),1)
			cv2.rectangle(tc, (y-3,x-6),(y+tcols-3,x+trows-6),(0,0,255),1)
	#        print('0==t  %s,%s'%(x,y) )

	mn,_,mnLoc,_ = cv2.minMaxLoc(result)

	# Draw the rectangle:
	# Extract the coordinates of our best match
	MPx,MPy = mnLoc

	# Step 2: Get the size of the template. This is the same size as the match.
	#trows,tcols = template.shape[:2]

	# Step 3: Draw the rectangle on large_image
	cv2.rectangle(image, (MPx-1,MPy-1),(MPx+tcols,MPy+trows),(0,0,255),1)
	if show:
		# cv2.imwrite('rect.bmp',image)
		# Display the original image with the rectangle around the match.
		cv2.imshow('output',image)

		# The image is only displayed if we call this
		cv2.waitKey(0)
	return image	