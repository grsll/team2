# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CarwashOrder(models.Model):
    _name = "compose_auto_clean.carwash_order"
    _description = "Carwash Order"

    # Bisa menggunakan customer dari compose_auto_clean.customer
    customer_id = fields.Many2one(
        "compose_auto_clean.customer", string="Customer", required=True
    )
    vehicle_id = fields.Many2one(
        "compose_auto_clean.vehicle",
        string="Vehicle",
        required=True,
        domain="[('customer_id', '=', customer_id)]",
    )
    service_name = fields.Selection(
        [
            ("basic_wash", "Basic Wash"),
            ("premium_wash", "Premium Wash"),
            ("deluxe_wash", "Deluxe Wash"),
        ],
        string="Service Name",
        required=True,
    )
    price = fields.Float(string="Price", compute="_compute_price", readonly=True)
    duration = fields.Float(
        string="Duration (hours)", compute="_compute_duration", readonly=True
    )
    variant = fields.Selection(
        [
            ("basic", "Basic"),
            ("premium", "Premium"),
            ("deluxe", "Deluxe"),
        ],
        string="Variant",
        compute="_compute_variant",
        readonly=True,
    )
    payment_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("belum bayar", "Belum Bayar"),
            ("lunas", "Lunas"),
        ],
        string="Payment Status",
        default="draft",
    )
    order_date = fields.Datetime(string="Order Date", default=fields.Datetime.now)

    @api.depends("service_name")
    def _compute_price(self):
        for record in self:
            if record.service_name == "basic_wash":
                record.price = 50000
            elif record.service_name == "premium_wash":
                record.price = 75000
            elif record.service_name == "deluxe_wash":
                record.price = 100000
            else:
                record.price = 0

    @api.depends("service_name")
    def _compute_duration(self):
        for record in self:
            if record.service_name == "basic_wash":
                record.duration = 1
            elif record.service_name == "premium_wash":
                record.duration = 1.5
            elif record.service_name == "deluxe_wash":
                record.duration = 2
            else:
                record.duration = 0

    @api.depends("service_name")
    def _compute_variant(self):
        for record in self:
            if record.service_name == "basic_wash":
                record.variant = "basic"
            elif record.service_name == "premium_wash":
                record.variant = "premium"
            elif record.service_name == "deluxe_wash":
                record.variant = "deluxe"
            else:
                record.variant = False
