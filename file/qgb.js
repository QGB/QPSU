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
    
    return new Promise(function (resolve, reject) {  //看code最后行，其实 r=没用 ，反正chrome默认返回最后一个值
      chrome.tabs.executeScript(tab_id,
      {'code': 'r=undefined\n'+ //每次执行后默认保留变量，去除它
      gs_lib_func+code+
"\n if((typeof r)==='undefined'){r=new Date()} \
    if((typeof r)==='function'){r=r.toString()} \
    rj=JSON.stringify(r);\
    if(rj){r=rj}\
    else{r==JSON.stringify(r+'')}\
    r=r"
      } ,function(as) { //array of any	(optional) result	The result of the script in every injected frame.
        if(as && as.length)
            resolve(JSON.parse(as[0] )  ) // 【0】 这只是临时 方便await ，以后要删除
        else
            resolve(as) 
      })
   })
}
//console.log(new Date().toISOString());await tab_exec(t,'r=new Date()');  // 延迟 2ms

async function tab_update(tab,url){
    var tab_id=tab
    if(tab.id){tab_id=tab.id  }
    return new Promise(function (resolve, reject) {
      chrome.tabs.update(tab_id,{'url': url } ,function(tab) { //url 必须 http...  否则会跳到 插件url
        resolve(tab)
      })
   })
}

async function tab_remove(tab){
    var tab_id=tab
    if(tab.id){tab_id=tab.id  }
    return new Promise(function (resolve, reject) {
      chrome.tabs.remove(tab_id,function() { 
        resolve(arguments)
      })
   })
}

async function rpc_sleep(aisec){
    sec=await post("https://okfw.net/r=U.get('rpc_sleep',1);U.sleep(r)")
    sec=Number.parseInt(sec)
    return sec
}

async function get_urls_doc(
  query_url="https://okfw.net/r=B.next_id('https://item.taobao.com/item.htm?id={}')",
  post_url="https://okfw.net/r=B.receive(request)"){

    main_post_code=_CODE(function(){
       r=0
       while(!document.querySelector('.tb-rmb')){
            r+=1
            _sleep(0.1)
       }
       async function main(){
            sf=document.querySelector('.sufei-dialog')
            if(sf){
                await post("https://okfw.net/r=U.set('taobao_sf',U.stime());")
            }else{
                await post("post_url",document.documentElement.outerHTML)
                document.body.style.background='green'
            }
            
       }
       main()
    }).replace('post_url',post_url)

    check_code=_CODE(function(){
        r=document.body.style.background
   })

   tid=(await tab_query()).map(t=>t.id)[0] // seems min id
   url=await post(query_url)
   while(url && url.length){
       await tab_update(tid,url)  
       await sleep(1555)
       await tab_exec(tid,main_post_code)
       await rpc_sleep()
       n=0
       check=await tab_exec(tid,check_code)
       while(check!='green'){
            n+=1
            await rpc_sleep()
            console.log(n,new Date(),'wait...green')
            if((n%3)===0){
                await tab_exec(tid,main_post_code)
                await sleep(555)
                bcheck=await post('https://okfw.net/r=B.got_err()')
                if(bcheck && bcheck.length){
                    console.log(bcheck,new Date())
                    n=-1
                    continue
                }
                
            }
            check=await tab_exec(tid,check_code)
        }
        url=await post(query_url)
                
   }

}

///////////////////////// lib end //////////////////////////////////////
async function taobao_cart_back(){
    gbloop=1
    while(gbloop){
        for(var t of (await tab_query({url: "https://cart.taobao.com/add_cart_succeed.htm*"}) )){
            await tab_remove(t)
//             await tab_exec(t,_CODE(function(){
//                 Array.from(document.querySelectorAll('span')).map(i=>i.style.background='green')
//                 history.back()

//             }))
        }
        await sleep(444)
    }
        
}

//await tab_exec( await tab_current()  ,    'alert(new Date() )  '  )


//最好这个要阻塞，但是没找到好办法。要不只能轮询
gs_taobao_list= _CODE(function(){
    us=Array.from(document.querySelectorAll('dl.item')).map(i=>i.querySelector('img') ).map(img=>img.src )
    dis=Array.from(document.querySelectorAll('dl.item')).map(i=>i.outerHTML )
    if(!location.href){
        alert('location.href no')
        throw 233
    }
//     ds=[location.href , document.documentElement.outerHTML]
//     imgs=[]
    async function main(){
        await post("https://okfw.net/r=TB.insert(request)", [location.href,dis,new Date()] )
        next=(  document.querySelector(".ui-page-s-next") ||
                Array.from(document.querySelector('.pagination-mini').querySelectorAll('a'))[1]
            )//tmall ||taobao
        next.style.background ='green'

    }
    main()

    r=new Date()

})


async function taobao_list(base_url="https://youxin-electronic.taobao.com/"){
    var t=(await tab_query({url: base_url+"*"}) )[0]
    console.log(await post("https://okfw.net/r=start_time=U.stime()"),t )
    var base_search_url=base_url+"search.htm?orderType=price_asc&pageNo="
    url=base_search_url+1
    while(url && url.length>9){
        check=await post("https://okfw.net/url=T.json_loads(request.get_data());r=TB.include(url)",url)
        if(check==='False' && t.url!=url){
            await tab_update(t,url)   
            t=(await tab_query({url: base_url+"*"}) )[0]
        }
        if(check==='True'){
            var max=await post("https://okfw.net/r=TB.max_num()")
            url=base_search_url+(parseInt(max)+1)
            continue
        }

        await tab_exec(t, gs_taobao_list )
        await sleep(888)
        for(var i of [0,1,2,3,4,5,6,7,8]){
           console.log(i)
           next=await tab_exec(t, _CODE(function(){
               r=""
               tmp=document.querySelector('.pagination-mini')

               next=Array.from(tmp.querySelectorAll('a'))[1]
               if(next.style.background==="green") r=next.href   

            }))
           if(!next){
                if((i+1)%3===0){
                    await tab_exec(t, gs_taobao_list )
                    await sleep(888)
                    continue
                }
                break
           }
           if(!next.startsWith('http') ){
               await sleep(999)
               continue   
            }else{
               url=next
               break
            }
            

        }
        
    }

    console.log(await post("https://okfw.net/r=done=U.stime()") )
 
}//end taobao_list

