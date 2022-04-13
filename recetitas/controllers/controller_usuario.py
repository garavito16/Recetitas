
from flask import flash, redirect, render_template,request,session
from recetitas import app
from recetitas.models.model_usuario import User
from recetitas.models.model_receta import Receta
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def load_initial():
    return render_template('index.html')

@app.route('/dashboard')
def load_dashboard():
    if("id" in session):
        recetas = Receta.getAllReceta()
        return render_template('dashboard.html',recetas=recetas)
    else:
        return redirect('/')

@app.route('/register',methods=['POST'])
def register():
    user = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "confirm_password" : request.form["confirm_password"]
    }
    if(User.verifyData(user)):
        user["password"] = bcrypt.generate_password_hash(request.form["password"])
        resultado = User.addUser(user)
        if(resultado > 0):
            session["usuario"] = user["first_name"] + " " + user["last_name"]
            session["id"] = resultado
            session["email"] = user["email"]
            return redirect('/dashboard')
        else:
            flash('Ocurrió un error al intentar guardar los datos','registro')
            return redirect('/')
    else:
        return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    user = {
        "email" : request.form["email_login"],
        "password" : request.form["password_login"]
    }
    if(User.verifyDataLogin(user)):
        resultado = User.userXLogin(user)
        if(resultado != None):
            if(bcrypt.check_password_hash(resultado.password,user["password"])):
                session["usuario"] = resultado.nombres + " " + resultado.apellidos
                session["id"] = resultado.id
                session["email"] = user["email"]
                return redirect('/dashboard')
            else:
                flash("Credenciales incorrectas","login")
                return redirect('/')
        else:
            flash("No existe un usuario con el correo ingresado","login")
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')