from odoo import models
import datetime

class PartnerTransactionXLSX(models.AbstractModel):
    _name = 'report.partner_transaction_report.partner_transaction_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_report_name(self, report, data=False):
        return ""

    def get_workbook_options(self):
        """
        See https://xlsxwriter.readthedocs.io/workbook.html constructor options
        :return: A dictionary of options
        """
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        return {
            'filename': f'cari_hareket_ozeti_{current_date}.xlsx',
            'in_memory': True
        }

    def generate_xlsx_report(self, workbook, data, partners):

        report_data = data.get('report_data', [])
        report_title = data.get('report_title', 'Tüm Cariler')

        bold = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        number_format = workbook.add_format({'num_format': '#,##0.00'})

        sheet = workbook.add_worksheet('Cari Hareket Özeti')

        headers = [
            'Cari Adı', 'Telefon',
            'Ortalama Tarihi', 'Ort. Gün',
            'Borç Ort. Tarihi', 'Alacak Ort. Tarihi',
            'Borç', 'Alacak', 'Bakiye'
        ]

        sheet.set_column('A:A', 40)  # Cari Adı
        sheet.set_column('B:B', 15)  # Telefon
        sheet.set_column('C:C', 20)  #
        sheet.set_column('D:D', 10)  #
        sheet.set_column('E:E', 20)  #
        sheet.set_column('F:F', 20)  #
        sheet.set_column('G:I', 15)  #

        title = f'Cari Hareket Özeti Raporu - {report_title}'
        sheet.merge_range('A1:J1', title, bold)

        sheet.write(1, 0, f'Oluşturulma Tarihi: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}', bold)

        for col, header in enumerate(headers):
            sheet.write(3, col, header, bold)

        row = 4
        for line in report_data:
            sheet.write(row, 0, line['partner_name'])
            sheet.write(row, 1, line['partner_phone'] or '')

            sheet.write(row, 2, line['avg_transaction_date'], date_format)
            sheet.write(row, 3, line['days_since_avg_transaction'])

            sheet.write(row, 4, line['avg_debit_date'], date_format)
            sheet.write(row, 4, line['avg_credit_date'], date_format)

            sheet.write(row, 6, line['net_debit'], number_format)
            sheet.write(row, 7, line['net_credit'], number_format)
            sheet.write(row, 8, line['net_balance'], number_format)
            row += 1

        # if report_data:
        #     sheet.write(row + 1, 0, 'TOPLAM', bold)
        #     for col in range(6, 10):
        #         start_cell = chr(65 + col) + '5'  # G5, H5, I5, J5
        #         end_cell = chr(65 + col) + str(row)
        #         formula = f'=SUM({start_cell}:{end_cell})'
        #         sheet.write_formula(row + 1, col, formula, number_format)
