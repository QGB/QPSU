from microdot import Microdot

app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world!'

app.run()