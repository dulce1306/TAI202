from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Esta URL la usarías si estuviéramos haciendo peticiones reales a FastAPI con 'requests'
API = "http://127.0.0.1:5000/v1/usuarios/" 

# Bd local ficticia
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Ali", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

@app.route('/')
def inicio():
    return render_template('index.html', usuarios=usuarios)

# RUTA PARA ACTUALIZAR
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    # Buscamos el usuario por ID en nuestra lista local
    for usuario in usuarios:
        if usuario['id'] == id:
            # Obtenemos los datos que vienen del formulario del index.html
            usuario['nombre'] = request.form.get('nombre')
            usuario['edad'] = int(request.form.get('edad'))
            break
    return redirect(url_for('inicio'))

# RUTA PARA ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global usuarios
    # Creamos una nueva lista excluyendo el ID seleccionado
    usuarios = [u for u in usuarios if u['id'] != id]
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    # Usamos el puerto 5001 para que no choque con FastAPI (8000) o el default (5000)
    app.run(debug=True, port=5001)