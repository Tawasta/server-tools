##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:
from odoo.addons.auditlog.models.rule import DictDiffer

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class AuditlogRule(models.Model):

    # 1. Private attributes
    _inherit = "auditlog.rule"

    # 2. Fields declaration
    read_trigger_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        relation="auditlog_rule_read_fields_rel",
        string="Read trigger fields",
        domain="[('model_id', '=', model_id)]",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def create_logs(self, uid, res_model, res_ids, method,
                    old_values=None, new_values=None,
                    additional_log_values=None):
        """
        Overwrite audit log creation to prevent
        unnecessary read logs.
        """
        EMPTY_DICT = {}

        if old_values is None:
            old_values = EMPTY_DICT
        if new_values is None:
            new_values = EMPTY_DICT
        log_model = self.env['auditlog.log']
        http_request_model = self.env['auditlog.http.request']
        http_session_model = self.env['auditlog.http.session']

        # Check trigger fields from log rule and get fields' names
        trigger_fields = []
        log_rule = self.sudo().search([
            ("model_id", "=", res_model),
        ], limit=1)
        if log_rule and log_rule.read_trigger_field_ids:
            trigger_fields = log_rule.read_trigger_field_ids.mapped('name')

        for res_id in res_ids:
            # Don't create the log lines if method is read
            # and doesn't contain trigger fields
            field_list = list(old_values.get(res_id, EMPTY_DICT).keys())
            trigger_exists = any(elem in trigger_fields for elem in field_list)
            if method is 'read' and trigger_fields and not trigger_exists:
                continue

            model_model = self.env[res_model]
            name = model_model.browse(res_id).name_get()
            res_name = name and name[0] and name[0][1]
            vals = {
                'name': res_name,
                'model_id': self.pool._auditlog_model_cache[res_model],
                'res_id': res_id,
                'method': method,
                'user_id': uid,
                'http_request_id': http_request_model.current_http_request(),
                'http_session_id': http_session_model.current_http_session(),
            }
            vals.update(additional_log_values or {})
            log = log_model.create(vals)
            diff = DictDiffer(
                new_values.get(res_id, EMPTY_DICT),
                old_values.get(res_id, EMPTY_DICT))
            if method is 'create':
                self._create_log_line_on_create(log, diff.added(), new_values)
            elif method is 'read':
                self._create_log_line_on_read(
                    log,
                    list(old_values.get(res_id, EMPTY_DICT).keys()), old_values
                )
            elif method is 'write':
                self._create_log_line_on_write(
                    log, diff.changed(), old_values, new_values)

    # 8. Business methods
