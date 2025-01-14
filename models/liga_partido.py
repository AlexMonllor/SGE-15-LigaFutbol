# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Un partido de la liga'


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
    equipo_casa = fields.Many2one(
        'liga.equipo',
        string='Equipo local',
    )
    #Goles equipo de casa
    goles_casa= fields.Integer()

    #Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga.equipo',
        string='Equipo visitante',
    )
    #Goles equipo de casa
    goles_fuera= fields.Integer()
    
    #Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise models.ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')


     #Constraints de atributos
    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_fuera and record.equipo_casa == record.equipo_fuera:
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
                if recordPartido.equipo_casa.nombre == recordEquipo.nombre:
                    if recordPartido.goles_casa > recordPartido.goles_fuera:
                        recordEquipo.victorias += 1
                        if (recordPartido.goles_casa - recordPartido.goles_fuera) >= 4:
                            recordEquipo.puntos += 4
                        else:
                            recordEquipo.puntos += 3
                    elif recordPartido.goles_casa < recordPartido.goles_fuera:
                        recordEquipo.derrotas += 1
                        if (recordPartido.goles_fuera - recordPartido.goles_casa) >= 4:
                            recordEquipo.puntos -= 1
                    else:
                        recordEquipo.empates += 1
                    recordEquipo.goles_a_favor += recordPartido.goles_casa
                    recordEquipo.goles_en_contra += recordPartido.goles_fuera

                if recordPartido.equipo_fuera.nombre == recordEquipo.nombre:
                    if recordPartido.goles_casa < recordPartido.goles_fuera:
                        recordEquipo.victorias += 1
                    elif recordPartido.goles_casa > recordPartido.goles_fuera:
                        recordEquipo.derrotas += 1
                    else:
                        recordEquipo.empates += 1
                    recordEquipo.goles_a_favor += recordPartido.goles_fuera
                    recordEquipo.goles_en_contra += recordPartido.goles_casa



    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
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
