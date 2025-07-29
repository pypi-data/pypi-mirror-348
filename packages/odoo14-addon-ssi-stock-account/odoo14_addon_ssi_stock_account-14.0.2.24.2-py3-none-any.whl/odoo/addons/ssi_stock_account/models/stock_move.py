# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move"]

    journal_id = fields.Many2one(
        string="Journal",
        related="picking_id.journal_id",
    )
    debit_usage_id = fields.Many2one(
        string="Debit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
    )
    credit_usage_id = fields.Many2one(
        string="Credit Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )

    svl_total_amount = fields.Float(
        string="SVL. Total Amount",
        compute="_compute_svl_total_amount",
        store=True,
    )
    journal_entry_total_amount = fields.Float(
        string="Journal Entry Total Amount",
        compute="_compute_journal_entry_total_amount",
        store=True,
    )
    svl_journal_entry_diff = fields.Boolean(
        string="SVL Different from Journal Entry",
        compute="_compute_svl_journal_entry_diff",
        store=True,
    )
    abs_svl_journal_entry_diff = fields.Boolean(
        string="Absolute SVL Different from Journal Entry",
        compute="_compute_svl_journal_entry_diff",
        store=True,
    )

    @api.depends(
        "stock_valuation_layer_ids",
        "stock_valuation_layer_ids.value",
    )
    def _compute_svl_total_amount(self):
        for record in self:
            result = 0.0
            for svl in record.stock_valuation_layer_ids:
                result += svl.value
            record.svl_total_amount = result

    @api.depends(
        "account_move_ids",
        "account_move_ids.line_ids",
        "account_move_ids.line_ids.debit",
        "account_move_ids.line_ids.credit",
    )
    def _compute_journal_entry_total_amount(self):
        for record in self:
            result = 0.0
            for am in record.account_move_ids:
                for line in am.line_ids:
                    result += line.debit
            record.journal_entry_total_amount = result

    @api.depends(
        "svl_total_amount",
        "journal_entry_total_amount",
    )
    def _compute_svl_journal_entry_diff(self):
        for record in self:
            result = abs_result = False
            if record.svl_total_amount != record.journal_entry_total_amount:
                result = True

            if abs(record.svl_total_amount) != abs(record.journal_entry_total_amount):
                abs_result = True

            record.svl_journal_entry_diff = result
            record.abs_svl_journal_entry_diff = abs_result

    @api.onchange(
        "debit_usage_id",
        "product_id",
    )
    def onchange_debit_account_id(self):
        self.debit_account_id = False
        if self.product_id and self.debit_usage_id:
            self.debit_account_id = self.product_id._get_product_account(
                usage_code=self.debit_usage_id.code
            )

    @api.onchange(
        "credit_usage_id",
        "product_id",
    )
    def onchange_credit_account_id(self):
        self.credit_account_id = False
        if self.product_id and self.credit_usage_id:
            self.credit_account_id = self.product_id._get_product_account(
                usage_code=self.credit_usage_id.code
            )

    @api.onchange(
        "picking_type_id",
        "price_unit",
        "product_id",
    )
    def onchange_debit_usage_id(self):
        self.debit_usage_id = False
        if self.picking_type_id and self.picking_type_id.debit_account_method:
            if self.picking_type_id.debit_account_method == "manual":
                self.debit_usage_id = self.picking_type_id.debit_usage_id
            elif self.picking_type_id.debit_account_method == "code":
                try:
                    localdict = self._get_account_localdict()
                    safe_eval(
                        self.picking_type_id.debit_account_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception:
                    result = False
                self.debit_usage_id = result

    @api.onchange(
        "picking_type_id",
        "price_unit",
        "product_id",
    )
    def onchange_credit_usage_id(self):
        self.credit_usage_id = False
        if self.picking_type_id and self.picking_type_id.credit_account_method:
            if self.picking_type_id.credit_account_method == "manual":
                self.credit_usage_id = self.picking_type_id.credit_usage_id
            elif self.picking_type_id.credit_account_method == "code":
                try:
                    localdict = self._get_account_localdict()
                    safe_eval(
                        self.picking_type_id.credit_account_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception:
                    result = False
                self.credit_usage_id = result

    def _get_account_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _action_assign(self):
        _super = super(StockMove, self)
        _super._action_assign()

        for record in self.sudo():
            if not record.debit_account_id:
                record.onchange_debit_usage_id()
                record.onchange_debit_account_id()

            if not record.credit_account_id:
                record.onchange_credit_usage_id()
                record.onchange_credit_account_id()

    def _action_cancel(self):
        _super = super(StockMove, self)
        _super._action_cancel()
        for record in self.sudo():
            record.stock_valuation_layer_ids.unlink()
