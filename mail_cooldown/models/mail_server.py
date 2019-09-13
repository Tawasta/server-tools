# -*- coding: utf-8 -*-
from odoo import api, models, tools, fields, _
from odoo.addons.base.ir.ir_mail_server import extract_rfc2822_addresses
import datetime


class MailServer(models.Model):
    _inherit = 'ir.mail_server'

    @api.model
    def send_email(self, message, **kwargs):
        """
        Override send mail to force a cooldown for sending
        """

        email_to = message['To']
        email_cc = message['Cc']
        email_bcc = message['Bcc']
        smtp_to_list = filter(None, tools.flatten(
            map(extract_rfc2822_addresses, [email_to, email_cc, email_bcc])))

        res_partner = self.env['res.partner']
        mail_message = self.env['mail.message']

        # TODO: configurable timeframe
        timeframe = datetime.datetime.now() - datetime.timedelta(minutes=15)
        timeframe_str = fields.Datetime.to_string(timeframe)

        # TODO: configurable limit
        limit = 3

        for email in smtp_to_list:
            for partner in res_partner.search([('email', '=', email)]):
                domain = [
                    ('partner_ids', '=', partner.id),
                    ('date', '>', timeframe_str)
                ]
                message_ids = mail_message.search(domain)

                assert len(message_ids) <= limit, _(
                    'One of the mail recipients has been sent too many mails. '
                    'Wait for a while before sending another')

        super(MailServer, self).send_email(message, **kwargs)