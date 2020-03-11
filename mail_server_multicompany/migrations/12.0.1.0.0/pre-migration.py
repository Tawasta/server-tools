def migrate(cr, version):
    # Update field name
    cr.execute(
        """
        ALTER TABLE ir_mail_server
        RENAME COLUMN company TO company_id;
        """
    )

