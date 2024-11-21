from odoo import models, fields, api


class JamaahWizard(models.TransientModel):
    _name = "jamaah.wizard"
    _description = "Wizard untuk Menambahkan Jamaah ke Manifest"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    jamaah_id = fields.Many2one("res.partner", string="Jamaah", required=True)

    title = fields.Char(string="Title")
    nama_panjang = fields.Char(
        related="jamaah_id.name", string="Nama Panjang", readonly=True
    )
    jenis_kelamin = fields.Selection(
        related="jamaah_id.jenis_kelamin", string="Jenis Kelamin", readonly=True
    )
    no_ktp = fields.Char(related="jamaah_id.no_ktp", string="No KTP", readonly=True)
    no_passport = fields.Char(
        related="jamaah_id.no_passpor", string="No Passport", readonly=True
    )
    tanggal_lahir = fields.Date(
        related="jamaah_id.tanggal_lahir", string="Tanggal Lahir", readonly=True
    )
    tempat_lahir = fields.Char(
        related="jamaah_id.tempat_lahir", string="Tempat Lahir", readonly=True
    )
    tanggal_berlaku = fields.Date(
        related="jamaah_id.tanggal_berlaku", string="Tanggal Berlaku", readonly=True
    )
    tanggal_expired = fields.Date(
        related="jamaah_id.tanggal_expired", string="Tanggal Expired", readonly=True
    )
    imgirasi = fields.Char(
        related="jamaah_id.imigrasi", string="Imigrasi", readonly=True
    )
    nama_passport = fields.Char(
        related="jamaah_id.nama_passpor", string="Nama Passport", readonly=True
    )

    scan_passpor = fields.Binary(string="Scan Paspor", related="jamaah_id.scan_passpor")
    scan_ktp = fields.Binary(string="Scan KTP", related="jamaah_id.scan_ktp")
    scan_buku_nikah = fields.Binary(
        string="Scan Buku Nikah", related="jamaah_id.scan_buku_nikah"
    )
    scan_kartu_keluarga = fields.Binary(
        string="Scan Kartu Keluarga", related="jamaah_id.scan_kartu_keluarga"
    )

    title = fields.Char(compute="_compute_title", default="")

    tipe_kamar = fields.Selection(
        [
            ("double", "Double"),
            ("triple", "Triple"),
            ("quad", "Quad"),
        ],
        string="Tipe Kamar",
        default="doble",
    )

    umur = fields.Char(string="Umur")
    mahrom_id = fields.Many2one("res.partner", string="Mahrom")
    agent = fields.Char(string="Agent")
    notes = fields.Char("notes")

    @api.depends("jamaah_id")
    def _compute_title(self):
        if self.jamaah_id.jenis_kelamin == "perempuan":
            self.title = "Madam"
        else:
            self.title = "Mister"

    def add_jamaah_to_manifest(self):

        self.env["manifest"].create(
            {
                "sale_order_id": self.sale_order_id.id,
                "title": self.title,
                "nama_panjang": self.nama_panjang,
                "jenis_kelamin": self.jenis_kelamin,
                "no_ktp": self.no_ktp,
                "no_passport": self.no_passport,
                "tanggal_lahir": self.tanggal_lahir,
                "tempat_lahir": self.tempat_lahir,
                "tanggal_berlaku": self.tanggal_berlaku,
                "tanggal_expired": self.tanggal_expired,
                "imgirasi": self.imgirasi,
                "tipe_kamar": self.tipe_kamar,
                "nama_passport": self.nama_passport,
                "umur": self.umur,
                "mahrom_id": self.mahrom_id.id,
                "agent": self.agent,
            }
        )
