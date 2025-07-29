from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from odoo import api, models

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_schema_sale.schemas.sale import Sale

quotation_cart_router = APIRouter(tags=["carts"])


@quotation_cart_router.post("/{uuid}/request_quotation")
@quotation_cart_router.post("/current/request_quotation")
@quotation_cart_router.post("/request_quotation")
def request_quotation(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
    uuid: UUID | None = None,
) -> Sale:
    sale = env["shopinvader_api_cart.cart_router.helper"]._request_quotation(
        partner, uuid
    )
    return Sale.from_sale_order(sale)


class ShopinvaderApiCartRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    def _request_quotation(self, partner: ResPartner, uuid: UUID | None = None):
        sale = self.env["sale.order"]._find_open_cart(partner.id, uuid)
        sale.action_request_quotation()
        return sale
