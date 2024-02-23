# Odoo module===================================================
from odoo import models , fields , api 

OPTIONS = [('technology', 'Technology'), ('business', 'Business')]

class Lead(models.Model):
    _inherit = 'crm.lead'

    # Fields
    technology_name  = fields.Char(string='Technology')
    business_name  = fields.Char(string='Business')
    custom_stage_id = fields.Many2one(comodel_name='lead.stage', string='Custom Stage', index=True, tracking=True, readonly=False, store=True, ondelete='restrict')

    opportunity_type = fields.Selection(OPTIONS,
        string='Opportunity Type',
        default='technology',
    )

    is_completed = fields.Boolean(
        string='Complete' ,default=False,
        help='Lead is ready to convert opportunity'
        )


    @property
    def lead_stage_complete(self):
        return self.env['lead.stage'].search([('name','=','Complete')],limit=1)
    

    #----------------------------------------------------------
    # Action Method
    #---------------------------------------------------------- 
    def action_mark_to_complete(self):
        """
        Mark the lead as complete if its stage indicates completion.

        If the lead's 'lead_stage_complete' field indicates completion,
        update the 'custom_stage_id' field with the corresponding stage ID
        and set the 'is_completed' field to True.

        :return: None
        """
        is_completed = self.lead_stage_complete
        if is_completed:
            self.write({'custom_stage_id': is_completed.id,'is_completed':True})

    #----------------------------------------------------------
    # Onchange Method
    #---------------------------------------------------------- 
    @api.onchange('custom_stage_id')
    def onchange_lead_stage_id(self):
        """
        Update the 'is_completed' field based on the selected custom stage.

        If the selected custom stage is named 'Complete', set the 'is_completed'
        field to True; otherwise, set it to False.

        :return: None
        """
        self.is_completed = True if self.custom_stage_id.name == 'Complete' else False


    
    #----------------------------------------------------------
    # Override
    #----------------------------------------------------------        
    def convert_opportunity(self, partner, user_ids=False, team_id=False):
        if not self.is_completed:
            return False
        customer = partner or self.env['res.partner']
        for lead in self:
            if not lead.active or lead.probability == 100:
                continue
            vals = lead._convert_opportunity_data(customer, team_id)
            for opportunity_type, _ in OPTIONS:
                if opportunity_type == 'technology':
                    vals.update({'opportunity_type':opportunity_type})
                    lead.copy(vals)
                else:
                    vals.update({'opportunity_type':opportunity_type})
                    lead.write(vals)
        if user_ids or team_id:
            self._handle_salesmen_assignment(user_ids=user_ids, team_id=team_id)

        return True
    
    
    