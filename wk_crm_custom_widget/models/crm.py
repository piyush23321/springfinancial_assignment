from odoo import models , fields , api 

OPTIONS = [('technology', 'Technology'), ('business', 'Business')]

class CRM(models.Model):
    _inherit = 'crm.lead'

    technology_name  = fields.Char(string='Technology')
    business_name  = fields.Char(string='Business')

    opportunity_type = fields.Selection(OPTIONS,
        string='Opportunity Type',
        default='technology',
    )

    is_completed = fields.Boolean(
        string='Complete' ,default=False,
        help='Lead is ready to convert opportunity'
        )

    stage_id = fields.Many2one(comodel='lead.stage', string='Stage', compute = '_compute_stage', index=True, tracking=True, readonly=False, store=True, ondelete='restrict')

    @property
    def lead_stage_complete(self):
        return self.env['lead.stage'].search([('name','=','Complete')],limit=1)

    
    @api.depends('stage_id')
    def _compute_stage(self):
        is_completed = self.lead_stage_complete
        if is_completed:
            self.write({'lead_stage_id': is_completed.id}) 

    # Overrides this core's function in order to create two opportunity with two types
    def convert_opportunity(self, partner, user_ids=False, team_id=False):
        # check if lad is not complete terminate the process.
        if not self.complete:
            return False
        customer = partner if partner else self.env['res.partner']
        for lead in self:
            if not lead.active or lead.probability == 100:
                continue
            vals = lead._convert_opportunity_data(customer, team_id)
            # added
            vals['opportunity_type'] = 'business'
            # end
            lead.write(vals)
            # ********Duplicate lead with diffrent opportunity_type*******
            try:
                d_lead=lead.copy()
                vals['opportunity_type'] = 'technology'
                d_lead.write(vals)
            except Exception as e:
                _logger.debug(f'***Error While Duplicatig lead*****{str(e)}')
            # *****END********
        if user_ids or team_id:
            self._handle_salesmen_assignment(user_ids=user_ids, team_id=team_id)

        return True
    
    def action_set_lead_complete(self):
        search_complete = self.env['crm.lead.stage'].search([('name','=','Complete')],limit=1)
        _logger.info(f'search_complete \n\n  {[search_complete,self.lead_stage_id.name]}')
        if search_complete:
            self.lead_stage_id = search_complete.id
            self.complete = True

    

    @api.onchange('lead_stage_id')
    def onchange_lead_stage_id(self):
        _logger.info(f'=============lead_stage_id in onchange*****======= \n\n  {[self.lead_stage_id.name]}')
        if self.lead_stage_id.name == 'Complete':
            self.complete = True
        else:
            self.complete = False