# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Partido de la Liga'


    #Atributos del modelo


    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR LOS Many2One en Vistas
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
    @api.model
    def sumar_gols_casa(self):
        for record in self.search([]):
            record.goles_casa += 2
        self.actualizoRegistrosEquipo()

    @api.model
    def sumar_gols_fuera(self):
        for record in self.search([]):
            record.goles_fuera += 2
        self.actualizoRegistrosEquipo()
   

    #Nombre del equipo que juega en casa casa
    equipo_local = fields.Many2one(
        'liga.equipo',
        string='Equip Local',
        required=True
    )
    #Goles equipo de casa
    goles_local= fields.Integer(string='Gols Local')

    #Nombre del equipo que juega fuera
    equipo_visitante = fields.Many2one(
        'liga.equipo',
        string='Equip Visitant',
        required=True
    )
    #Goles equipo de casa
    goles_visitante= fields.Integer(string='Gols Visitant')

    fecha = fields.Datetime(string='Data del Partit', required=True)
    ubicacion = fields.Char(string='Ubicació')
    
    #Constraints de atributos
    @api.constrains('equipo_local')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_local:
                raise models.ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_local == record.equipo_visitante:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')


     #Constraints de atributos
    @api.constrains('equipo_visitante')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_visitante:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_visitante and record.equipo_local == record.equipo_visitante:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')




    
    '''
    Funcion para actualizar la clasificacion de los equipos, re-calculandola entera
    '''
    def actualizoRegistrosEquipo(self):
        for recordEquipo in self.env['liga.equipo'].search([]):
            recordEquipo.victorias = 0
            recordEquipo.empates = 0
            recordEquipo.derrotas = 0
            recordEquipo.goles_a_favor = 0
            recordEquipo.goles_en_contra = 0
            recordEquipo.puntos = 0

            for recordPartido in self.env['liga.partido'].search([]):
                if recordPartido.equipo_local.nombre == recordEquipo.nombre:
                    if recordPartido.goles_local > recordPartido.goles_visitante:
                        recordEquipo.victorias += 1
                        if (recordPartido.goles_local - recordPartido.goles_visitante) >= 4:
                            recordEquipo.puntos += 4
                        else:
                            recordEquipo.puntos += 3
                    elif recordPartido.goles_local < recordPartido.goles_visitante:
                        recordEquipo.derrotas += 1
                        if (recordPartido.goles_visitante - recordPartido.goles_local) >= 4:
                            recordEquipo.puntos -= 1
                    else:
                        recordEquipo.empates += 1
                    recordEquipo.goles_a_favor += recordPartido.goles_local
                    recordEquipo.goles_en_contra += recordPartido.goles_visitante

                if recordPartido.equipo_visitante.nombre == recordEquipo.nombre:
                    if recordPartido.goles_local < recordPartido.goles_visitante:
                        recordEquipo.victorias += 1
                    elif recordPartido.goles_local > recordPartido.goles_visitante:
                        recordEquipo.derrotas += 1
                    else:
                        recordEquipo.empates += 1
                    recordEquipo.goles_a_favor += recordPartido.goles_visitante
                    recordEquipo.goles_en_contra += recordPartido.goles_local



    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_local', 'goles_local', 'equipo_visitante', 'goles_visitante')
    def actualizar(self):
        self.actualizoRegistrosEquipo()
    

    #Sobrescribo el borrado (unlink)
    def unlink(self):
        #Borro el registro, que es lo que hace el metodo normalmente
        result=super(LigaPartido,self).unlink()
        #Añado que llame a actualizoRegistroEquipo()
        self.actualizoRegistrosEquipo()
        return result

    #Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        #hago lo normal del metodo create
        result = super().create(values)
        #Añado esto: llamo a la funcion que actualiza la clasificacion
        self.actualizoRegistrosEquipo()
        #hago lo normal del metodo create
        return result
