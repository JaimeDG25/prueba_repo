#IMPORTACION PARA INCIAR FLASK
from flask import Flask,render_template,redirect,request,jsonify,url_for,session
from Settings.setting import get_sqlalchemy_uri,test_pyodbc_connection
from Models.model import Cotizaciones
from datetime import datetime
#a
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key="TU_API_KEY_AQUI")  
#DEFINIENDO UNA VARIABLE QUE SIRVA COMO INICIADOR
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'

from Models.model import db,Usuario
db.init_app(app)
with app.app_context():
    db.create_all()

#CREANDO UNA RUTA RAIZ PARA RETORNAR UN TEXTO
@app.route('/')
def login():
    consulta = Usuario.query.all()
    print(consulta)
    return render_template('login.html')
@app.route('/enviar_login', methods=['GET', 'POST'])
def enviar_login():
    if request.method == 'POST':
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        usuario = Usuario.query.filter_by(correo_usuario=correo, contraseña_usuario=contraseña).first()
        if usuario:
            session['correo_usuario'] = usuario.correo_usuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', mensaje='Correo o contraseña incorrectos'))
        return render_template('index.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 

@app.route('/index')
def index():
    correo = session.get('correo_usuario', 'Usuario no identificado')
    print(correo)
    return render_template('index.html',correo=correo)

@app.route('/enviar_datos', methods=['GET', 'POST'])
def enviar_datos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        tservicio = request.form['tservicio']
        descripcion = request.form['descripcion']
        #resultado_ia = analizar_con_ia(descripcion, tservicio)

        precios = {
            '1': 1500,
            '2': 2000,
            '3': 800
        }
        precio = precios.get(tservicio)
        # if not resultado_ia or "error" in resultado_ia:
        #     return jsonify({"error": resultado_ia.get("error", "Error desconocido")})
        if not precio:
            return jsonify({"error": "Tipo de servicio inválido"}), 400
        total = Cotizaciones.query.count() + 1
        numero_formateado = f"COT-2025-{str(total).zfill(4)}"
        nueva_cotizacion = Cotizaciones(
            numero_cotizacion=numero_formateado,
            nombrecliente_cotizacion=nombre,
            correocliente_cotizacion=correo,
            tservicio_cotizacion=tservicio,
            precio_cotizacion=precio,
            fcreacion_cotizacion=datetime.utcnow()
        )
        db.session.add(nueva_cotizacion)
        db.session.commit()

        return jsonify({
            "codigo_cotizacion": numero_formateado,
            "nombre": nombre,
            "correo": correo,
            "tipo_servicio": tservicio,
            "precio": precio,
            "descripciom":descripcion,
            "fecha_creacion": nueva_cotizacion.fcreacion_cotizacion.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template('index.html')    


# def analizar_con_ia(descripcion, tipo_servicio):
#     prompt = f"""
#     Analiza este caso legal: {descripcion}
#     Tipo de servicio: {tipo_servicio}

#     Evalúa:
#     1. Complejidad (Baja/Media/Alta)
#     2. Ajuste de precio recomendado (0%, 25%, 50%)
#     3. Servicios adicionales necesarios
#     4. Genera propuesta profesional para cliente
#     """

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Eres un asesor legal profesional."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             max_tokens=500
#         )

#         texto_generado = response['choices'][0]['message']['content']

#         return {
#             'complejidad': 'Media',
#             'ajuste_precio': 25,
#             'servicios_adicionales': ['Ejemplo: revisión de contratos'],
#             'propuesta_texto': texto_generado
#         }

#     except Exception as e:
#         print("Error al consultar OpenAI:", e)
#         return {"error": str(e)}


#DEFINIENDO EL MODO DESARROLLADOR Y EL PUERTO 
if __name__ == '__main__':
    app.run(debug=True, port=5000)