from odoo import http
from odoo.http import request
import json
import logging
import ast
_logger = logging.getLogger(__name__)

# Make Sure You Have single db in Odoo

class PartnerCreate(http.Controller):
    @http.route(['/api/create_partner'],type='json', auth="public" ,methods=['POST'], csrf=False)
    def create_partner(self , **kwargs):
        """
        API end point to create the partners with the data.
        """
        partner_id , status = False , True
        country_name , state_code ,c_id, s_id = "","",False, False
        data = json.loads(request.httprequest.data.decode('utf-8'))
        if 'country' in data:
            country_name = data.pop('country','') or ''
        if 'state' in data:
            state_code = data.pop('state','') or ''
        c_id , s_id = self.get_country_state_id(country_name,state_code)
        data.update({'country_id':c_id,"state_id":s_id})
        # _logger.debug(f'kwargs into create partner=========\n\n\n {data}\n\n')
        try:
            partner = request.env['res.partner'].sudo().create(data)
            if partner:
                partner_id = partner.id
        except Exception as e:
            error_message=f'While creating partner there is an error:-{str(e)}'
            status = False
        _logger.debug(f'****partner Created****=========\n\n\n {partner_id}\n\n')
        if not status:
            return {'success':False ,'partner_id':partner_id, 'error_message':error_message}
        return {'success':True ,'partner_id':partner_id}
    
    def get_country_state_id(self, country_name,state_code):
        """
        To get the country id and state id on the basis of country name and state code.
        @return country and state id 
        """
        country_id, state_id = False, False
        if country_name:
            search_country = request.env['res.country'].search([('name','=ilike',country_name)])
            if search_country:
                country_id =search_country.id
                search_state = request.env['res.country.state'].search([('country_id','=',country_id),('code','=',state_code)])
                if search_state:
                    state_id = search_state.id
        return country_id, state_id