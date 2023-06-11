from jnius import autoclass, PythonJavaClass, cast, java_method

Context =  autoclass('android.content.Context')
Parcelable = autoclass('android.os.Parcelable')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
String  = autoclass('java.lang.String')
NokeDeviceManagerService = autoclass('com.noke.nokemobilelibrary.NokeDeviceManagerService')
NokeDevice = autoclass('com.noke.nokemobilelibrary.NokeDevice')
NokeMobileError = autoclass('com.noke.nokemobilelibrary.NokeMobileError')


class NokeApi():
    def __init__(self, util):
        self.python_activity = PythonActivity.mActivity
        self.service_connection = ServiceConnection()
        self.service_connection.addCallback(util)

    def initiateNokeService(self):
        currentActivity = cast('android.app.Activity', self.python_activity)
        context = cast('android.content.Context', currentActivity.getApplicationContext())

        nokeIntent = Intent()
        nokeIntent.setClassName(context, 'com.noke.nokemobilelibrary.NokeDeviceManagerService')
        self.python_activity.bindService(nokeIntent, self.service_connection, Context.BIND_AUTO_CREATE)


class ServiceConnection(PythonJavaClass):
    __javainterfaces__ = ['android.content.ServiceConnection']
    __javacontext__ = 'app'

    def addCallback(self, util):
        self.util = util

    @java_method('(Landroid/content/ComponentName;Landroid/os/IBinder;)V')
    def onServiceConnected(self, className, rawBinder):
        global mNokeService
        nokeService = cast('com.noke.nokemobilelibrary.NokeDeviceManagerService$LocalBinder',rawBinder)
        mNokeService = nokeService.getService()
        mNokeService.setAllowAllDevices(True)
        self.util.NokeServiceListener = NokeServiceListener(self.util)
        mNokeServiceListener = self.util.NokeServiceListener
        mNokeService.registerNokeListener(mNokeServiceListener)
        print('noke name')
        print(self.util.nokeName)
        print('noke name')
        print(self.util.nokeMac)
        jName = cast('java.lang.String', String(self.util.nokeName))
        jMac = cast('java.lang.String', String(self.util.nokeMac))
        noke1 = NokeDevice(jName, jMac)
        mNokeService.addNokeDevice(noke1)
        mNokeService.setUploadUrl("https://coreapi-sandbox.appspot.com/upload/")
        mNokeService.startScanningForNokeDevices()

        if not mNokeService.initialize():
            print("Unable to initialize Bluetooth")
        print('initializing')

    @java_method('(Landroid/content/ComponentName;)V')
    def onServiceDisconnected(classname):
        mNokeService = None


class NokeServiceListener(PythonJavaClass):
    __javainterfaces__ = ['com.noke.nokemobilelibrary.NokeServiceListener']
    __javacontext__ = 'app'

    def __init__(self, util):
        super(NokeServiceListener, self).__init__()
        self.util = util

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeDiscovered(self, noke):
        self.util.NokeCallback = "Connecting"
        mNokeService.connectToNoke(noke)
        print("Discovered Noke")

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeConnecting(self, noke):
        self.util.NokeCallback = "Connecting"
        print('Connecting to Noke')

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeConnected(self, noke):
        print("Noke Connected")
        self.util.NokeCallback = "Connected"
        mNokeService.stopScanning()
        self.request_unluck(noke)

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeSyncing(self, noke):
        print("NOKE SYNCING")
        self.util.NokeCallback = "SYNCING"

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeUnlocked(self, noke):
        print('Noke Unlocked')
        self.util.NokeCallback = "Unlocked"

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;)V')
    def onNokeDisconnected(self, noke):
        print("Noke Disconnected")
        self.util.NokeCallback = "Disconnected"
        mNokeService.startScanningForNokeDevices();
        mNokeService.setBluetoothScanDuration(20);

    @java_method('(I)V')
    def onBluetoothStatusChanged(self, bluetoothStatus):
        print(bluetoothStatus)

    @java_method('(Lcom/noke/nokemobilelibrary/NokeDevice;ILjava/lang/String;)V')
    def onError(self, noke, error, message):
        self.utility.NokeCallback = "Error"
        print(error)
        print(message)

    def request_unluck(self, noke):
        data = {"session": str(noke.getSession()), "mac": str(noke.getMac())}
        result = self.util.sendNokeMessage(data)
        command_str = result['data']["commands"]
        noke.sendCommands(command_str)