async function tmall_list(base_url="https://qyssm.tmall.com/"){
    var t=(await tab_query({url: base_url+"*"}) )[0]
    var base_search_url=base_url+"search.htm?search=y&scene=taobao_shop&orderType=price_asc&pageNo="
    url=base_search_url+1
    while(url && url.length>9){
        check=await post("https://okfw.net/url=T.json_loads(request.get_data());r=in_ds(url)",url)
        if(check==='False' && t.url!=url){
            await tab_update(t,url)   
            t=(await tab_query({url: base_url+"*"}) )[0]
        }
        if(check==='True'){
            var max=await post("https://okfw.net/r=max_ds()")
            url=base_search_url+(parseInt(max)+1)
            continue
        }

        await tab_exec(t, gs_taobao_list )
        await sleep(888)
        for(var i of [0,1,2,3,4,5,6,7,8]){
           console.log(i)
           next=await tab_exec(t, _CODE(function(){
               r=""
               next=document.querySelector(".ui-page-s-next")
               if(next.style.background==="green") r=next.href   
            })) 
              
            if(!next){
                if((i+1)%3===0){
                    await tab_exec(t, gs_taobao_list )
                    await sleep(888)
                }
                continue
            }
            if(!next.startsWith('http') ){
                await sleep(999)
                continue   
            }else{
                url=next
                break
            }
            

        }
        
    }

    console.log(await post("https://okfw.net/r=done=U.stime()") )
    
}

gs_get_document= _CODE(function(){
    async function main(){
        dls=document.querySelectorAll('.tb-sku > dl.tm-sale-prop ')
        for(dl of dls){

        }
        p=document.querySelector('.tm-fcs-panel')
        //ts=Array.from(document.querySelectorAll('.tb-txt') ).map(i=>i.outerHTML)                
        await post("https://okfw.net/u,h=T.json_loads(request.get_data());duh[u]=h;r=len(duh)",[location.href,document.documentElement.outerHTML])
        p.style.background='green'

    }
    main()
    r=new Date()
})
async function tmall_get_item(base_url="https://detail.tmall.com/item.htm"){
    t=await tab_query({url: base_url+"*"})
        
    while( t.length ){
        t=t[0]
        await tab_exec(t,gs_get_document)
        await sleep(9999*5)
        r=await tab_exec(t, _CODE(function(){
            r=document.querySelector('.tm-fcs-panel').style.background
        }))    
        n=0
        while(r!='green'){
            n+=1
            await sleep(500)
            r=await tab_exec(t, _CODE(function(){
                r=document.querySelector('.tm-fcs-panel').style.background
            })) 
            console.log(new Date(),'wait...green')
            if((n%5)===0){
                await tab_exec(t,gs_get_document)
            }
        }
        url=await post("https://okfw.net/r=u=next_url()")
        await tab_update(t,url)  
        await sleep(1555)
        t=await tab_query({url: base_url+"*"})
    
    }
    console.log('done')
}
    

async function taobao_add_cart(){
    t=await tab_query({active:true,url: "https://item.taobao.com/item.htm*"})
    t=t[0]

    url=await post("https://okfw.net/r=TB.get_item_url(cart_ids)")
    while( url&&url.length ){
        await tab_update(t,url)
        await rpc_sleep()
        await tab_exec(t, _CODE(function(){
            r=document.querySelector('.tb-btn-add > a')
            r.click()
        }))
        await rpc_sleep()
        ta=await tab_query({url: "https://cart.taobao.com/add_cart_succeed.htm*"})
        if(ta.length){
            t=ta[0]
            url=await post("https://okfw.net/r=TB.get_item_url(cart_ids)")
        }else{
            url 
        }

    }
    console.log('add cart done',new Date())
}
async function taobao_get_item(){
    t=await tab_query({url: "https://item.taobao.com/item.htm*"})
        
    while( t.length ){
        t=t[0]
        await tab_exec(t, _CODE(function(){
            async function main(){
                ts=Array.from(document.querySelectorAll('.tb-txt') ).map(i=>i.outerHTML)                
                await post("https://okfw.net/r=u=T.json_loads(request.get_data())",location.href)
                await post("https://okfw.net/r=ts=T.json_loads(request.get_data());dut[u]=ts",ts)
            }
            main()
			r=new Date()
        }))
        await sleep(1444)
        url=await post("https://okfw.net/r=u=yx_url()")
        await tab_update(t,url)  
        await sleep(1555)
        t=await tab_query({url: "https://item.taobao.com/item.htm*"})
    
    }
    console.log('done')
}

//////////////////////////////////////////////////////////////////
async function main(){
    if(!chrome.tabs)return
    return t=await tab_current()
    var img="https://img.alicdn.com/bao/uploaded/i3/2658592015/TB2Xk8McA.OyuJjSszhXXbZbVXa_!!2658592015.jpg_240x240.jpg"
    var ds=document.querySelectorAll('dl.item') 
    img=ds[5].querySelector('img')
    b=await get_img_b64(img)
//     console.log(b)
    return(b)
}


 main()

