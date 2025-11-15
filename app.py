from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime
import requests
from urllib.parse import unquote
from urllib.parse import quote
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# === Configurações da conexão com o MySQL ===
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv("DB_PASSWORD"),
    'database': 'webapp_postagens'
}

# --- Função de conexão com o banco ---
def conectar_db():
    return mysql.connector.connect(**DB_CONFIG)

# === Página inicial ===
@app.route('/')
def home():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM paginas")
    paginas = cursor.fetchall()
    conn.close()
    return render_template('form.html', paginas=paginas)

# === Página de cadastro ===
@app.route('/cadastro')
def cadastro():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM paginas")
    paginas = cursor.fetchall()
    conn.close()
    return render_template('cadastro.html', paginas=paginas)

# === Salvar cadastro ===
@app.route('/salvar_pagina', methods=['POST'])
def salvar_pagina():
    try:
        nome = request.form['nome']
        page_id = request.form['page_id']
        access_token = request.form['access_token']
        data_expiracao = request.form['data_expiracao']

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO paginas (nome, page_id, access_token, data_expiracao)
            VALUES (%s, %s, %s, %s)
        """, (nome, page_id, access_token, data_expiracao))
        conn.commit()
        conn.close()

        return redirect(url_for('lista_pagina'))
    except Exception as e:
        return f"Erro ao salvar página: {e}"

# === Listar páginas cadastradas ===
@app.route('/lista_pagina')
def lista_pagina():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paginas")
    paginas = cursor.fetchall()
    conn.close()
    return render_template('lista_pagina.html', paginas=paginas)

# === Postagem automática em todas as páginas ===
@app.route('/postar', methods=['POST'])
def postar():
    mensagem = request.form.get('mensagem', '').strip()
    hashtags = request.form.get('hashtags', '').strip()
    link = request.form.get('link', '').strip()
    imagem = request.files.get('imagem')

    # --- Corrige e garante link puro ---
    if link:
        link = link.replace('|', '-')  # decodifica se já estiver escapado

    # --- Monta o texto final do post ---
    texto_final = mensagem
    if hashtags:
        texto_final += f"\n\n{hashtags}"
    if link:
        texto_final += f"\n\n{link}"  # sem quote()

    # --- Verifica se há conteúdo mínimo ---
    if not texto_final.strip() and (not imagem or not imagem.filename):
        return "Mensagem vazia!", 400

    # --- Busca as páginas cadastradas ---
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, page_id, access_token FROM paginas")
    paginas = cursor.fetchall()
    conn.close()

    if not paginas:
        return "Nenhuma página cadastrada!", 400

    resultados = []

    for nome, page_id, token in paginas:
        try:
            if imagem and imagem.filename:
                imagem.stream.seek(0, 2)
                tamanho = imagem.stream.tell()
                imagem.stream.seek(0)

                if tamanho > 0:
                    url = f"https://graph.facebook.com/{page_id}/photos"
                    files = {'source': imagem.stream}
                    data = {'caption': texto_final, 'access_token': token}
                    r = requests.post(url, files=files, data=data)
                else:
                    url = f"https://graph.facebook.com/{page_id}/feed"
                    data = {'message': texto_final, 'access_token': token}
                    r = requests.post(url, data=data)
            else:
                url = f"https://graph.facebook.com/{page_id}/feed"
                data = {'message': texto_final, 'access_token': token}
                r = requests.post(url, data=data)

            if r.status_code == 200:
                resultados.append(f"✅ Post enviado com sucesso para {nome}")
            else:
                erro = r.json().get('error', {}).get('message', r.text)
                resultados.append(f"⚠️ Falha ao postar em {nome}: {erro}")

        except Exception as e:
            resultados.append(f"❌ Erro em {nome}: {e}")

    return render_template("resultado.html", resultados=resultados)

# === API para consultar páginas cadastradas ===
@app.route('/api/paginas')
def api_paginas():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, page_id, access_token, data_expiracao FROM paginas")
    paginas = cursor.fetchall()
    conn.close()
    return jsonify(paginas)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
