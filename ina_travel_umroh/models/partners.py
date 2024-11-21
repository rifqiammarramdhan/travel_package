# imo
from odoo import _, api, fields, models


# oomodel
class Partner(models.Model):
    _inherit = "res.partner"

    no_ktp = fields.Char(string="No. KTP")
    umur = fields.Integer(string="umur")
    nama_ayah = fields.Char(string="Nama Ayah")
    pekerjaan_ayah = fields.Char(string="Pekerjaan Ayah")
    tempat_lahir = fields.Char(string="Tempat Lahir")
    pendidikan = fields.Char(string="Pendidikan")
    status_hubungan = fields.Selection(
        [
            ("belum_menikah", "Belum Menikah"),
            ("menikah", "Menikah"),
            ("cerai", "Cerai"),
            ("janda", "Janda"),
            ("duda", "Duda"),
        ],
        string="Status Pernikahan",
    )
    jenis_kelamin = fields.Selection(
        [
            ("laki_laki", "Laki-Laki"),
            ("perempuan", "Perempuan"),
        ],
        string="Jenis Kelamin",
    )
    nama_ibu = fields.Char(string="Nama Ibu")
    pekerjaan_ibu = fields.Char(string="Pekerjaan Ibu")
    tanggal_lahir = fields.Date(string="Tanggal Lahir")
    golongan_darah = fields.Selection(
        [
            ("a", "A"),
            ("b", "B"),
            ("ab", "AB"),
            ("o", "O"),
            ("tidak_tahu", "Tidak Tahu"),
        ],
        string="Golongan Darah",
    )
    ukuran_baju = fields.Selection(
        [
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
        ],
        string="Ukuran Baju",
    )
    mahrom_line = fields.One2many("manifest", "mahrom_id", string="Mahrom")
    no_passpor = fields.Char(string="No. Paspor")
    tanggal_berlaku = fields.Date(string="Tanggal Berlaku")
    imigrasi = fields.Char(string="Imigrasi")
    nama_passpor = fields.Char(string="Nama Paspor")
    tanggal_expired = fields.Date(string="Tanggal Expired")
    scan_passpor = fields.Binary(string="Scan Paspor")
    scan_ktp = fields.Binary(string="Scan KTP")
    scan_buku_nikah = fields.Binary(string="Scan Buku Nikah")
    scan_kartu_keluarga = fields.Binary(string="Scan Kartu Keluarga")
    is_airlines = fields.Boolean(string="Airlines")
    is_hotel = fields.Boolean(string="Hotel")
    is_jamaah = fields.Boolean(string="Jamaah")

    def default_get(self, fields):
        res = super(Partner, self).default_get(fields)
        if self.env.context.get("default_is_hotel"):
            res["is_hotel"] = True
        if self.env.context.get("default_is_airline"):
            res["is_airline"] = True
        return res
