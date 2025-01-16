# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web
class Main(http.Controller):
    # Decorador que indica que la url "/eliminarempates" atenderá por HTTP, sin autenticación
    # Devolverá texto que estará en formato JSON
    # Se puede probar accediendo a http://localhost:8069/eliminarempates
    @http.route('/eliminarempates', type='http', auth='none')
    def obtenerNumeroPartidosEmpatadosJSON(self):
        # Obtenemos la referencia al modelo de Partido
        partidos = request.env['liga.partido'].sudo().search([('goles_local', '=', 'goles_visitante')])
        
        # Contamos el número de partidos empatados
        numero_empates = len(partidos)

        partidos.unlink()
        
        # Convertimos el número a JSON
        json_result = json.dumps({'numero_empates': numero_empates})

        return json_result
