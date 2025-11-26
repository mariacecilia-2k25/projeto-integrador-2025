import os
from sqlalchemy import create_engine, Column, String, Integer, Date, Time, ForeignKey, CHAR
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

# Carregar o arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

# -------------------------------
# Tabela de Cadastro
# -------------------------------
class Cadastro(Base):
    __tablename__ = 'cadastro'

    email = Column(String(100), primary_key=True)
    nome = Column(String(100), nullable=False)
    senha = Column(String(50), nullable=False)
    telefone = Column(String(15), unique=True)
    cpf = Column(CHAR(11), unique=True)

    # Relacionamento 1:N com Consultas
    consultas = relationship("Consultas", back_populates="cliente")

# -------------------------------
# Tabela de Consultas
# -------------------------------
class Consultas(Base):
    __tablename__ = 'consultas'

    id_consulta = Column(Integer, primary_key=True, autoincrement=True)
    email_cliente = Column(String(100), ForeignKey('cadastro.email'))  # ✅ Faltava o ForeignKey aqui
    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    medico = Column(String(100))

    # Relacionamento inverso
    cliente = relationship("Cadastro", back_populates="consultas")

# -------------------------------
# Tabela de Login
# -------------------------------
class Login(Base):
    __tablename__ = 'login'

    id_login = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), ForeignKey('cadastro.email'))
    senha = Column(String(50), nullable=False)

# -------------------------------
# Criação do banco de dados
# -------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print("✅ Banco de dados criado com sucesso!")
