"""
Validators Module
Contains validation classes for business rules.
Implements OOP patterns with encapsulation and inheritance.
"""


class ValidationError(Exception):
    """
    Custom exception for validation errors.
    
    Attributes:
        message: Error message
        field: Field that failed validation
    """
    
    def __init__(self, message, field=None):
        """
        Constructor for ValidationError.
        
        Args:
            message: Error message
            field: Field that failed validation (optional)
        """
        super().__init__(message)
        self._message = message
        self._field = field
    
    @property
    def message(self):
        """Get the error message."""
        return self._message
    
    @property
    def field(self):
        """Get the field that failed validation."""
        return self._field
    
    def to_dict(self):
        """Convert error to dictionary."""
        return {
            'error': self._message,
            'field': self._field
        }


class BaseValidator:
    """
    Base validator class.
    Provides common validation functionality.
    Demonstrates inheritance pattern.
    """
    
    @staticmethod
    def validate_not_empty(value, field_name):
        """
        Validate that a value is not empty.
        
        Args:
            value: Value to validate
            field_name: Name of the field being validated
            
        Raises:
            ValidationError: If value is empty
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f'{field_name} não pode estar vazio', field_name)
    
    @staticmethod
    def validate_not_negative(value, field_name):
        """
        Validate that a numeric value is not negative.
        
        Args:
            value: Value to validate
            field_name: Name of the field being validated
            
        Raises:
            ValidationError: If value is negative
        """
        if value is not None and value < 0:
            raise ValidationError(f'{field_name} não pode ser negativo', field_name)
    
    @staticmethod
    def validate_positive(value, field_name):
        """
        Validate that a numeric value is positive.
        
        Args:
            value: Value to validate
            field_name: Name of the field being validated
            
        Raises:
            ValidationError: If value is not positive
        """
        if value is None or value <= 0:
            raise ValidationError(f'{field_name} deve ser um valor positivo', field_name)
    
    @staticmethod
    def validate_list_not_empty(value, field_name):
        """
        Validate that a list is not empty.
        
        Args:
            value: List to validate
            field_name: Name of the field being validated
            
        Raises:
            ValidationError: If list is empty
        """
        if not value or not isinstance(value, list) or len(value) == 0:
            raise ValidationError(f'{field_name} não pode estar vazia', field_name)


class DietaValidator(BaseValidator):
    """
    Validator for Dieta (Diet) model.
    Inherits from BaseValidator.
    """
    
    def __init__(self):
        """Constructor for DietaValidator."""
        super().__init__()
    
    def validate(self, data):
        """
        Validate diet data.
        
        Args:
            data: Dictionary with diet data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        self.validate_not_empty(data.get('meta'), 'meta')
        
        return data
    
    def validate_refeicao_exists(self, refeicao_id, db_session):
        """
        Validate that a meal exists before associating with diet.
        Business rule: Cannot associate non-existent meals.
        
        Args:
            refeicao_id: ID of the meal to validate
            db_session: Database session
            
        Raises:
            ValidationError: If meal does not exist
        """
        from app.models.refeicao import Refeicao
        refeicao = Refeicao.get_by_id(refeicao_id)
        if not refeicao:
            raise ValidationError(
                f'Refeição com ID {refeicao_id} não existe',
                'refeicao_id'
            )
        return refeicao
    
    def validate_exercicio_exists(self, exercicio_id, db_session):
        """
        Validate that an exercise exists before associating with diet.
        Business rule: Cannot associate non-existent exercises.
        
        Args:
            exercicio_id: ID of the exercise to validate
            db_session: Database session
            
        Raises:
            ValidationError: If exercise does not exist
        """
        from app.models.exercicio import Exercicio
        exercicio = Exercicio.get_by_id(exercicio_id)
        if not exercicio:
            raise ValidationError(
                f'Exercício com ID {exercicio_id} não existe',
                'exercicio_id'
            )
        return exercicio


