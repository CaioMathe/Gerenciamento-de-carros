from statistics import mode
from urllib import request
from flask import Flask, render_template, request, redirect
import sqlite3 
import os
app = Flask(__name__)

_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        connection = sqlite3.connect(_dir + '\\town.db')
        cursor = connection.cursor()
        query = "SELECT * FROM clientes;"
        result = cursor.execute(query)
        result = result.fetchall()
        
        # ------------Dados dos Carros-----
        query = f"SELECT * FROM carros;"
        carros = cursor.execute(query)
        carros = carros.fetchall()
        # ------------Dados dos Carros á venda-----
        query = f"SELECT * FROM venda;"
        venda = cursor.execute(query)
        venda = venda.fetchall()
        return render_template("index.html", dados=result, carros=carros, venda=venda)
            
    except:
        return render_template("index.html")

@app.route('/cadastro/cliente', methods=['POST'])
def cadastro_cliente_post():
            nome = request.form['Nome']
            connection = sqlite3.connect(_dir + '\\town.db')
            cursor = connection.cursor()
            query = f"INSERT INTO clientes (nome, carros) VALUES ( '{nome}', 4);"
            cursor.execute(query)
            connection.commit()
            return redirect("/")


@app.route('/cadastro/cliente')
def cadastro_cliente():
    return render_template('cadastro_cliente.html')

@app.route('/cadastro/carros', methods=['POST'])
def cadastro_carros_post():
            modelo = request.form['modelo']
            id_cliente = request.form['id_cliente']
            cor = request.form['cor']
            connection = sqlite3.connect(_dir + '\\town.db')
            cursor = connection.cursor()
            query1 = f"SELECT * FROM carros WHERE id_cliente = {id_cliente};"
            result = cursor.execute(query1)
            result = result.fetchall()
            resultado_count = len(result) + 1
            if(resultado_count > 3):
                # mensagem = "Você não pode adicionar mais que 3 carros a um cliente"
                return redirect("/cadastro/carros")
            else:
                query = f"INSERT INTO carros (modelo, id_cliente, cor, venda) VALUES ( '{modelo}', {id_cliente}, '{cor}', 'N');"
                cursor.execute(query)
                connection.commit()
                return redirect("/")

@app.route('/cadastro/carros', methods=['GET'])
def cadastro_carros():
    connection = sqlite3.connect(_dir + '\\town.db')
    cursor = connection.cursor()
    query = "SELECT * FROM clientes;"
    result = cursor.execute(query)
    result = result.fetchall()
    return render_template('cadastro_carro.html', dados=result)

@app.route('/cliente/<int:id>')
def cliente(id):
    connection = sqlite3.connect(_dir + '\\town.db')
    cursor = connection.cursor()

    # ------------Dados do Cliente-----
    query = f"SELECT * FROM clientes where id = {id};"
    cliente = cursor.execute(query)
    cliente = cliente.fetchall()[0]
    # ------------Dados dos Carros-----
    query = f"SELECT * FROM carros where id_cliente = {id};"
    result = cursor.execute(query)
    result = result.fetchall()

    return render_template('cliente.html', cliente=cliente, carros=result)


@app.route('/venda/<int:id>/<int:id_cliente>/<string:modelo>/<string:cor>', methods=['POST', 'GET'])
def venda_post(id, id_cliente, modelo, cor):
        connection = sqlite3.connect(_dir + '\\town.db')
        cursor = connection.cursor()
        query = f"INSERT INTO venda (id_cliente, id_carro, modelo, cor) VALUES ({id_cliente}, {id}, '{modelo}', '{cor}');"
        cursor.execute(query)
        connection.commit()

        query2 = f"UPDATE carros SET venda = 'S' WHERE id = {id};"
        cursor.execute(query2)
        connection.commit()
        return redirect(f"/")

@app.route('/finalizar-venda/', methods=['POST', 'GET'])
def compra_post():
            id_cliente = request.form['id_cliente']
            modelo = request.form['modelo']
            cor = request.form['cor']
            id = request.form['id']
            connection = sqlite3.connect(_dir + '\\town.db')
            cursor = connection.cursor()
            query1 = f"SELECT * FROM carros WHERE id_cliente = {id_cliente};"
            result = cursor.execute(query1)
            result = result.fetchall()
            resultado_count = len(result) + 1
            if(resultado_count > 3):
                return redirect("/")
            else:
                query = f"INSERT INTO carros (modelo, id_cliente, cor, venda) VALUES ( '{modelo}', {id_cliente}, '{cor}', 'N');"
                cursor.execute(query)
                connection.commit()
                
                query2 = f"DELETE FROM venda WHERE id = {id}"
                cursor.execute(query2)
                connection.commit()
                return redirect("/")


@app.route('/finalizar-venda/<int:id>')
def compra(id):
    connection = sqlite3.connect(_dir + '\\town.db')
    cursor = connection.cursor()

    query = "SELECT * FROM clientes;"
    result = cursor.execute(query)
    result = result.fetchall()
    
    query1 = f"SELECT * FROM venda WHERE id = {id};"
    carro = cursor.execute(query1)
    carro = carro.fetchall()[0]

    return render_template('compra.html', clientes = result, carro = carro)