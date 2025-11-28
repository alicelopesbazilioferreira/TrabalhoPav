from flask import request
from flask_restful import Resource
from app.controllers.refeicao_controller import RefeicaoController
class RefeicaoListResource(Resource):
    def __init__(self):
        """Constructor for RefeicaoListResource."""
        self._controller = RefeicaoController()
    
    def get(self):
        dieta_id = request.args.get('dieta_id', type=int)
        
        if dieta_id:
            refeicoes = self._controller.get_by_dieta(dieta_id)
        else:
            refeicoes = self._controller.get_all()
        
        return {'data': refeicoes, 'count': len(refeicoes)}, 200
    
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        refeicao, error = self._controller.create(data)
        
        if error:
            return {'error': error}, 400
        
        return {'data': refeicao.to_dict(), 'message': 'Refeição criada com sucesso'}, 201


class RefeicaoResource(Resource):    
    def __init__(self):
        """Constructor for RefeicaoResource."""
        self._controller = RefeicaoController()
    
    def get(self, id):
        refeicao, error = self._controller.get_by_id(id)
        
        if error:
            return {'error': error}, 404
        
        return {'data': refeicao}, 200
    
    def put(self, id):
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        refeicao, error = self._controller.update(id, data)
        
        if error:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'data': refeicao, 'message': 'Refeição atualizada com sucesso'}, 200
    
    def delete(self, id):
        success, error = self._controller.delete(id)
        
        if not success:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'message': 'Refeição excluída com sucesso'}, 200
