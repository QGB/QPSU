import os
import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import py

U,T,N,F=py.importUTNF()



def c(x,y,ms=555):
	os.system('adb shell input touchscreen swipe {0} {1} {0} {1} {2}'.format(x,y,ms))
	

	
def scrollUp():
	os.system('adb shell input touchscreen swipe 55 888 55 444 555')
	
def xb():
	scrollUp()
	c(89,1119)                                                            # 18 
	U.sleep(0.3)
	c(287,860)                                                            # 申请补卡
	U.sleep(2)
	U.sleep(2)
	c(216,512)                                                            # 输入框 
	c(99,999)                                                             # 22 
	c(363,746)    
	c(51,124)	
	
def sb():
	scrollUp()
	c(89,923)                                                            # 18 
	U.sleep(0.3)
	c(287,860)                                                            # 申请补卡
	U.sleep(2)
	U.sleep(2)
	c(216,512)                                                            # 输入框 
	c(99,999)                                                             # 22 
	c(363,746)    
	c(51,124)
	
def backup_all_app(adb='C:/QGB/software/scrcpy-win64/adb.exe',backup_path='D:/nexus6p/apks/',):
	backup_path=backup_path.replace('\\','/')
	if not backup_path.endswith('/'):
		backup_path+='/'
	ipy=U.get_ipy(raise_err=True)
	ps=ipy.getoutput(f'{adb} shell pm list packages')
	print(len(ps))
	count=0
	for i in ps:
		p=T.sub(i,'package:',).strip()
		if not p:
			print('#skip',i)
			continue
		path=ipy.getoutput(f'{adb} shell pm path {p}')
		if len(path)!=1:
			print('#err getoutput pm path',i,p,path)
			continue
		path=T.sub(path[0],'package:',).strip() 
		if not path:
			print('#err T.sub pm path',i,p,path)
			continue
		name= T.subLast(path,'/','')
		backup_file=f'{backup_path}{p}={name}'
		if F.exist(backup_file):
			print('#exist,skip',backup_file)
		ipy.system(f'{adb} pull {path} {backup_file}')
		
		count+=1
		
	return count
	