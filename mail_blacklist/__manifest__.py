##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2016 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

{
    'name': 'Mail Blacklist',
    'summary': 'Filter incoming and outgoing mail by address or domain',
    'version': '12.0.0.3.3',
    'category': 'Tools',
    'website': 'https://github.com/Tawasta/server-tools',
    'author': 'Tawasta',
    'license': 'AGPL-3',
    'application': False,
    'installable': False,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'mail',
    ],
    'data': [
        'views/mail_blacklist_menu.xml',
    ],
    'demo': [
    ],
}
