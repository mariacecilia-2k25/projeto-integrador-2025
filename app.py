from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Cadastro, Consultas, Base
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

# --------------------------------
# Configuração do Banco de Dados
# --------------------------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Exemplo de URL para SQL Server:
# DATABASE_URL = "mssql+pyodbc://usuario:senha@SERVIDOR/NOME_DO_BANCO?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# --------------------------------
# Rotas de Páginas
# --------------------------------
@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

# Rota da página do administrador
@app.route('/clientes')
@app.route('/clientes.html')
def clientes():
    return render_template('admin/clientes.html')


# --------------------------------
# Rota: Cadastro
# --------------------------------
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    session = Session()
    try:
        data = request.get_json()

        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        telefone = data.get('telefone')
        cpf = data.get('cpf')

        # Verifica se e-mail já está cadastrado
        if session.query(Cadastro).filter_by(email=email).first():
            return jsonify({"erro": "❌ E-mail já cadastrado!"}), 400

        novo_usuario = Cadastro(
            nome=nome,
            email=email,
            senha=senha,
            telefone=telefone,
            cpf=cpf
        )

        session.add(novo_usuario)
        session.commit()

        return jsonify({"mensagem": "✅ Usuário cadastrado com sucesso!"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"erro": f"Erro ao cadastrar: {str(e)}"}), 500
    finally:
        session.close()

# --------------------------------
# Rota: Login
# --------------------------------
@app.route('/login', methods=['POST'])
def login():
    session = Session()
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        # login do admin direto no backend
        if email == "admin@gmail.com" and senha == "1234":
            return jsonify({"mensagem": "Bem-vindo, administrador!", "admin": True}), 200

        usuario = session.query(Cadastro).filter_by(email=email, senha=senha).first()

        if usuario:
            return jsonify({"mensagem": f"Bem-vindo(a), {usuario.nome}!", "admin": False}), 200
        else:
            return jsonify({"erro": "❌ Email ou senha incorretos!"}), 401

    except Exception as e:
        return jsonify({"erro": f"Erro no login: {str(e)}"}), 500
    finally:
        session.close()

# --------------------------------
# Rota: Agendamento
# --------------------------------
@app.route('/agendar', methods=['POST'])
def agendar():
    session = Session()
    try:
        data = request.get_json()
        email = data.get('email')
        data_consulta = datetime.strptime(data.get('data'), "%Y-%m-%d").date()
        hora = data.get('hora')
        medico = data.get('medico')

        nova_consulta = Consultas(
            email_cliente=email,
            data=data_consulta,
            horario=hora,
            medico=medico
        )

        session.add(nova_consulta)
        session.commit()

        return jsonify({"mensagem": "✅ Consulta agendada com sucesso!"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"erro": f"Erro ao agendar: {str(e)}"}), 500
    finally:
        session.close()

# --------------------------------
# Inicialização do servidor
# --------------------------------
if __name__ == '__main__':
    app.run(debug=True)
