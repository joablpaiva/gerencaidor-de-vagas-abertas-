# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao_cargo = db.Column(db.String(200), nullable=False)
    requisitos_obrigatorios = db.Column(db.String(500), nullable=False)
    requisitos_desejaveis = db.Column(db.String(500), nullable=True)
    remuneracao_mensal = db.Column(db.Float, nullable=False)
    beneficios = db.Column(db.String(200), nullable=True)
    local_trabalho = db.Column(db.String(100), nullable=False)
    preenchida = db.Column(db.Boolean, default=False)