class RefeicaoValidator(BaseValidator):
    """
    Validator for Refeicao (Meal) model.
    Inherits from BaseValidator.
    """
    
    # Valid meal types - pre-computed as class constant
    TIPOS_VALIDOS = [
        'café da manhã', 
        'almoço', 
        'jantar', 
        'lanche', 
        'ceia', 
        'pré-treino', 
        'pós-treino'
    ]
    # Pre-computed lowercase version for validation
    TIPOS_VALIDOS_LOWER = [t.lower() for t in TIPOS_VALIDOS]
    
    def __init__(self):
        """Constructor for RefeicaoValidator."""
        super().__init__()
    
    def validate(self, data):
        """
        Validate meal data.
        
        Args:
            data: Dictionary with meal data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate tipo_refeicao
        tipo = data.get('tipo_refeicao')
        self.validate_not_empty(tipo, 'tipo_refeicao')
        self.validate_tipo_refeicao(tipo)
        
        # Validate quantidade (must be non-negative)
        quantidade = data.get('quantidade')
        if quantidade is None:
            raise ValidationError('quantidade é obrigatória', 'quantidade')
        self.validate_not_negative(quantidade, 'quantidade')
        
        # Validate alimentos (must not be empty)
        alimentos = data.get('alimentos')
        self.validate_list_not_empty(alimentos, 'alimentos')
        
        # Validate dieta_id if provided
        dieta_id = data.get('dieta_id')
        if dieta_id is not None:
            self.validate_dieta_exists(dieta_id)
        
        return data
    
    def validate_tipo_refeicao(self, tipo):
        """
        Validate that meal type is valid.
        
        Args:
            tipo: Meal type to validate
            
        Raises:
            ValidationError: If meal type is invalid
        """
        if tipo.lower() not in self.TIPOS_VALIDOS_LOWER:
            raise ValidationError(
                f'Tipo de refeição inválido. Tipos válidos: {", ".join(self.TIPOS_VALIDOS)}',
                'tipo_refeicao'
            )
    
    def validate_dieta_exists(self, dieta_id):
        """
        Validate that the diet exists.
        Business rule: Cannot create meal for non-existent diet.
        
        Args:
            dieta_id: ID of the diet to validate
            
        Raises:
            ValidationError: If diet does not exist
        """
        from app.models.dieta import Dieta
        dieta = Dieta.get_by_id(dieta_id)
        if not dieta:
            raise ValidationError(
                f'Dieta com ID {dieta_id} não existe',
                'dieta_id'
            )
        return dieta


class ExercicioValidator(BaseValidator):
    """
    Validator for Exercicio (Exercise) model.
    Inherits from BaseValidator.
    """
    
    def __init__(self):
        """Constructor for ExercicioValidator."""
        super().__init__()
    
    def validate(self, data):
        """
        Validate exercise data.
        
        Args:
            data: Dictionary with exercise data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate tipo_exercicio
        self.validate_not_empty(data.get('tipo_exercicio'), 'tipo_exercicio')
        
        # Validate quantidade_repeticoes (must be non-negative)
        repeticoes = data.get('quantidade_repeticoes')
        if repeticoes is None:
            raise ValidationError('quantidade_repeticoes é obrigatória', 'quantidade_repeticoes')
        self.validate_not_negative(repeticoes, 'quantidade_repeticoes')
        
        # Validate ciclos (must be non-negative) - Business rule
        ciclos = data.get('ciclos')
        if ciclos is None:
            raise ValidationError('ciclos é obrigatório', 'ciclos')
        self.validate_not_negative(ciclos, 'ciclos')
        
        # Validate pausa_entre_ciclos (must be non-negative)
        pausa = data.get('pausa_entre_ciclos')
        if pausa is None:
            raise ValidationError('pausa_entre_ciclos é obrigatória', 'pausa_entre_ciclos')
        self.validate_not_negative(pausa, 'pausa_entre_ciclos')
        
        # Validate dieta_id if provided
        dieta_id = data.get('dieta_id')
        if dieta_id is not None:
            self.validate_dieta_exists(dieta_id)
        
        return data
    
    def validate_dieta_exists(self, dieta_id):
        """
        Validate that the diet exists.
        Business rule: Cannot create exercise for non-existent diet.
        
        Args:
            dieta_id: ID of the diet to validate
            
        Raises:
            ValidationError: If diet does not exist
        """
        from app.models.dieta import Dieta
        dieta = Dieta.get_by_id(dieta_id)
        if not dieta:
            raise ValidationError(
                f'Dieta com ID {dieta_id} não existe',
                'dieta_id'
            )
        return dieta
