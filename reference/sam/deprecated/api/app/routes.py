from app import app

@app.route('/')
@app.route('/index')
def index():
   user = {'username': 'Jesse'}
   return f'''
   <html>
      <head>
         <title>Home Page - Microblog</title>
      </head>
      <body>
         <h1>Hello, {user['username']}!</h1>
      </body>
   </html>
   '''
@app.route('/listen')
def listen():
   return
   
@app.route('/sync')
def sync():
   return

def fetchFromMongo():
   return

def insertIntoMongo():
   return
