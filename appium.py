from appium.webdriver.errorhandler import MobileErrorHandler
from appium.webdriver.switch_to import MobileSwitchTo	
from appium import webdriver

class MyWebDriverAppium(webdriver.Remote):	

	def __init__(self, command_executor='http://127.0.0.1:4723/wd/hub',
			 desired_capabilities=None, session_id=None):
		self.preserved_session_id = session_id

		self.error_handler = MobileErrorHandler()
		self._switch_to = MobileSwitchTo(self)

		# add new method to the `find_by_*` pantheon
		# By.IOS_UIAUTOMATION = MobileBy.IOS_UIAUTOMATION
		# By.IOS_PREDICATE = MobileBy.IOS_PREDICATE
		# By.ANDROID_UIAUTOMATOR = MobileBy.ANDROID_UIAUTOMATOR
		# By.ACCESSIBILITY_ID = MobileBy.ACCESSIBILITY_ID
		super(MyWebDriverAppium, self).__init__(command_executor, desired_capabilities)

	def start_session(self, desired_capabilities, browser_profile=None):
		if self.preserved_session_id:
			self.command_executor._commands['getSession'] = ('GET', '/session/$sessionId')
			self.session_id = self.preserved_session_id
			response = self.execute('getSession', {'sessionId ': self.session_id})
			self.session_id = response['sessionId']
			self.capabilities = response['value']
			self.w3c = response['status']
		else:
			super(MyWebDriverAppium, self).start_session(desired_capabilities, browser_profile)
			