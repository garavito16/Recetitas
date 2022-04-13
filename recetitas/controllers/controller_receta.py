from flask import flash, redirect, render_template,request,session
from recetitas import app
from recetitas.models.model_receta import Receta

@app.route('/recipes/new')
def newReceta():
    if "id" in session:
        return render_template("formularioReceta.html",receta={"id":0})
    else:
        return redirect('/')

@app.route('/recipes/edit/<id>')
def editReceta(id):
    if "id" in session:
        data = {
            "id" : id
        }
        resultado = Receta.getRecetaXid(data)
        if(resultado != None):
            return render_template('formularioReceta.html',receta=resultado)
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/saveReceta',methods=['POST'])
def saveReceta():
    if "id" in session:
        data = {
            "nombre" : request.form["name"],
            "descripcion" : request.form["description"],
            "instrucciones" : request.form["instructions"],
            "fecha" : request.form["date_mode"],
            "usuario_id" :  session["id"],
            "tiempo" : request.form["tiempo"],
            "id" : request.form["identificador"]
        }
        if(request.form["identificador"] == "0"):
            if(Receta.verifyData(data)):
                resultado = Receta.addReceta(data)
                if(resultado > 0):
                    return redirect('/dashboard')
                else:
                    flash("ocurrio un error al intentar guardar la receta","receta")
                    return redirect('/recipes/new')
            else:
                return redirect('/recipes/new')
        else:
            if(Receta.verifyData(data)):
                resultado = Receta.updateReceta(data)
                print(resultado)
                if(resultado == None):
                    return redirect('/dashboard')
                else:
                    flash("ocurrio un error al intentar actualizar la receta","receta")
                    return redirect('/recipes/edit/'+request.form["identificador"])
            else:
                return redirect('/recipes/edit/'+request.form["identificador"])
    else:
        return redirect('/')

@app.route('/recipes/<id>')
def viewReceta(id):
    if "id" in session:
        data = {
            "id" : id
        }
        resultado = Receta.getRecetaXid(data)
        if(resultado != None):
            return render_template('viewReceta.html',receta=resultado)
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/recipes/delete/<id>')
def deleteReceta(id):
    if "id" in session:
        data = {
            "id" : id
        }
        Receta.deleteReceta(data)
        return redirect('/dashboard')
    else:
        return redirect('/') 