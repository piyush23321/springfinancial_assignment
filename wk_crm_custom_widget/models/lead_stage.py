from odoo import models , fields


class Stage(models.Model):
    _name = 'lead.stage'
    _description = 'Managing stages for lead convert to opportunity'


    name = fields.Char(string='Stage', help="Lead stage name", required="True")
    sequence_id = fields.Integer('Sequence', default=1, help="Order stage Sequence")
