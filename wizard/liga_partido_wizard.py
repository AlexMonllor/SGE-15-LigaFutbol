from odoo import models, fields

class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Wizard per crear nous partits'

    equipo_local = fields.Many2one('liga.equipo', string='Equip Local', required=True)
    equipo_visitante = fields.Many2one('liga.equipo', string='Equip Visitant', required=True)
    fecha = fields.Datetime(string='Data del Partit', required=True)
    ubicacion = fields.Char(string='Ubicació')

    def add_liga_partido(self):
        partidoModel = self.env['liga.partido']
        for wiz in self:
            partidoModel.create({
                'equipo_local': wiz.equipo_local.id,
                'equipo_visitante': wiz.equipo_visitante.id,
                'fecha': wiz.fecha,
                'ubicacion': wiz.ubicacion,
            })