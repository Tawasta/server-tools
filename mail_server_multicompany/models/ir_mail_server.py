from odoo import api
from odoo import fields
from odoo import models

import logging
_logger = logging.getLogger(__name__)


class IrMailserver(models.Model):
    _inherit = 'ir.mail_server'

    company_id = fields.Many2one(
        'res.company',
        'Company',
    )

    @api.model
    def send_email(self, message, mail_server_id=None, *args, **kwargs):

        print(self)
        print(message)
        print(mail_server_id)
        print(mail_server_id)

        if not mail_server_id:
            # Use mail message id meta information for getting the sending company
            # TODO: could this be done with more reliable way?
            references = message['Message-Id']

            '''
            # Remove the hostname part
            try:
                references = references.split("@")[0]
            except Exception, e:
                _logger.warning(e)

            try:
                # Split the parts to a list. The list should look like this:
                # ['<1490169823.917293071746826.735164174278517', 'openerp', '1234', 'crm.claim']
                # [{id-numbers that we don't use here}, {static 'openerp'}, {model instance id}, {model}]
                references_list = references.split("-")

                model_instance_id = references_list[2]
                model_name = references_list[3]

            except Exception, e:
                _logger.warning(e)

                model_instance_id = False
                model_name = False

            if model_name and model_instance_id:
                # Try to find the model instance
                try:
                    model = self.env[model_name]
                    model_instance = model.browse([int(model_instance_id)])

                    # Try different field names
                    if hasattr(model_instance, 'company_id'):
                        company_id = company = getattr(model_instance, 'company_id').id
                    elif hasattr(model_instance, 'company'):
                        company_id = getattr(model_instance, 'company').id
                    else:
                        company_id = False

                except Exception, e:
                    _logger.warning(e)
                    company_id = False

                # Get a company-spesifitc mail server if one exists
                mail_server = self.env['ir.mail_server'].search([
                    ('company', '=', company_id)
                ], limit=1, order='sequence DESC')

                if mail_server:
                    mail_server_id = mail_server.id
                '''

        return super(IrMailserver, self).send_email(
            message, mail_server_id, *args, **kwargs)
