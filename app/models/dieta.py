from app.models.base_model import BaseModel
from app import db
class Dieta(BaseModel):    
    __tablename__ = 'dietas'
    
    # Diet attributes
    meta = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    
    # Relationships - bidirectional
    refeicoes = db.relationship(
        'Refeicao',
        backref='dieta',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    exercicios = db.relationship(
        'Exercicio',
        backref='dieta',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, meta, descricao=None, **kwargs):
        super(Dieta, self).__init__(**kwargs)
        self.meta = meta
        self.descricao = descricao
    
    def get_meta(self):
        """Get the diet goal (encapsulation)."""
        return self.meta
    
    def set_meta(self, value):
        """Set the diet goal (encapsulation)."""
        self.meta = value
    
    def get_descricao(self):
        """Get the diet description (encapsulation)."""
        return self.descricao
    
    def set_descricao(self, value):
        """Set the diet description (encapsulation)."""
        self.descricao = value
    
    def to_dict(self, include_relations=False):
        data = super().to_dict()
        data.update({
            'meta': self.meta,
            'descricao': self.descricao
        })
        
        # Conditionally include relationships
        if include_relations:
            data['refeicoes'] = [r.to_dict() for r in self.refeicoes]
            data['exercicios'] = [e.to_dict() for e in self.exercicios]
        else:
            data['refeicoes_count'] = self.refeicoes.count()
            data['exercicios_count'] = self.exercicios.count()
        
        return data
    
    def add_refeicao(self, refeicao):
        self.refeicoes.append(refeicao)
        db.session.commit()
    
    def add_exercicio(self, exercicio):
        self.exercicios.append(exercicio)
        db.session.commit()
    
    def __repr__(self):
        """String representation of the diet."""
        return f'<Dieta id={self.id} meta="{self.meta}">'
