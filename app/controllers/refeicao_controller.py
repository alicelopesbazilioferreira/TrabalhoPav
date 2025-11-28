from app import db
from app.models.refeicao import Refeicao
from app.validators.validators import RefeicaoValidator, ValidationError
class RefeicaoController:
    def __init__(self):
        """Constructor for RefeicaoController."""
        self._validator = RefeicaoValidator()
    
    def create(self, data):
        try:
            # Validate data
            self._validator.validate(data)
            
            # Process alimentos list
            alimentos = data.get('alimentos', [])
            if isinstance(alimentos, str):
                alimentos = [alimentos]
            
            # Create meal instance
            refeicao = Refeicao(
                tipo_refeicao=data.get('tipo_refeicao'),
                quantidade=data.get('quantidade'),
                alimentos=alimentos,
                dieta_id=data.get('dieta_id')
            )
            
            # Save to database
            refeicao.save()
            
            return refeicao, None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def get_all(self):
        refeicoes = Refeicao.get_all()
        return [r.to_dict() for r in refeicoes]
    
    def get_by_id(self, id):
        refeicao = Refeicao.get_by_id(id)
        if not refeicao:
            return None, f'Refeição com ID {id} não encontrada'
        return refeicao.to_dict(), None
    
    def get_by_dieta(self, dieta_id):
        refeicoes = Refeicao.get_by_dieta(dieta_id)
        return [r.to_dict() for r in refeicoes]
    
    def update(self, id, data):
        try:
            # Get existing meal
            refeicao = Refeicao.get_by_id(id)
            if not refeicao:
                return None, f'Refeição com ID {id} não encontrada'
            
            # Validate tipo_refeicao if present
            if 'tipo_refeicao' in data:
                self._validator.validate_not_empty(data['tipo_refeicao'], 'tipo_refeicao')
                self._validator.validate_tipo_refeicao(data['tipo_refeicao'])
            
            # Validate quantidade if present
            if 'quantidade' in data:
                self._validator.validate_not_negative(data['quantidade'], 'quantidade')
            
            # Validate alimentos if present
            if 'alimentos' in data:
                self._validator.validate_list_not_empty(data['alimentos'], 'alimentos')
            
            # Validate dieta_id if present
            if 'dieta_id' in data and data['dieta_id'] is not None:
                self._validator.validate_dieta_exists(data['dieta_id'])
            
            # Update fields using loop
            allowed_fields = ['tipo_refeicao', 'quantidade', 'alimentos', 'dieta_id']
            update_data = {}
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            # Apply updates
            refeicao.update(**update_data)
            
            return refeicao.to_dict(), None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def delete(self, id):
        try:
            refeicao = Refeicao.get_by_id(id)
            if not refeicao:
                return False, f'Refeição com ID {id} não encontrada'
            
            refeicao.delete()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
