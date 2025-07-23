_TEXT=function(wrap) {return wrap.toString().match(/\/\*\s([\s\S]*)\s\*\//)[1];}  // 提取 /* 之间的内容 */
_CODE=function(wrap) {return wrap.toString().match(/function\s*\(\s*\)\s*{\s*([\s\S]*)\s*}/ )[1];}//auto trim { code_start_end_space }

function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms) )  }

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

async function taobao_search_list(base_url="https://youxin-electronic.taobao.com/"){

}


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
    console.log(await post(
"https://okfw.net/base_url=T.json_loads(request.get_data());r=start_time=[TB.init(base_url),U.stime()]",base_url),t )
    
    var base_search_url=base_url+"search.htm?orderType=price_asc&pageNo="
    var max=await post("https://okfw.net/r=TB.max_num()")
    var url=base_search_url+(parseInt(max)+1)
    while(url && url.length>9){
        var check=await post("https://okfw.net/url=T.json_loads(request.get_data());r=TB.include(url)",url)
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
        await rpc_sleep()
        for(var i of [0,1,2,3,4,5,6,7,8]){
           console.log(i)
           var next=await tab_exec(t, _CODE(function(){
               r=""
               var tmp=document.querySelector('.pagination-mini')

               var next=Array.from(tmp.querySelectorAll('a'))[1]
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
    

async function taobao_add_cart(asurl="https://okfw.net/r=TB.get_item_url(carts)"){
    if(!asurl.startsWith('https://'))asurl="https://okfw.net/r=TB.get_item_url("+asurl+")"
    ta=await tab_query({url: "https://cart.taobao.com/add_cart_succeed.htm*"})
    for(var t of ta){
        console.log(t.id,t.title)
        await tab_remove(t)
    }
    
    t=tid=(await tab_query()).map(t=>t.id)[0] // seems min id

    url=await post(asurl)
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
            url=await post(asurl)
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
    return console.log(eval('2+2'))
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

