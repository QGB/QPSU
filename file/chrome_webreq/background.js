var rule = {
conditions: [
  new chrome.declarativeWebRequest.RequestMatcher({url: {hostContains: '.zhimg.'}})
  // RequestMatcher(	  {url: {urlEquals: getURLHttpSimpleLoad() }  }   ),
],
actions: [
  // new chrome.declarativeWebRequest.SendMessageToExtension(
	  // {message: EVENT_MESSAGE_EXTENSION_STRING}),
	 new chrome.declarativeWebRequest.CancelRequest()

],
};
chrome.declarativeWebRequest.onRequest.addRules([rule], function() {
	// chrome.tabs.create({"url": 'http://qq.com'});
	console.log('addRules:',rule)
});