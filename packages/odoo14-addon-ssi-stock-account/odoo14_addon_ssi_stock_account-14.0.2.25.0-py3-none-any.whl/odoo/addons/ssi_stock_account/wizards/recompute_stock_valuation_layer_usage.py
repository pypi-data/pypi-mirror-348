# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RecomputeStockValuationLayer(models.TransientModel):
    _name = "recompute_stock_valuation_layer_usage"
    _description = "Recompute Stock Valuation Layer Usage"

    @api.model
    def _default_svl_id(self):
        result = []
        if self.env.context.get("active_model", False) == "stock.valuation.layer":
            result = self.env.context.get("active_id", [])
        return result

    svl_id = fields.Many2one(
        string="Stock Valuation Layer",
        comodel_name="stock.valuation.layer",
        default=lambda self: self._default_svl_id(),
    )
    allowed_svl_ids = fields.Many2many(
        string="Allowed SVLs",
        comodel_name="stock.valuation.layer",
        compute="_compute_allowed_svl_ids",
        store=False,
    )
    svl_ids = fields.Many2many(
        string="Stock Valuation Layers",
        comodel_name="stock.valuation.layer",
        column1="source_svl_id",
        column2="dest_svl_id",
    )

    @api.depends(
        "svl_id",
    )
    def _compute_allowed_svl_ids(self):
        SVL = self.env["stock.valuation.layer"]
        for record in self:
            criteria = [
                ("product_id", "=", record.svl_id.product_id.id),
                ("date", ">=", record.svl_id.date),
                ("incoming_usage_quantity_diff", "!=", 0.0),
                ("quantity", "<", 0.0),
            ]
            svls = SVL.search(criteria)
            record.allowed_svl_ids = svls.ids

    def action_confirm(self):
        for record in self.sudo():
            record._confirm()

    def _confirm(self):
        self.ensure_one()
        Usage = self.env["stock_valuation_layer_usage"]
        for dest_svl in self.svl_ids:
            qty = min(
                self.svl_id.usage_quantity_diff,
                abs(dest_svl.incoming_usage_quantity_diff),
            )
            data = {
                "stock_valuation_layer_id": self.svl_id.id,
                "dest_stock_valuation_layer_id": dest_svl.id,
                "quantity": qty,
                "value": qty * self.svl_id.unit_cost,
            }
            Usage.create(data)
