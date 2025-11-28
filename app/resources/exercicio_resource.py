"""
Exercicio Resource Module
Contains Flask-RESTful resources for exercise API endpoints.
"""

from flask import request
from flask_restful import Resource
from app.controllers.exercicio_controller import ExercicioController


class ExercicioListResource(Resource):
    """
    Resource for exercise collection endpoints.
    
    Endpoints:
        - GET /api/exercicios - List all exercises
        - POST /api/exercicios - Create a new exercise
    """
    
    def __init__(self):
        """Constructor for ExercicioListResource."""
        self._controller = ExercicioController()
    
    def get(self):
        """
        List all exercises.
        
        Query params:
            - dieta_id: Filter by diet ID (optional)
        
        Returns:
            tuple: (list of exercises, HTTP status code)
        """
        dieta_id = request.args.get('dieta_id', type=int)
        
        if dieta_id:
            exercicios = self._controller.get_by_dieta(dieta_id)
        else:
            exercicios = self._controller.get_all()
        
        return {'data': exercicios, 'count': len(exercicios)}, 200
    
    def post(self):
        """
        Create a new exercise.
        
        Request body:
            {
                "tipo_exercicio": "string (required)",
                "quantidade_repeticoes": "integer (required)",
                "ciclos": "integer (required, non-negative)",
                "pausa_entre_ciclos": "integer (required)",
                "dieta_id": "integer (optional)"
            }
            
        Returns:
            tuple: (created exercise or error, HTTP status code)
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        exercicio, error = self._controller.create(data)
        
        if error:
            return {'error': error}, 400
        
        return {'data': exercicio.to_dict(), 'message': 'Exercício criado com sucesso'}, 201


class ExercicioResource(Resource):
    """
    Resource for single exercise endpoints.
    
    Endpoints:
        - GET /api/exercicios/<id> - Get a specific exercise
        - PUT /api/exercicios/<id> - Update an exercise
        - DELETE /api/exercicios/<id> - Delete an exercise
    """
    
    def __init__(self):
        """Constructor for ExercicioResource."""
        self._controller = ExercicioController()
    
    def get(self, id):
        exercicio, error = self._controller.get_by_id(id)
        
        if error:
            return {'error': error}, 404
        
        return {'data': exercicio}, 200
    
    def put(self, id):
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        exercicio, error = self._controller.update(id, data)
        
        if error:
            if 'não encontrado' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'data': exercicio, 'message': 'Exercício atualizado com sucesso'}, 200
    
    def delete(self, id):
        success, error = self._controller.delete(id)
        
        if not success:
            if 'não encontrado' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'message': 'Exercício excluído com sucesso'}, 200
