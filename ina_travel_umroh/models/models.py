from odoo import _, api, fields, models


class TravelPackage(models.Model):
    _name = "travel.package"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Travel Package"

    ref = fields.Char(string="Referensi", readonly=True, default="/")
    name = fields.Char(string="PO Number", default="New", readonly=True, tracking=True)
    tanggal_berangkat = fields.Date("Tanggal Berangkat", required=True, tracking=True)
    tanggal_kembali = fields.Date("Tanggal Kembali", required=True, tracking=True)
    sale_id = fields.Many2one("product.product", string="Sale", tracking=True)
    product_id = fields.Many2many("product.product", string="Products", tracking=True)
    mrp_bom_id = fields.Many2one("mrp.bom", string="Mrp Bom", tracking=True)
    sale_order_id = fields.Many2one("sale.order", string="Sale Order", tracking=True)
    quota = fields.Integer("Quota", tracking=True)
    remaining_quota = fields.Integer(
        "Remaining Quota", compute="_compute_remaining_quota"
    )
    quota_progress = fields.Float("Quota Progress", compute="compute_quota_progress")
    jamaah_ids = fields.Many2many(
        "res.partner",
        "travelpackage_jamaah_rel",
        "travel_package_id",
        "partner_id",
        "Peserta",
        readonly=True,
        states={"draft": [("readonly", False)]},
        tracking=True,
    )
    hotel_id = fields.Many2one("product.product", string="Nama Hotel", tracking=True)
    check_in_hotel = fields.Date("Check In", tracking=True)
    check_out_hotel = fields.Date("Check Out", tracking=True)
    hotel_line = fields.One2many(
        "hotel.line", "travel_package_id", string="Hotel Line", tracking=True
    )
    airline_line = fields.One2many(
        "airline.line", "travel_package_id", string="Airline Line", tracking=True
    )
    schedule_line = fields.One2many(
        "schedule.lines", "travel_package_id", string="Schedule Lines", tracking=True
    )
    hpp_line = fields.One2many(
        "hpp.lines", "travel_package_id", string="HPP Lines", tracking=True
    )
    manifest_line = fields.One2many(
        "manifest", "travel_package_id", string="Manifest", tracking=True
    )
    total_cost = fields.Float(
        string="Total Cost", compute="_compute_total_cost", store=True, tracking=True
    )
    name = fields.Char(string="Package Name", tracking=True)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # Cron Scheduler
    def cron_expire_travel(self):
        now = fields.Date.today()
        expired_ids = self.search(
            [("tanggal_kembali", "<", now), ("status", "=", "confirm")]
        )
        expired_ids.write({"status": "done"})

    def set_toDraft(self):
        if self.status == "confirm" or self.status == "cancel":
            self.status = "draft"

    def set_confirm(self):
        if self.status == "draft":
            self.name = f"{self.ref}-Umroh Bintang 5"
            self.status = "confirm"

    def set_toDone(self):
        if self.status == "confirm":
            self.status = "done"

    def set_cancel(self):
        if self.status == "done":
            self.status = "cancel"

    @api.onchange("ref")
    def _onchange_mrp_bom_id(self):
        if self.name == "New":
            self.name = self.ref + "-" + "Umroh Bintang 5"

    @api.model
    def create(self, vals):
        vals["ref"] = self.env["ir.sequence"].next_by_code("travel.package")
        return super(TravelPackage, self).create(vals)

    # Hitung Total
    @api.depends("mrp_bom_id.bom_line_ids", "hpp_line.subtotal")
    def _compute_total_cost(self):
        for package in self:
            total = 0.0
            if package.mrp_bom_id:
                total += sum(line.subtotal for line in package.hpp_line)
            package.total_cost = total

    @api.onchange("mrp_bom_id")
    def _onchange_mrp_bom_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            mrp_bom_line = self.env["mrp.bom.line"].search(
                [("bom_id", "=", self.mrp_bom_id.id)]
            )
            for bom_line in mrp_bom_line:
                vals = {
                    "travel_package_id": self.id,
                    "barang": bom_line.product_id.name,
                    "quantity": bom_line.product_qty,
                    "units": bom_line.product_uom_id.name,
                    "unit_price": bom_line.product_id.lst_price,
                    "subtotal": bom_line.product_qty * bom_line.product_id.lst_price,
                }
                lines.append((0, 0, vals))
            rec.hpp_line = lines

    def func_update_jamaah(self):
        for rec in self:
            lines = [(5, 0, 0)]
            existing_jamaah = self.env["sale.order"].search(
                [("travel_package_id", "=", self.id), ("state", "in", ["sale", "done"])]
            )
            if existing_jamaah:
                for line in existing_jamaah.sale_order_line:
                    vals = {
                        "title": line.title.name,
                        "nama_panjang": line.name,
                        "jenis_kelamin": line.jenis_kelamin,
                        "no_ktp": line.no_ktp,
                        "no_passport": line.no_passpor,
                        "tanggal_lahir": line.tanggal_lahir,
                        "tempat_lahir": line.tempat_lahir,
                        "tanggal_berlaku": line.tanggal_berlaku,
                        "tanggal_expired": line.tanggal_expired,
                        "imigrasi": line.imigrasi,
                        "tipe_kamar": line.tipe_kamar,
                        "nama_passport": line.nama_passpor,
                        "umur": line.umur,
                        "mahrom_id": line.mahrom_id.id,
                        "agent": line.agent,
                    }
                    lines.append((0, 0, vals))
                rec.write({"manifest_line": lines})

    def action_print_report(self):
        report = self.env.ref("ina_travel_umroh.report_travel_xlsx")
        return report.report_action(self)

    @api.depends("quota", "jamaah_ids")
    def compute_quota_progress(self):
        for package in self:
            existing_jamaah = self.env["manifest"].search(
                [("travel_package_id", "=", package.id)]
            )
            if package.quota > 0:
                package.quota_progress = 100 * len(existing_jamaah) / package.quota
            else:
                package.quota_progress = 0.0

    @api.depends("quota", "jamaah_ids")
    def _compute_remaining_quota(self):
        for package in self:
            existing_jamaah = self.env["manifest"].search(
                [("travel_package_id", "=", package.id)]
            )
            package.remaining_quota = package.quota - len(existing_jamaah)


