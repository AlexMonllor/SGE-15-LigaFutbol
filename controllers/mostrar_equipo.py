from odoo import http
from odoo.http import request

class MostrarEquipo(http.Controller):
    @http.route('/visualitzaequip', auth='none', type='http', website=True)
    def get_team(self, name):
        equipos = request.env['liga.equipo'].sudo().search([('nombre', '=', name)])
        return request.render('liga_futbol.kanban_box', {
            'equipos': equipos,
        })
