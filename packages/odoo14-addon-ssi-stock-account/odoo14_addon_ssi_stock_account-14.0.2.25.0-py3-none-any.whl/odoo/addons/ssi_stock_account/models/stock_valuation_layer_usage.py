# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockValuationLayerUsage(models.Model):
    _name = "stock_valuation_layer_usage"
    _description = "Stock Valuation Layer Usage"

    stock_valuation_layer_id = fields.Many2one(
        comodel_name="stock.valuation.layer",
        string="Stock Valuation Layer",
        help="Valuation Layer that was used",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="stock_valuation_layer_id.product_id",
        store=True,
    )
    dest_stock_valuation_layer_id = fields.Many2one(
        comodel_name="stock.valuation.layer",
        string="Destination Stock Valuation Layer",
        help="Valuation Layer that was used",
        required=False,
    )
    quantity = fields.Float(string="Taken Quantity")
    value = fields.Float(string="Taken Value")
