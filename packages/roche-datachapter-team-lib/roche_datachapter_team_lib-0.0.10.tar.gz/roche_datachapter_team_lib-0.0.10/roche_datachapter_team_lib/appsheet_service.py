"""Clase para peticiones de appsheet con metodos para obtener, editar y crear registros en la base de datos de appshet"""
import urllib3
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from .google_services import GoogleServices

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AppsheetService:
    """Servicio para invocar API de Appsheet"""

    def __init__(self, application_id: str, application_access_key: str):
        self.application_id = application_id
        self.application_access_key = application_access_key

    def get_table_data(self, table_name: str, rows: list = None):
        """Obtiene los datos de una tabla de appsheet de una aplicación"""
        if rows is None:
            rows = []

        url = f"https://api.appsheet.com/api/v2/apps/{self.application_id}/tables/{table_name}/Action"
        headers = {
            "Content-Type": "application/json",
            "muteHttpExceptions": "true"
        }
        json_body = {
            "Action": "Find",
            "Properties": {
                "Locale": "en-US",
                "Timezone": "Pacific Standard Time"
            },
            "Rows": rows
        }
        params = {
            'applicationAccessKey': self.application_access_key
        }

        def make_request_get_data():
            """Función encapsulada para reintentar la petición en caso de error"""
            response = requests.post(
                url, headers=headers, params=params, json=json_body, verify=False, timeout=10
            )
            response.raise_for_status()
            return response

        try:
            response = GoogleServices.retry_request(make_request_get_data)
            if response.headers.get('Content-Type') == 'application/json':
                return response.json()
            raise ValueError("La respuesta no es de tipo JSON o esta vacia")
        except HTTPError as http_err:
            raise TimeoutError(f"HTTP error occurred: {http_err}") from http_err
        except Timeout as timeout_err:
            raise TimeoutError(f"Request timed out: {timeout_err}") from timeout_err
        except RequestException as req_err:
            raise TimeoutError(f"Request error: {req_err}") from req_err
        except ValueError as value_err:
            print(f"Error al procesar la respuesta: {value_err}")
            return None
        except Exception as error:
            raise TimeoutError(f"Error al obtener los datos de la tabla: {error}") from error

    def add_registers_to_table(self, rows_list: list, table_name: str):
        """Agrega registros a una tabla de appsheet de una aplicación"""
        if rows_list is None or rows_list == []:
            raise ValueError("La lista de registros no puede ser nula o vacía")
        url = f"https://api.appsheet.com/api/v2/apps/{self.application_id}/tables/{table_name}/Action"
        headers = {
            "Content-Type": "application/json",
            "muteHttpExceptions": "true"
        }
        json_body = {
            "Action": "Add",
            "Properties": {
                "Locale": "en-US",
                "Timezone": "Pacific Standard Time"
            },
            "Rows": rows_list
        }
        params = {
            'applicationAccessKey': self.application_access_key
        }

        def make_request_add_data():
            """Función encapsulada para reintentar la petición en caso de error"""
            response = requests.post(
                url, headers=headers, params=params, json=json_body, verify=False, timeout=10
            )
            response.raise_for_status()
            return response

        try:
            response = GoogleServices.retry_request(make_request_add_data)
            if response.headers.get('Content-Type') == 'application/json':
                return response.json()
            raise ValueError("La respuesta no es de tipo JSON o esta vacia")
        except HTTPError as http_err:
            raise TimeoutError(f"HTTP error occurred: {http_err}") from http_err
        except Timeout as timeout_err:
            raise TimeoutError(f"Request timed out: {timeout_err}") from timeout_err
        except RequestException as req_err:
            raise TimeoutError(f"Request error: {req_err}") from req_err
        except ValueError as value_err:
            print(f"Error al procesar la respuesta: {value_err}")
            return None
        except Exception as error:
            raise TimeoutError(f"Error al agregar registros a la tabla: {error}") from error

    def perform_action(self, table_name: str, action: str, rows: list = None):
        """Realiza una acción en una tabla de appsheet de una aplicación"""
        if rows is None:
            rows = []

        url = f"https://api.appsheet.com/api/v2/apps/{self.application_id}/tables/{table_name}/Action"
        headers = {
            "Content-Type": "application/json",
            "muteHttpExceptions": "true"
        }
        json_body = {
            "Action": action,
            "Properties": {
                "Locale": "en-US",
                "Timezone": "Pacific Standard Time"
            },
            "Rows": rows
        }
        params = {
            'applicationAccessKey': self.application_access_key
        }

        def make_request_perform_action():
            """Función encapsulada para reintentar la petición en caso de error"""
            response = requests.post(
                url, headers=headers, params=params, json=json_body, verify=False, timeout=10
            )
            response.raise_for_status()
            return response

        try:
            response = GoogleServices.retry_request(make_request_perform_action)
            if response.headers.get('Content-Type') == 'application/json':
                return response.json()
            raise ValueError("La respuesta no es de tipo JSON o esta vacia")
        except HTTPError as http_err:
            raise TimeoutError(f"HTTP error occurred: {http_err}") from http_err
        except Timeout as timeout_err:
            raise TimeoutError(f"Request timed out: {timeout_err}") from timeout_err
        except RequestException as req_err:
            raise TimeoutError(f"Request error: {req_err}") from req_err
        except ValueError as value_err:
            print(f"Error al procesar la respuesta: {value_err}")
            return None
        except Exception as error:
            raise TimeoutError(f"Error al realizar la acción: {error}") from error
