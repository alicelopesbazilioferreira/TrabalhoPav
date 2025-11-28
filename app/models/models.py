# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# db = SQLAlchemy()

# # Tabelas de associação para relacionamentos many-to-many
# dieta_refeicao = db.Table('dieta_refeicao',
#     db.Column('dieta_id', db.Integer, db.ForeignKey('dieta.id'), primary_key=True),
#     db.Column('refeicao_id', db.Integer, db.ForeignKey('refeicao.id'), primary_key=True)
# )

# dieta_exercicio = db.Table('dieta_exercicio',
#     db.Column('dieta_id', db.Integer, db.ForeignKey('dieta.id'), primary_key=True),
#     db.Column('exercicio_id', db.Integer, db.ForeignKey('exercicio.id'), primary_key=True)
# )

# class Dieta(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     descricao = db.Column(db.Text)
#     objetivo = db.Column(db.String(100))
#     duracao_dias = db.Column(db.Integer)
#     data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relacionamentos many-to-many
#     refeicoes = db.relationship('Refeicao', secondary=dieta_refeicao, lazy='subquery',
#                                backref=db.backref('dietas', lazy=True))
#     exercicios = db.relationship('Exercicio', secondary=dieta_exercicio, lazy='subquery',
#                                 backref=db.backref('dietas', lazy=True))

# class Refeicao(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     tipo = db.Column(db.String(50))  # café da manhã, almoço, jantar, lanche
#     ingredientes = db.Column(db.Text)
#     calorias = db.Column(db.Integer)
#     proteinas = db.Column(db.Float)
#     carboidratos = db.Column(db.Float)
#     gorduras = db.Column(db.Float)
#     tempo_preparo = db.Column(db.Integer)  # em minutos
#     data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# class Exercicio(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     tipo = db.Column(db.String(50))  # cardio, força, flexibilidade
#     descricao = db.Column(db.Text)
#     duracao_minutos = db.Column(db.Integer)
#     calorias_queimadas = db.Column(db.Integer)
#     nivel_dificuldade = db.Column(db.String(20))  # fácil, médio, difícil
#     equipamentos = db.Column(db.Text)
#     data_criacao = db.Column(db.DateTime, default=datetime.utcnow)