# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
    _name = "compose_auto_clean.customer"
    _description = "Customer"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(string="Active", default=True)

    # Workflow Logic
    customer_type = fields.Selection(
        [("baru", "Customer Baru"), ("lama", "Customer Lama")],
        string="Status Registrasi",
        default="baru",
        tracking=True,
    )

    # Search field for existing customer
    existing_customer_id = fields.Many2one(
        "compose_auto_clean.customer", string="Cari Data Customer Lama"
    )

    # Data Fields
    name = fields.Char(string="Nama", required=True, tracking=True)
    address = fields.Text(string="Alamat")
    phone = fields.Char(string="Nomor HP")
    vehicle_type = fields.Selection(
        [
            ("motor", "Motor"),
            ("mobil", "Mobil"),
            ("truk", "Truk"),
            ("bus", "Bus"),
        ],
        string="Jenis Kendaraan",
    )
    vehicle_number = fields.Char(string="Nomor Kendaraan")

    # Relationship to single current vehicle (for easy entry)
    vehicle_id = fields.Many2one(
        "compose_auto_clean.vehicle", string="Kendaraan Saat Ini", tracking=True
    )

    # Tracking
    visit_count = fields.Integer(
        string="Jumlah Kunjungan", compute="_compute_visit_count", store=True
    )
    last_visit_date = fields.Datetime(string="Kunjungan Terakhir")
    order_ids = fields.One2many(
        "compose_auto_clean.carwash_order", "customer_id", string="Orders"
    )

    @api.onchange("existing_customer_id")
    def _onchange_existing_customer(self):
        if self.customer_type == "lama" and self.existing_customer_id:
            res = self.existing_customer_id
            self.name = res.name
            self.address = res.address
            self.phone = res.phone
            self.vehicle_type = res.vehicle_type
            self.vehicle_number = res.vehicle_number
            self.vehicle_id = res.vehicle_id

    @api.depends("order_ids")
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.order_ids)

    def _sync_vehicle_data(self):
        """Helper to create or update vehicle record from customer data"""
        Vehicle = self.env["compose_auto_clean.vehicle"]
        for record in self:
            if record.vehicle_number:
                # Cari kendaraan berdasarkan nomor plat
                vehicle = Vehicle.search(
                    [("name", "=", record.vehicle_number)], limit=1
                )

                vals = {
                    "name": record.vehicle_number,
                    "vehicle_type": record.vehicle_type,
                    "customer_id": record.id,
                }

                if vehicle:
                    # Update jika pemiliknya sama atau belum ada pemilik
                    if not vehicle.customer_id or vehicle.customer_id.id == record.id:
                        vehicle.write(vals)
                        record.vehicle_id = vehicle.id
                else:
                    # Buat baru jika tidak ditemukan
                    new_vehicle = Vehicle.create(vals)
                    record.vehicle_id = new_vehicle.id

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Customer, self).create(vals_list)
        records._sync_vehicle_data()
        return records

    def write(self, vals):
        res = super(Customer, self).write(vals)
        if any(f in vals for f in ["vehicle_number", "vehicle_type"]):
            self._sync_vehicle_data()
        return res
