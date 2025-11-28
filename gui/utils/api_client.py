"""
API Client Module
Contains the client class for communicating with the REST API.
"""

import requests
from typing import Optional, Dict, Any, Tuple


class ApiClient:
    """
    API Client for communicating with the Diet Management REST API.
    
    Provides methods for GET, POST, PUT, DELETE operations.
    Handles errors and exceptions.
    
    Demonstrates:
        - Encapsulation of HTTP operations
        - Error handling
        - Use of dictionaries and conditions
    """
    
    def __init__(self, base_url: str = 'http://localhost:5000/api'):
        """
        Constructor for ApiClient.
        
        Args:
            base_url: Base URL of the API (default: http://localhost:5000/api)
        """
        self._base_url = base_url
        self._timeout = 10  # Request timeout in seconds
    
    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_url
    
    @base_url.setter
    def base_url(self, value: str):
        """Set the base URL."""
        self._base_url = value
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data (for POST/PUT)
            params: Query parameters (for GET)
            
        Returns:
            tuple: (response data or None, error message or None)
        """
        url = f'{self._base_url}/{endpoint}'
        
        try:
            response = None
            
            # Use conditions to determine request method
            if method == 'GET':
                response = requests.get(url, params=params, timeout=self._timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=self._timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=self._timeout)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=self._timeout)
            else:
                return None, f'Método HTTP inválido: {method}'
            
            # Process response
            if response.status_code >= 200 and response.status_code < 300:
                try:
                    return response.json(), None
                except ValueError:
                    return {'status': 'success'}, None
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Erro desconhecido')
                except ValueError:
                    error_msg = f'Erro HTTP {response.status_code}'
                return None, error_msg
                
        except requests.ConnectionError:
            return None, 'Erro de conexão: API não disponível'
        except requests.Timeout:
            return None, 'Tempo limite de requisição excedido'
        except requests.RequestException as e:
            return None, f'Erro na requisição: {str(e)}'
        except ValueError:
            return None, 'Erro ao processar resposta da API'
    
    # ==================== DIETA METHODS ====================
    
    def get_dietas(self) -> Tuple[Optional[list], Optional[str]]:
        """
        Get all diets.
        
        Returns:
            tuple: (list of diets or None, error message or None)
        """
        result, error = self._make_request('GET', 'dietas')
        if error:
            return None, error
        return result.get('data', []), None
    
    def get_dieta(self, id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get a specific diet by ID.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (diet data or None, error message or None)
        """
        result, error = self._make_request('GET', f'dietas/{id}')
        if error:
            return None, error
        return result.get('data'), None
    
    def create_dieta(self, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Create a new diet.
        
        Args:
            data: Diet data dictionary
            
        Returns:
            tuple: (created diet or None, error message or None)
        """
        result, error = self._make_request('POST', 'dietas', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def update_dieta(self, id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Update a diet.
        
        Args:
            id: Diet ID
            data: Updated diet data
            
        Returns:
            tuple: (updated diet or None, error message or None)
        """
        result, error = self._make_request('PUT', f'dietas/{id}', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def delete_dieta(self, id: int) -> Tuple[bool, Optional[str]]:
        """
        Delete a diet.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        result, error = self._make_request('DELETE', f'dietas/{id}')
        if error:
            return False, error
        return True, None
    
    # ==================== REFEICAO METHODS ====================
    
    def get_refeicoes(self, dieta_id: Optional[int] = None) -> Tuple[Optional[list], Optional[str]]:
        """
        Get all meals, optionally filtered by diet ID.
        
        Args:
            dieta_id: Optional diet ID to filter by
            
        Returns:
            tuple: (list of meals or None, error message or None)
        """
        params = {'dieta_id': dieta_id} if dieta_id else None
        result, error = self._make_request('GET', 'refeicoes', params=params)
        if error:
            return None, error
        return result.get('data', []), None
    
    def get_refeicao(self, id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get a specific meal by ID.
        
        Args:
            id: Meal ID
            
        Returns:
            tuple: (meal data or None, error message or None)
        """
        result, error = self._make_request('GET', f'refeicoes/{id}')
        if error:
            return None, error
        return result.get('data'), None
    
    def create_refeicao(self, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Create a new meal.
        
        Args:
            data: Meal data dictionary
            
        Returns:
            tuple: (created meal or None, error message or None)
        """
        result, error = self._make_request('POST', 'refeicoes', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def update_refeicao(self, id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Update a meal.
        
        Args:
            id: Meal ID
            data: Updated meal data
            
        Returns:
            tuple: (updated meal or None, error message or None)
        """
        result, error = self._make_request('PUT', f'refeicoes/{id}', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def delete_refeicao(self, id: int) -> Tuple[bool, Optional[str]]:
        """
        Delete a meal.
        
        Args:
            id: Meal ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        result, error = self._make_request('DELETE', f'refeicoes/{id}')
        if error:
            return False, error
        return True, None
    
    # ==================== EXERCICIO METHODS ====================
    
    def get_exercicios(self, dieta_id: Optional[int] = None) -> Tuple[Optional[list], Optional[str]]:
        """
        Get all exercises, optionally filtered by diet ID.
        
        Args:
            dieta_id: Optional diet ID to filter by
            
        Returns:
            tuple: (list of exercises or None, error message or None)
        """
        params = {'dieta_id': dieta_id} if dieta_id else None
        result, error = self._make_request('GET', 'exercicios', params=params)
        if error:
            return None, error
        return result.get('data', []), None
    
    def get_exercicio(self, id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get a specific exercise by ID.
        
        Args:
            id: Exercise ID
            
        Returns:
            tuple: (exercise data or None, error message or None)
        """
        result, error = self._make_request('GET', f'exercicios/{id}')
        if error:
            return None, error
        return result.get('data'), None
    
    def create_exercicio(self, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Create a new exercise.
        
        Args:
            data: Exercise data dictionary
            
        Returns:
            tuple: (created exercise or None, error message or None)
        """
        result, error = self._make_request('POST', 'exercicios', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def update_exercicio(self, id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Update an exercise.
        
        Args:
            id: Exercise ID
            data: Updated exercise data
            
        Returns:
            tuple: (updated exercise or None, error message or None)
        """
        result, error = self._make_request('PUT', f'exercicios/{id}', data=data)
        if error:
            return None, error
        return result.get('data'), None
    
    def delete_exercicio(self, id: int) -> Tuple[bool, Optional[str]]:
        """
        Delete an exercise.
        
        Args:
            id: Exercise ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        result, error = self._make_request('DELETE', f'exercicios/{id}')
        if error:
            return False, error
        return True, None
    
    def check_connection(self) -> Tuple[bool, Optional[str]]:
        """
        Check if the API is available.
        
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            response = requests.get(f'{self._base_url}/dietas', timeout=5)
            return response.status_code == 200, None
        except requests.ConnectionError:
            return False, 'API não disponível'
        except Exception as e:
            return False, str(e)