# Hotel Line
class HotelLine(models.Model):
    _name = "hotel.line"
    _description = "HotelLine"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    partner_id = fields.Many2one("res.partner", string="Parner")
    date_check_in = fields.Date(string="Check In Hotel")
    date_check_out = fields.Date(string="Check Out Hotel")
    city = fields.Char(string="Kota", related="partner_id.city")
    is_hotel = fields.Boolean(string="Hotel")


# Airline Lines
class AirlineLine(models.Model):
    _name = "airline.line"
    _description = "Airline Line"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    partner_id = fields.Many2one("res.partner", string="Parner")
    tanggal_berangkat = fields.Date(string="Tanggal Berangkat")
    kota_asal = fields.Char(string="Kota Asal")
    kota_tujuan = fields.Char(string="Kota Tujuan")


# Schedules Line
class ScheduleLines(models.Model):
    _name = "schedule.lines"
    _description = "Schedule Lines"
    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    nama_kegiatan = fields.Char("Nama Kegiatan")
    tanggal_kegiatan = fields.Date("Tangal Kegiatan")


# Manifest
class Manifest(models.Model):
    _name = "manifest"
    _description = "Manifest"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    title = fields.Char(string="Title")
    nama_panjang = fields.Char("nama_panjang")
    jenis_kelamin = fields.Char("jenis_kelamin")
    no_ktp = fields.Char("no_ktp")
    no_passport = fields.Char("no_passport")
    tanggal_lahir = fields.Date("tanggal_lahir")
    tempat_lahir = fields.Char("tempat_lahir")
    tanggal_berlaku = fields.Date("tanggal_berlaku")
    tanggal_expired = fields.Date("tanggal_expired")
    imigrasi = fields.Char("Imigrasi")
    nama_passport = fields.Char("nama_passport")
    tipe_kamar = fields.Char("tipe_kamar")
    umur = fields.Char("umur")
    passpor_issued = fields.Char("")
    passpor_expired = fields.Date("")
    agent = fields.Char("agent")
    notes = fields.Char("notes")
    alamat = fields.Char("alamat")
    mahrom_id = fields.Many2one("res.partner", string="Mahrom")
    scan_passpor = fields.Binary(string="Scan Paspor")
    scan_ktp = fields.Binary(string="Scan KTP")
    scan_buku_nikah = fields.Binary(string="Scan Buku Nikah")
    scan_kartu_keluarga = fields.Binary(string="Scan Kartu Keluarga")


# HPP Line
class HppLines(models.Model):
    _name = "hpp.lines"
    _description = "HPP Lines"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    mrp_bom_id = fields.Many2one("mrp.bom", string="BOM")
    barang = fields.Char(string="Barang")
    quantity = fields.Integer("Quantity")
    units = fields.Char("Units")
    unit_price = fields.Float("Unit Price")
    subtotal = fields.Float("Subtotal")


class PassporSaleOrder(models.Model):
    _name = "passpor.sale.order"
    _description = "Passpor Sale Order"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", ondelete="cascade"
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", delegate=True, ondelete="cascade"
    )
    tipe_kamar = fields.Selection(
        [
            ("double", "Double"),
            ("triple", "Triple"),
            ("quad", "Quad"),
        ]
    )
    mahrom_id = fields.Many2one("res.partner", string="Mahrom")
    agent = fields.Char(string="Agent")
    notes = fields.Char("notes")


#  Sales Order
class SaleOrder(models.Model):
    _inherit = "sale.order"

    travel_package_id = fields.Many2one(
        "travel.package", string="Paket Perjalanan", ondelete="cascade"
    )
    jamaah_id = fields.Many2one("res.partner", string="Jamaah", required=True)
    sale_order_line = fields.One2many(
        "passpor.sale.order", "sale_order_id", string="Sale Order"
    )

    @api.onchange("travel_package_id")
    def _onchange_travel_package_id(self):
        if self.travel_package_id:
            product = self.travel_package_id.sale_id
            if product:
                self.order_line = [(5, 0, 0)]
                self.order_line = [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "product_uom_qty": 1,
                            "price_unit": product.lst_price,
                        },
                    )
                ]
