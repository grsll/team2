from odoo import models, fields

class Vehicle(models.Model):
    _name = 'compose_auto_clean.vehicle'
    _description = 'Tabel Kendaraan'

    name = fields.Char(string='Plat Nomor Kendaraan', required=True)
    vehicle_type = fields.Selection([
        ('mobil', 'Mobil'),
        ('motor', 'Motor')
    ], string='Jenis Kendaraan', required=True, default='mobil')
    brand = fields.Char(string='Merek Kendaraan')
    color = fields.Char(string='Warna Kendaraan')
    customer_id = fields.Many2one('res.partner', string='Pemilik Kendaraan', required=True, ondelete='cascade')
    carwash_ids = fields.One2many('compose_auto_clean.carwash_order', 'vehicle_id', string='Riwayat Cuci')