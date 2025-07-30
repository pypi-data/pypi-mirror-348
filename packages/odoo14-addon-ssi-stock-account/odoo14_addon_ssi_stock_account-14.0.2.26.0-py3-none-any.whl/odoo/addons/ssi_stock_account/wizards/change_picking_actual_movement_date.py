# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class ChangePickingActualMovementDate(models.TransientModel):
    _name = "change_picking_actual_movement_date"
    _inherit = "change_picking_actual_movement_date"
    _description = "Change Picking Actual Movement Date"

    def _confirm(self):
        _super = super(ChangePickingActualMovementDate, self)
        for picking in self.picking_ids:
            if picking.account_move_ids:
                error_message = _(
                    """
                Context: Change picking actual movement date
                Database ID: %s
                Problem: Journal entry already exist for %s
                Solution: Cancel accounting entries
                """
                    % (picking.id, picking.display_name)
                )
                raise UserError(error_message)
        _super._confirm()
        self._update_svl_actual_movement_date()

    def _update_svl_actual_movement_date(self):
        self.ensure_one()
        if len(self.picking_ids.stock_valuation_layer_ids) > 0:
            query = """
                UPDATE public.stock_valuation_layer
                    SET create_date = %(create_date)s
                WHERE id IN %(svl_ids)s
            """
            params = {
                "create_date": self.actual_movement_date,
                "svl_ids": tuple(self.picking_ids.stock_valuation_layer_ids.ids),
            }
            self._cr.execute(query, params)
            self.picking_ids.stock_valuation_layer_ids._compute_date()
