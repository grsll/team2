from odoo import models, fields, api

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
    active = fields.Boolean(string='Aktif', default=True)
    wash_count = fields.Integer(string='Jumlah Cuci', compute='_compute_wash_count')

    @api.depends('wash_order_ids')
    def _compute_wash_count(self):
        for rec in self:
            rec.wash_count = len(rec.wash_order_ids)
    
    @api.onchange('name')
    def _onchange_name_upper(self):
        if self.name:
            self.name = self.name.upper()

    def action_archive_vehicle(self):
        for rec in self:
            rec.active = False
            
    def action_view_wash_history(self):
        return {
            'name': _('Riwayat Cuci Kendaraan'),
            'type': 'ir.actions.act_window',
            'res_model': 'cdn.wash.order',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id},
        }