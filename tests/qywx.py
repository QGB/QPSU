from corpwechatbot.app import AppMsgSender
app = AppMsgSender(**U.get_or_dill_load_and_set('d3_qywx'))  
app.send_text(content="如果我是DJ，你会爱我吗？")