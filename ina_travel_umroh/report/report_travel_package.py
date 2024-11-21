from odoo import api, fields, models


class CourseXlsx(models.AbstractModel):
    _name = "report.ina_travel_umroh.report_travel"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet("Travel %s" % obj.name)
        text_top_style = workbook.add_format(
            {
                "font_size": 12,
                "bold": True,
                "font_color": "white",
                "bg_color": "#b904bf",
                "valign": "vcenter",
                "text_wrap": True,
            }
        )
        text_header_style = workbook.add_format(
            {
                "font_size": 12,
                "bold": True,
                "font_color": "white",
                "bg_color": "#b904bf",
                "valign": "vcenter",
                "text_wrap": True,
                "align": "center",
            }
        )
        text_style = workbook.add_format(
            {"font_size": 12, "valign": "vcenter", "text_wrap": True, "align": "center"}
        )
        number_style = workbook.add_format(
            {
                "num_format": "#,##0",
                "font_size": 12,
                "align": "right",
                "valign": "vcenter",
                "text_wrap": True,
            }
        )

        sheet.write(1, 2, "Manifest", text_top_style)
        sheet.write(1, 3, obj.ref)

        row = 4
        sheet.freeze_panes(6, 10)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 9, 15)
        header = [
            "No",
            "Title",
            "Gender",
            "FullName",
            "Tempat Lahir",
            "Tanggal Lahir",
            "NO. PASSPOR",
            "PASSPOR ISSUED",
            "PASSPOR EXPIRED",
            "IMIGRASI",
            "MAHROM",
            "USIA",
            "NIK",
            "ORDER",
            "ROOM TYPE",
            "ROOM LEADER",
            "NO. ROOM",
            "ALAMAT",
        ]
        sheet.write_row(row, 0, header, text_header_style)

        no_list = []
        tiitle = []
        gender = []
        fullname = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passport = []
        passpor_issued = []
        passpor_expired = []
        imigrasi = []
        mahrom = []
        usia = []
        nik = []
        order = []
        room_type = []
        room_leader = []
        no_room = []
        alamat = []

        no = 1
        for x in obj.manifest_line:
            no_list.append(no)
            tiitle.append(x.title or "")
            fullname.append(x.nama_panjang or "")
            gender.append(x.jenis_kelamin or "")
            tempat_lahir.append(x.tempat_lahir or "")
            tanggal_lahir.append(x.tanggal_lahir or "")
            no_passport.append(x.no_passport or "")
            passpor_issued.append(x.passpor_issued or "")
            passpor_expired.append(x.passpor_expired or "")
            imigrasi.append(x.imigrasi or "")
            mahrom.append(x.mahrom_id.name or "")
            usia.append(x.umur or "")
            nik.append(x.no_ktp or "")
            # order.append(x.state.capitalize())
            room_type.append(x.tipe_kamar or "")
            alamat.append(x.alamat or "")

            no += 1

        row += 1
        sheet.write_column(row, 0, no_list, text_style)
        sheet.write_column(row, 1, tiitle, text_style)
        sheet.write_column(row, 2, gender, text_style)
        sheet.write_column(row, 3, fullname, text_style)
        sheet.write_column(row, 4, tempat_lahir, text_style)
        sheet.write_column(row, 5, tanggal_lahir, text_style)
        sheet.write_column(row, 6, no_passport, text_style)
        sheet.write_column(row, 7, passpor_issued, text_style)
        sheet.write_column(row, 8, passpor_expired, text_style)
        sheet.write_column(row, 9, imigrasi, text_style)
        sheet.write_column(row, 10, mahrom, text_style)
        sheet.write_column(row, 11, usia, number_style)
        sheet.write_column(row, 12, nik, text_style)

        header = [
            "No",
            "AIRLINE",
            "DEPARTURE DATE",
            "DEPARTURE CITY",
            "ARIVAL CITY",
        ]
        sheet.write_row(11, 2, header, text_header_style)
        row_airline = 12

        no_list_airline = []
        airline = []
        departure_date = []
        departure_city = []
        arrival_city = []

        no = 1
        for x in obj.airline_line:
            no_list_airline.append(no)
            airline.append(x.partner_id.name or "")
            departure_date.append(x.tanggal_berangkat or "")
            departure_city.append(x.kota_asal or "")
            arrival_city.append(x.kota_tujuan or "")
            no += 1

        sheet.write_column(row_airline, 2, no_list_airline, text_style)
        sheet.write_column(row_airline, 3, airline, text_style)
        sheet.write_column(row_airline, 4, departure_date, text_style)
        sheet.write_column(row_airline, 5, departure_city, text_style)
        sheet.write_column(row_airline, 6, arrival_city, text_style)
