"""
Dieta Resource Module
Contains Flask-RESTful resources for diet API endpoints.
"""

from flask import request
from flask_restful import Resource
from app.controllers.dieta_controller import DietaController


class DietaListResource(Resource):
    def __init__(self):
        """Constructor for DietaListResource."""
        self._controller = DietaController()
    
    def get(self):
        dietas = self._controller.get_all()
        return {'data': dietas, 'count': len(dietas)}, 200
    
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        dieta, error = self._controller.create(data)
        
        if error:
            return {'error': error}, 400
        
        return {'data': dieta.to_dict(), 'message': 'Dieta criada com sucesso'}, 201


class DietaResource(Resource):    
    def __init__(self):
        """Constructor for DietaResource."""
        self._controller = DietaController()
    
    def get(self, id):
        dieta, error = self._controller.get_by_id(id)
        
        if error:
            return {'error': error}, 404
        
        return {'data': dieta}, 200
    
    def put(self, id):
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        dieta, error = self._controller.update(id, data)
        
        if error:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'data': dieta, 'message': 'Dieta atualizada com sucesso'}, 200
    
    def delete(self, id):
        success, error = self._controller.delete(id)
        
        if not success:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'message': 'Dieta excluída com sucesso'}, 200
