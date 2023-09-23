#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.youtube'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()

import scrapetube

def get_channel_all_videos_info(url):
	if '://' not in url and '@' not in url:
		url='@'+url

	if url.startswith('@'):
		url=f'https://www.youtube.com/{url}/videos'
		
	ut=T.sub_last(url,'@')
	
	if '/' not in ut  :url+='/videos'
	# if url.endswith('/'):url+='videos'
	cid=T.sub(url,'@','/')
	if not cid or not url.endswith('videos'):raise py.ArgumentError(url)
	
	vs=U.get_or_set(cid,[])
	if not vs:
		videos = scrapetube.get_channel(channel_url=url , sort_by = "newest" )
		print(U.stime(),url)
		vs=list(videos)
		print(U.stime(),len(vs))
	return vs
get_channel=get_channel_all_videos_info
# get_channel_all_videos	

def download_video(url):
	return
download=download_video
	
	
def download_channel_all_videos(url):
	