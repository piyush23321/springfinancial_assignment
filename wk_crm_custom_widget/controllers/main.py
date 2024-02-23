# Odoo module===================================================
from odoo import http
from odoo.http import request
import json

class PartnerCreate(http.Controller):

    def fetch_record(self, model, vals):
        return vals and int(request.env[model].search(['|',('name','=ilike',vals), ('code','=ilike',vals)], limit=1)) or False
    
    @http.route('/create/partner', type='json', auth="public" , methods=['POST'], website=False)
    def create_partner(self, *kwargs):
        Partner = request.env['res.partner']
        data = json.loads(request.httprequest.data.decode('utf-8'))
        try:
            country = data.get('country_id', False)
            state = data.get('state_id', False)
            data.update({'country_id':self.fetch_record('res.country',country), 'state_id':self.fetch_record('res.country.state',state)})
            partner = Partner.sudo().create(data)
            status = "Success"
            msg="%r %r"%(partner.complete_name, partner.id)

        except Exception as e:
            msg=f'Error while creating Partner: ----{str(e)}'
            status = "Failed"

        finally:
            return {'Response':status ,'description':msg}