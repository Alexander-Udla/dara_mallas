from odoo import fields, models

class college(models.Model):
    _name="dara_mallas.college"
    
    name=fields.Char("Facultad")
    code=fields.Char("Codigo")
    dean_id = fields.Many2one("dara_mallas.dean") 