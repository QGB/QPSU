function teste(){

    ds=document.querySelectorAll('dl.item') 
    img=ds[1].querySelector('img')

    img.setAttribute("crossOrigin",'Anonymous')

    c= document.createElement("CANVAS")
    ctx = c.getContext('2d');
    ctx.drawImage(img,0,0);  

    b = c.toDataURL("image/png");

    console.log(b)
}

_TEXT=function(wrap) {return wrap.toString().match(/\/\*\s([\s\S]*)\s\*\//)[1];}  // 提取 /* 之间的内容 */
_CODE=function(wrap) {return wrap.toString().match(/function\s*\(\s*\)\s*{\s*([\s\S]*)\s*}/ )[1];}//auto trim { code_start_end_space }

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms) )  }
function _sleep(sec){// chrome 74 还有效~
 // console.log(new Date().toISOString())  // 
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'https://okfw.net/r=U.sleep('+sec+')', false);  // `false` makes the request synchronous
  xhr.send(null);
 // console.log(new Date().toISOString())
}

function get_img(URL) {
    return new Promise((resolve, reject) => {
        let img = new Image()
        img.setAttribute("crossOrigin",'Anonymous')

        img.onload = () => resolve(img)
        img.onerror = reject
        img.src = URL
    })
}    

async function get_img_b64(URL) {
    if(URL.src){
        URL=URL.src
    }
    var img=await get_img(URL)
    var canvas = document.createElement("canvas");// 这个不注册的话，document.querySelector("canvas") 找不到，  暂时不考虑 复用对象等性能问题
//         canvas.width = this.width;
//         canvas.height = this.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var b64 = canvas.toDataURL("image/png");
//     var b =canvas.toBlob(function(blob){...}, 'image/jpeg', 0.95); // JPEG at 95% quality
    return b64
// alert(dataURL.replace(/^data:image\/(png|jpg);base64,/, ""));  T.sub

}

async function post(url,data){
    if(typeof a!='string')data=JSON.stringify(data)

    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('post', url, true);
        // xhr.responseType = 'document';
        xhr.onload = function () {
            resolve(xhr.response);
        };
        xhr.send(data)
    });
}
//await post("https://okfw.net/r=U.dir(q)",[1,2,3] )
/////////////////////////////////////////////////////////////////////
async function tab_query(qd={} ){
    return new Promise(function (resolve, reject) {    
      chrome.tabs.query(qd, function(tabs) { 
        resolve(tabs)
      })

   })
}
getAllTabs=get_all_tabs= tab_query


async function get_current_tab(){ return (await tab_query({'active': true,}) )[0]  }
tab_current=get_current_tab
// await sleep(999)
// await tab_query({currentWindow:true })  //  在控制台没有选中窗口 导致 返回【】

var gs_lib_func = _sleep.toString()+
    sleep.toString()+post.toString()+
    get_img.toString() + get_img_b64.toString()+'\n'

async function tab_exec(tab,code){
    var tab_id=tab
    if(tab.id){tab_id=tab.id  }
    
    return new Promise(function (resolve, reject) {  //看下一行，其实 r=没用 ，反正默认返回最后一个值
      chrome.tabs.executeScript(tab_id,{'code': gs_lib_func+code+'\n r=JSON.stringify(r)' } ,function(as) { //array of any	(optional) result	The result of the script in every injected frame.
        resolve(JSON.parse(as[0] )  ) // 【0】 这只是临时 方便await ，以后要删除
      })
   })
}
//console.log(new Date().toISOString());await tab_exec(t,'r=new Date()');  // 延迟 2ms

async function tab_update(tab,url){
    return new Promise(function (resolve, reject) {
      chrome.tabs.update(tab.id,{'url': url } ,function(tab) { //url 必须 http...  否则会跳到 插件url
        resolve(tab)
      })
   })
}

async function tab_remove(tab){
    return new Promise(function (resolve, reject) {
      chrome.tabs.remove(tab.id,function() { 
        resolve(arguments)
      })
   })
}


//await tab_exec( await tab_current()  ,    'alert(new Date() )  '  )


//最好这个要阻塞，但是没找到好办法。要不只能轮询
sg= _CODE(function(){
    us=Array.from(document.querySelectorAll('dl.item')).map(i=>i.querySelector('img') ).map(img=>img.src )
    dis=Array.from(document.querySelectorAll('dl.item')).map(i=>i.outerHTML )
    ds=[location.href , document.documentElement.outerHTML]
    imgs=[]
    async function main(){
    await post("https://okfw.net/r=t=T.json_loads(request.get_data());ts.append(t) ", new Date() )
       await post("https://okfw.net/ud=T.json_loads(request.get_data());ds[ud[0]]=ud[1];r=len(ds) ", ds )
       await post("https://okfw.net/lds=T.json_loads(request.get_data());dis.append(lds);r=len(dis) ", dis )
       imgs= await Promise.all(   us.map(async u=>[u,await get_img_b64(u)] ) );
       await post("https://okfw.net/ll=T.json_loads(request.get_data());imgs.append(ll);r=len(imgs) ", imgs )

       Array.from(document.querySelector('.pagination-mini').querySelectorAll('a'))[1].style.background ='green'

        
    await post("https://okfw.net/r=t=T.json_loads(request.get_data());ts.append(t) ", new Date() )
    }
    main()

    r=new Date()

})


async function ext_main(){
    var t=(await tab_query({url: "https://youxin-electronic.taobao.com/*"}) )[0]
    url="https://youxin-electronic.taobao.com/search.htm?orderType=price_asc&pageNo="+1
    while(url && url.length>9){
        check=await post("https://okfw.net/url=T.json_loads(request.get_data());r=in_ds(url)",url)
        if(check==='False' && t.url!=url){
            await tab_update(t,url)   
            t=(await tab_query({url: "https://youxin-electronic.taobao.com/*"}) )[0]
        }
        if(check==='True'){
            var max=await post("https://okfw.net/r=max_ds()")
            url="https://youxin-electronic.taobao.com/search.htm?orderType=price_asc&pageNo="+(parseInt(max)+1)
            continue
        }

        
        await sleep(888)
        await tab_exec(t, sg )
        await sleep(399)
        for(var i of [0,1,2,3,4,5,6,7,8]){
           console.log(i)
           if(i%3==0){ await tab_exec(t, sg ) }
           next=await tab_exec(t, _CODE(function(){
               r=""
               tmp=document.querySelector('.pagination-mini')
               if(tmp){
                    next=Array.from(tmp.querySelectorAll('a'))[1]
                   if(next.style.background==="green") r=next.href 
               }else{
                   r='reload'
               }
                

            }))
            if(next==='reload'){
                await tab_update(t,url)   
                t=(await tab_query({url: "https://youxin-electronic.taobao.com/*"}) )[0]
                await sleep(888)
                await tab_exec(t, sg )
                await sleep(399)
                continue
            }


            if(!next.startsWith('http') ){
                await sleep(499)
                continue   
            }else{
                url=next
                break
            }
            

        }
        
    }

    console.log(await post("https://okfw.net/r=done=U.stime()") )
 


}

//////////////////////////////////////////////////////////////////
async function main(){
    return t=await tab_current()
    var img="https://img.alicdn.com/bao/uploaded/i3/2658592015/TB2Xk8McA.OyuJjSszhXXbZbVXa_!!2658592015.jpg_240x240.jpg"
    var ds=document.querySelectorAll('dl.item') 
    img=ds[5].querySelector('img')
    b=await get_img_b64(img)
//     console.log(b)
    return(b)
}


 main()

