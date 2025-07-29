from extendable_pydantic import StrictExtendableBaseModel

from odoo.addons.shopinvader_schema_sale.schemas.sale import Sale


class Sale(Sale, extends=True):
    shop_only_quotation: bool | None = None

    @classmethod
    def from_sale_order(cls, odoo_rec):
        res = super().from_sale_order(odoo_rec)
        res.shop_only_quotation = odoo_rec.shop_only_quotation
        return res


class QuotationUpdateInput(StrictExtendableBaseModel, extra="ignore"):
    client_order_ref: str | None = None

    def to_sale_order_vals(self) -> dict:
        return {"client_order_ref": self.client_order_ref}


class QuotationConfirmInput(StrictExtendableBaseModel):
    """Extend it if you need params for the confirmation"""
