from app.models.base_model import BaseModel
from app import db


class Exercicio(BaseModel):    
    __tablename__ = 'exercicios'
    
    # Exercise attributes
    tipo_exercicio = db.Column(db.String(100), nullable=False)
    quantidade_repeticoes = db.Column(db.Integer, nullable=False)
    ciclos = db.Column(db.Integer, nullable=False)
    pausa_entre_ciclos = db.Column(db.Integer, nullable=False)
    
    # Foreign key relationship
    dieta_id = db.Column(db.Integer, db.ForeignKey('dietas.id', ondelete='CASCADE'))
    
    def __init__(self, tipo_exercicio, quantidade_repeticoes, ciclos, pausa_entre_ciclos, dieta_id=None, **kwargs):
        super(Exercicio, self).__init__(**kwargs)
        self.tipo_exercicio = tipo_exercicio
        self.quantidade_repeticoes = quantidade_repeticoes
        self.ciclos = ciclos
        self.pausa_entre_ciclos = pausa_entre_ciclos
        self.dieta_id = dieta_id
    
    def get_tipo_exercicio(self):
        """Get the exercise type (encapsulation)."""
        return self.tipo_exercicio
    
    def set_tipo_exercicio(self, value):
        """Set the exercise type (encapsulation)."""
        self.tipo_exercicio = value
    
    def get_quantidade_repeticoes(self):
        """Get the number of repetitions (encapsulation)."""
        return self.quantidade_repeticoes
    
    def set_quantidade_repeticoes(self, value):
        """Set the number of repetitions (encapsulation)."""
        self.quantidade_repeticoes = value
    
    def get_ciclos(self):
        """Get the number of cycles (encapsulation)."""
        return self.ciclos
    
    def set_ciclos(self, value):
        """Set the number of cycles (encapsulation)."""
        self.ciclos = value
    
    def get_pausa_entre_ciclos(self):
        """Get the pause time between cycles (encapsulation)."""
        return self.pausa_entre_ciclos
    
    def set_pausa_entre_ciclos(self, value):
        """Set the pause time between cycles (encapsulation)."""
        self.pausa_entre_ciclos = value
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'tipo_exercicio': self.tipo_exercicio,
            'quantidade_repeticoes': self.quantidade_repeticoes,
            'ciclos': self.ciclos,
            'pausa_entre_ciclos': self.pausa_entre_ciclos,
            'dieta_id': self.dieta_id
        })
        return data
    
    def get_total_duration(self):
        if self.ciclos > 0:
            return (self.ciclos - 1) * self.pausa_entre_ciclos
        return 0
    
    @classmethod
    def get_by_dieta(cls, dieta_id):
        return cls.query.filter_by(dieta_id=dieta_id).all()
    
    def __repr__(self):
        """String representation of the exercise."""
        return f'<Exercicio id={self.id} tipo="{self.tipo_exercicio}">'
