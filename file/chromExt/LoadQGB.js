gs_qgb_base_url="http://127.0.0.1:23571/"
gs_qgb_base_url="https://okfw.net/"
gs_qgb_base_url=gs_qgb_base_url+"a=T.subr(request.path,'%23-');r=F.read(a)%23-C:/QGB/babun/cygwin/home/qgb/js/"
function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms) )  }
loadQGB=function (isPrint){
	xhr=new XMLHttpRequest()
	xhr.open('get',gs_qgb_base_url+'qgb.js')
	xhr.onload=function(){
		eval(this.response)
		if(isPrint===undefined) console.log('loaded length  '+this.response.length)
	}
	xhr.send()
	return xhr
}
loadQGB()
