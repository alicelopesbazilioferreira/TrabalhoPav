from datetime import datetime
from app import db
class BaseModel(db.Model):    
    __abstract__ = True
    
    # Common fields for all models
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def to_dict(self):
        created_at_str = None
        if self.created_at is not None:
            try:
                created_at_str = self.created_at.isoformat()
            except AttributeError:
                created_at_str = str(self.created_at)
        
        return {
            'id': self.id,
            'created_at': created_at_str
        }
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def __repr__(self):
        """String representation of the model."""
        return f'<{self.__class__.__name__} id={self.id}>'
