from app import db
from app.models.exercicio import Exercicio
from app.validators.validators import ExercicioValidator, ValidationError
class ExercicioController:
    
    def __init__(self):
        """Constructor for ExercicioController."""
        self._validator = ExercicioValidator()
    
    def create(self, data):
        try:
            # Validate data
            self._validator.validate(data)
            
            # Create exercise instance
            exercicio = Exercicio(
                tipo_exercicio=data.get('tipo_exercicio'),
                quantidade_repeticoes=data.get('quantidade_repeticoes'),
                ciclos=data.get('ciclos'),
                pausa_entre_ciclos=data.get('pausa_entre_ciclos'),
                dieta_id=data.get('dieta_id')
            )
            
            # Save to database
            exercicio.save()
            
            return exercicio, None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def get_all(self):
        exercicios = Exercicio.get_all()
        return [e.to_dict() for e in exercicios]
    
    def get_by_id(self, id):
        exercicio = Exercicio.get_by_id(id)
        if not exercicio:
            return None, f'Exercício com ID {id} não encontrado'
        return exercicio.to_dict(), None
    
    def get_by_dieta(self, dieta_id):
        exercicios = Exercicio.get_by_dieta(dieta_id)
        return [e.to_dict() for e in exercicios]
    
    def update(self, id, data):
        try:
            # Get existing exercise
            exercicio = Exercicio.get_by_id(id)
            if not exercicio:
                return None, f'Exercício com ID {id} não encontrado'
            
            # Validate tipo_exercicio if present
            if 'tipo_exercicio' in data:
                self._validator.validate_not_empty(data['tipo_exercicio'], 'tipo_exercicio')
            
            # Validate quantidade_repeticoes if present
            if 'quantidade_repeticoes' in data:
                self._validator.validate_not_negative(data['quantidade_repeticoes'], 'quantidade_repeticoes')
            
            # Validate ciclos if present (Business rule: cannot be negative)
            if 'ciclos' in data:
                self._validator.validate_not_negative(data['ciclos'], 'ciclos')
            
            # Validate pausa_entre_ciclos if present
            if 'pausa_entre_ciclos' in data:
                self._validator.validate_not_negative(data['pausa_entre_ciclos'], 'pausa_entre_ciclos')
            
            # Validate dieta_id if present
            if 'dieta_id' in data and data['dieta_id'] is not None:
                self._validator.validate_dieta_exists(data['dieta_id'])
            
            # Update fields using loop
            allowed_fields = ['tipo_exercicio', 'quantidade_repeticoes', 'ciclos', 'pausa_entre_ciclos', 'dieta_id']
            update_data = {}
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            # Apply updates
            exercicio.update(**update_data)
            
            return exercicio.to_dict(), None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def delete(self, id):
        try:
            exercicio = Exercicio.get_by_id(id)
            if not exercicio:
                return False, f'Exercício com ID {id} não encontrado'
            
            exercicio.delete()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
