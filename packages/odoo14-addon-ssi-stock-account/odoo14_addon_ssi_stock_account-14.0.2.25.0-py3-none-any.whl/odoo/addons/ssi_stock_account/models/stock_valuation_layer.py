# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _name = "stock.valuation.layer"
    _inherit = [
        "stock.valuation.layer",
        "mixin.account_move",
        "mixin.account_move_double_line",
        "mixin.company_currency",
    ]
    # account.move.line
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "account_move_id"
    _accounting_date_field_name = "final_date"  # TODO
    _currency_id_field_name = "company_currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _number_field_name = False

    # Debit ML Attribute
    _debit_account_id_field_name = "debit_account_id"
    _debit_partner_id_field_name = "partner_id"
    _debit_analytic_account_id_field_name = "analytic_account_id"
    _debit_label_field_name = "description"
    _debit_product_id_field_name = "product_id"
    _debit_uom_id_field_name = "uom_id"
    _debit_quantity_field_name = "quantity"
    _debit_price_unit_field_name = "unit_cost"
    _debit_currency_id_field_name = "company_currency_id"
    _debit_company_currency_id_field_name = "company_currency_id"
    _debit_amount_currency_field_name = "value"
    _debit_company_id_field_name = "company_id"
    _debit_date_field_name = "final_date"
    _debit_need_date_due = False
    _debit_date_due_field_name = False

    # Credit ML Attribute
    _credit_account_id_field_name = "credit_account_id"
    _credit_partner_id_field_name = "partner_id"
    _credit_analytic_account_id_field_name = "analytic_account_id"
    _credit_label_field_name = "description"
    _credit_product_id_field_name = "product_id"
    _credit_uom_id_field_name = "uom_id"
    _credit_quantity_field_name = "quantity"
    _credit_price_unit_field_name = "unit_cost"
    _credit_currency_id_field_name = "company_currency_id"
    _credit_company_currency_id_field_name = "company_currency_id"
    _credit_amount_currency_field_name = "value"
    _credit_company_id_field_name = "company_id"
    _credit_date_field_name = "final_date"
    _credit_need_date_due = False
    _credit_date_due_field_name = False

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        related=False,
        compute="_compute_journal_id",
        store=False,
        readonly=False,
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        related="stock_move_id.debit_account_id",
        readonly=False,
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        related="stock_move_id.credit_account_id",
        readonly=False,
    )
    analytic_account_id = fields.Many2one(
        related="stock_move_id.analytic_account_id",
        readonly=False,
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="stock_move_id.picking_id.partner_id",
        readonly=False,
    )
    date_method = fields.Selection(
        string="Date Method",
        selection=[
            ("auto", "Automatic"),
            ("manual", "Manual"),
        ],
        required=True,
        default="auto",
    )
    manual_date = fields.Date(
        string="Manual Date",
    )
    final_date = fields.Date(
        string="Date",
        compute="_compute_final_date",
        store=True,
        compute_sudo=True,
    )
    date = fields.Date(
        string="Automatic Date",
        compute="_compute_date",
        store=True,
        compute_sudo=True,
    )
    account_move_date = fields.Date(
        string="Account Move Date",
        related="account_move_id.date",
        store=True,
    )
    date_is_equal = fields.Boolean(
        string="SVL Date is Equal to Journal Entry Date",
        compute="_compute_date_is_equal",
        store=True,
    )
    debit_move_line_id = fields.Many2one(
        string="Debit Move Line",
        comodel_name="account.move.line",
        readonly=False,
    )
    credit_move_line_id = fields.Many2one(
        string="Credit Move Line",
        comodel_name="account.move.line",
        readonly=False,
    )
    stock_move_date = fields.Datetime(
        string="Stock Move Date",
        related="stock_move_id.date",
        store=True,
    )
    datetime_is_equal = fields.Boolean(
        string="SVL Create Date is Equal to Stock Move Date",
        compute="_compute_datetime_is_equal",
        store=True,
    )

    # Usage
    usage_ids = fields.One2many(
        comodel_name="stock_valuation_layer_usage",
        inverse_name="stock_valuation_layer_id",
        string="Valuation Usage",
        help="Trace on what stock moves has the stock valuation been used in, "
        "including the quantities taken.",
    )
    incoming_usage_ids = fields.One2many(
        comodel_name="stock_valuation_layer_usage",
        inverse_name="dest_stock_valuation_layer_id",
        string="Incoming Valuation Usage",
        help="Trace on what stock moves has the stock valuation been used in, "
        "including the quantities taken.",
    )
    incoming_usage_quantity = fields.Float(
        string="Incoming Usage quantity",
        compute="_compute_incoming_usages",
        store=True,
    )
    incoming_usage_value = fields.Float(
        string="Incoming Usage value",
        compute="_compute_incoming_usages",
        store=True,
    )
    incoming_usage_quantity_diff = fields.Float(
        string="Incoming Usage Quantity Diff",
        compute="_compute_incoming_usage_diff",
        store=True,
    )
    usage_quantity_diff = fields.Float(
        string="Usage Quantity Diff",
        compute="_compute_usage_diff",
        store=True,
    )

    @api.depends(
        "date_method",
        "date",
        "manual_date",
    )
    def _compute_final_date(self):
        for record in self:
            if record.date_method == "auto":
                result = record.date
            else:
                result = record.manual_date
            record.final_date = result

    @api.depends(
        "date",
        "account_move_date",
        "account_move_id",
        "account_move_id.date",
    )
    def _compute_date_is_equal(self):
        for record in self:
            result = True
            if record.date != record.account_move_date:
                result = False
            record.date_is_equal = result

    @api.depends(
        "date",
        "stock_move_date",
        "stock_move_id",
        "stock_move_id.date",
    )
    def _compute_datetime_is_equal(self):
        for record in self:
            result = True
            if record.stock_move_id and record.create_date != record.stock_move_date:
                result = False
            record.datetime_is_equal = result

    @api.depends(
        "quantity",
        "incoming_usage_quantity",
    )
    def _compute_incoming_usage_diff(self):
        for record in self:
            result = abs(record.quantity) - abs(record.incoming_usage_quantity)
            record.incoming_usage_quantity_diff = result

    @api.depends(
        "quantity",
        "usage_quantity",
    )
    def _compute_usage_diff(self):
        for record in self:
            result = abs(record.quantity) - abs(record.usage_quantity)
            record.usage_quantity_diff = result

    @api.depends(
        "incoming_usage_ids.quantity",
        "incoming_usage_ids.value",
    )
    def _compute_incoming_usages(self):
        for rec in self:
            rec.incoming_usage_quantity = sum(rec.incoming_usage_ids.mapped("quantity"))
            rec.incoming_usage_value = sum(rec.incoming_usage_ids.mapped("value"))

    usage_quantity = fields.Float(
        string="Usage Quantity",
        compute="_compute_usage_values",
        store=True,
    )
    usage_value = fields.Float(
        string="Usage Value",
        compute="_compute_usage_values",
        store=True,
    )

    @api.depends(
        "usage_ids.quantity",
        "usage_ids.value",
    )
    def _compute_usage_values(self):
        for rec in self:
            rec.usage_quantity = sum(rec.usage_ids.mapped("quantity"))
            rec.usage_value = sum(rec.usage_ids.mapped("value"))

    def _compute_journal_id(self):
        for record in self:
            journal = False
            if (
                record.stock_move_id.picking_id
                and record.stock_move_id.picking_id.journal_id
            ):
                journal = record.stock_move_id.picking_id.journal_id.id
            elif record.stock_move_id.picking_type_id.journal_id:
                journal = record.stock_move_id.picking_type_id.journal_id.id
            record.journal_id = journal

    @api.depends("create_date")
    def _compute_date(self):
        for record in self:
            record.date = fields.Date.to_date(record.create_date)

    def action_create_accounting_entry(self):
        for record in self.sudo():
            record._create_accounting_entry()

    def action_delete_accounting_entry(self):
        for record in self.sudo():
            record._delete_accounting_entry()

    def action_sync_date_with_stock_move(self):
        for record in self.sudo():
            record._sync_date_with_stock_move()

    def _sync_date_with_stock_move(self):
        self.ensure_one()
        query = """
            UPDATE public.stock_valuation_layer
                SET create_date = %(create_date)s
            WHERE id = %(svl_ids)s
        """
        params = {
            "create_date": self.stock_move_id.date,
            "svl_ids": self.id,
        }
        self._cr.execute(query, params)
        self._compute_datetime_is_equal()

    def _create_accounting_entry(self):
        if self.account_move_id:
            return True

        self._create_standard_move()  # Mixin
        debit_ml, credit_ml = self._create_standard_ml()  # Mixin
        self.write(
            {
                "debit_move_line_id": debit_ml.id,
                "credit_move_line_id": credit_ml.id,
            }
        )
        self.account_move_id.write(
            {
                "stock_move_id": self.stock_move_id.id,
            }
        )
        self._post_standard_move()  # Mixin

    def _delete_accounting_entry(self):
        self.ensure_one()
        self._delete_standard_move()  # Mixin

    def _add_incoming_usage(self, incoming_svl):
        self.ensure_one()

        # TODO: Check

        Usage = self.env["stock_valuation_layer_usage"]
        qty = min(
            self.usage_quantity_diff, abs(incoming_svl.incoming_usage_quantity_diff)
        )
        data = {
            "stock_valuation_layer_id": self.id,
            "dest_stock_valuation_layer_id": incoming_svl.id,
            "quantity": qty,
            "value": qty * self.unit_cost,
        }
        Usage.create(data)
