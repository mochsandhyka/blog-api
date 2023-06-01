from app import app
from app.controllers import user

app.route('/user/create',methods = ['POST'])(user.create_user)
