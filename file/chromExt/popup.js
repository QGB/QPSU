var currentTab = 0;
// var url = '';
var backgroundPage = null;
//if(chrome.tabs){//chrome.tabs.query  VM109:1 Uncaught TypeError: Cannot read property 'query' of undefined
chrome.tabs&&chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
	currentTab = tabs[0];
	backgroundPage = chrome.extension.getBackgroundPage();
	console.log('qgb popup.js for tab id=' + currentTab.id + ' url=' + currentTab.url);

});

function f_js192(){
			console.log(tab.url,new Date())
			
			if(isNaN(ip)){code=js192.replace('192.168.1.1',ip)}
			else{code=js192.replace('192.168.1.1','192.168.'+ip)}
			// console.log(js192)
			if(tab.url.includes('://192.168.2.22')){code=code.replace('192.168.2.11','192.168.2.22')}
			chrome.tabs.executeScript(tab.id,{
			'code':code
			})
			setTimeout(f_js192,9999*7)//11=*4
		}
// f_js192()

function popupJs(a){
	// interpreter.api["
	// output.value=
	api={document:document,
		window:window,
		print:function(a){output.append(a)}
	}
	if(input.value) {
		try{
			output.append(interpreter.run( input.value,api)  )
			error.value=''
		}catch(e){
			error.value=e
		}
		
	}
	
}
function pageJs(a){/*
a： MouseEvent {isTrusted: true, screenX: 1648, screenY: 92, clientX: 494, clientY: 15, …}

*/
	txt=input.value
	if(txt) {
		chrome.tabs.sendMessage(currentTab.id, {
				type: 'eval',
				options: txt
			},function(a) {// a undefined
        // output.append(a);
		});
		// try{
			// output.append( )
			// error.value=''
		// }catch(e){
			// error.value=e
		// }
		
	}
}
function bgJs(code){
	if(!code)code=input.value
	chrome.extension.sendMessage({eval: code},function(response){
			output.append(response)
		}  
	)
}

// console.log(popupJs)


function taobao(a){
	chrome.tabs.sendMessage(currentTab.id, {
		type: 'taobao_'+a,
		options: input.value
	});	
}



function taobao_start(){
	popupJs('1+1')
}
// function taobao_pause(){}
// function taobao_item(){}
chrome.runtime&&chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
/*backgroundPage and popup ���ܹ��յ���Ϣ��������.onMessage.addListener ȫ�������յ�
{greeting: "hello"} 
{id: "lcgbfhamhkaojgnakpnbdnmelgahcnep", url: "https://shop136810323.taobao.com/search.htm?spm=a1��170.5.77ca50ea9Iz4mt&search=y&orderType=price_asc", tab: {��}, frameId: 0}
*/
// console.log(request,sender,sendResponse,'popup')
	for(i in request){//i of ::  Uncaught TypeError: request is not iterable
		switch(i){//https://www.zhihu.com/question/27819136 switch ���� break ����ִ�� ��һ��case(����ƥ������
			case 'out':
				output.append(request[i])
				break
			case 'in':
				input.value=request[i]
				break
			case 'err':
				err=request[i]
				// sendResponse(request)
				error.value=err.message||err
				break
			case 'clearOut':
				output.clear()
				break
			case 'eval':
				return	
				return sendResponse( eval(request[i] ) )
				break
				
		}
	}
	sendResponse('popup:'+new Date())
	// if(request['out']){
		
	// }
	
})


document.addEventListener('DOMContentLoaded', function () {//ֱ�ӻ�ȡ  Ϊnull
//e.addEventListener('click',function(){chrome.tabs.create({'url': 'http://192.168.2.3', 'selected': false})} //�ǵ���ģʽ����alert�������Դ�����������

window.input=document.getElementById('input')
window.output={
	e:document.getElementById('output'),
	count:0,
	get value() {
		e=this.e
		return e.value||e.innerText
	},
	clear:function(){
		this.count=0
		this.e.innerText=''
	},
	append:function(a){
		e=this.e
		if(this.count===0){
			e.innerText=''
		}
		d=document.createElement('li')
		
			// console.log(a)
		if(! (typeof a==='string')/*不加括号 不对？*/  ){
			a=JSON.stringify(a)
			// try{    a=JSON.stringify(a)	} catch(Exception){//catch一定要加参数，不然语法错误
				// try{a=String(a)             } catch(Exception){}
			// }
		}
		// d.innerText=a
		d.innerHTML='<pre>'+a+'</pre>'
		e.appendChild(d)	
		this.count+=1//e.children.length 233
		d.id='_'+this.count
	}
}

document.getElementById('popupJs').addEventListener('click', popupJs)
document.getElementById('pageJs').addEventListener('click',  pageJs)
document.getElementById('bgJs').addEventListener('click',    bgJs )

document.getElementById('clearOut').addEventListener('click',function(){ output.clear() }    )

document.getElementById('js192').addEventListener('click', popupJs)
//taobao_


document.getElementById('taobao_start').addEventListener('click',function(){taobao('start')})
document.getElementById('taobao_pause').addEventListener('click',function(){taobao('pause')})
document.getElementById ('taobao_item').addEventListener('click',function(){taobao('item')})
 
document.getElementById('get').addEventListener('click', function(){
		bgJs("\
	chrome.tabs.query({url:'https://ide.coding.net/ws/*'},function(tabs){\
		for(tab of tabs){\
			chrome.tabs.executeScript(tab.id,{code:'if(p=document.querySelector(\".port-content > a\") )chrome.storage.sync.set({\"cjs_post_url\":p.href}) ; else{alert(\"NO url in \"+document.URL)}  ' })  \
		}\
	})\
		")
	
	txt="N.http(gurl+'site/'+window.location.host+'.js','get',function(){ eval(this.response)  }      )"
	
	chrome.tabs.sendMessage(currentTab.id, {
		type: 'eval',
		options: txt
	},function(a) {// a undefined
// output.append(a);
	});
})
///////////////////////
});

function test(){
 
}

// alert(1)