from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv, find_dotenv
import pineapi as pa
import carga as carga
from datetime import datetime


load_dotenv(find_dotenv(), override = True)
os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/admin/<string:index_name>', methods=['GET'])
def borrar_indices(index_name):
    respuesta = pa.borrar_indices(index_name)
    return jsonify({"mensaje": respuesta})

#crear indices
@app.route('/admin', methods=['POST'])
def crear_indices():
    global vectores
    request1 = request.json
    index_name = request1['index_name']
    documento = request1['documento']
    contenido = carga.cargar_documento(documento)
    fragmentos = carga.fragmentar(contenido, 150)
    costo_openai = carga.costo_embedding(fragmentos)
    print(len(fragmentos))
    vectores, mensaje = pa.creando_vectores(index_name, fragmentos)
    return jsonify({"contenido": len(contenido), "mensajes": mensaje, "costo": costo_openai })
#metodos de consulta
#metodo para consultar por ingrediente
@app.route('/consulta', methods=['POST'])
def consulta():
    request1 = request.json
    consulta_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pregunta = "Del documento proporcionado: "+request1['pregunta']
    respuesta = pa.consultas(request1['index_name'], pregunta)
    return jsonify({"fecha_consulta": consulta_date, "respuesta": respuesta})

@app.route('/consulta/memoria', methods=['POST'])
def consulta_receta():
    global memoria
    request1 = request.json
    consulta_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pregunta = "Del documento proporcionado o de cualquier fuente de informacion  : " + request1['pregunta']
    respuesta, memoria = pa.consulta_con_memoria(vectores, pregunta, memoria)
    return jsonify({"fecha_consulta": consulta_date, "respuesta": respuesta})


if __name__ == '__main__':
    app.run()