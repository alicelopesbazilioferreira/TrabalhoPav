from sqlalchemy import JSON
from app.models.base_model import BaseModel
from app import db


class Refeicao(BaseModel):
    __tablename__ = 'refeicoes'
    
    # Meal attributes
    tipo_refeicao = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    # Use JSON type for compatibility with both SQLite and PostgreSQL
    alimentos = db.Column(JSON, nullable=False)
    
    # Foreign key relationship
    dieta_id = db.Column(db.Integer, db.ForeignKey('dietas.id', ondelete='CASCADE'))
    
    # Valid meal types
    TIPOS_VALIDOS = ['café da manhã', 'almoço', 'jantar', 'lanche', 'ceia', 'pré-treino', 'pós-treino']
    
    def __init__(self, tipo_refeicao, quantidade, alimentos, dieta_id=None, **kwargs):
        super(Refeicao, self).__init__(**kwargs)
        self.tipo_refeicao = tipo_refeicao
        self.quantidade = quantidade
        self.alimentos = alimentos if isinstance(alimentos, list) else [alimentos]
        self.dieta_id = dieta_id
    
    def get_tipo_refeicao(self):
        """Get the meal type (encapsulation)."""
        return self.tipo_refeicao
    
    def set_tipo_refeicao(self, value):
        """Set the meal type (encapsulation)."""
        self.tipo_refeicao = value
    
    def get_quantidade(self):
        """Get the quantity (encapsulation)."""
        return self.quantidade
    
    def set_quantidade(self, value):
        """Set the quantity (encapsulation)."""
        self.quantidade = value
    
    def get_alimentos(self):
        """Get the list of foods (encapsulation)."""
        return self.alimentos
    
    def set_alimentos(self, value):
        """Set the list of foods (encapsulation)."""
        self.alimentos = value if isinstance(value, list) else [value]
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'tipo_refeicao': self.tipo_refeicao,
            'quantidade': self.quantidade,
            'alimentos': self.alimentos,
            'dieta_id': self.dieta_id
        })
        return data
    
    def add_alimento(self, alimento):
        if self.alimentos is None:
            self.alimentos = []
        if alimento not in self.alimentos:
            self.alimentos = self.alimentos + [alimento]
            db.session.commit()
    
    def remove_alimento(self, alimento):
        if self.alimentos and alimento in self.alimentos:
            self.alimentos = [a for a in self.alimentos if a != alimento]
            db.session.commit()
    
    @classmethod
    def get_by_dieta(cls, dieta_id):
        return cls.query.filter_by(dieta_id=dieta_id).all()
    
    def __repr__(self):
        """String representation of the meal."""
        return f'<Refeicao id={self.id} tipo="{self.tipo_refeicao}">'
