# -*- coding: utf-8 -*-
{
    "name": "Partner Transaction Report",
    "version": "13.0.1.0.0",
    "category": "Accounting",
    "summary": "Cari Hareket Özeti Raporu",
    "description": """
        Cari hareket özeti raporu ile:
        * Seçilen carilerin hareket özetlerini görüntüleme
        * Ortalama işlem tarihi ve gün hesaplama
        * Toplam işlem tutarları ve bakiye bilgileri
    """,
    "author": "Kıta Yazılım",
    "website": "https://kitayazilim.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "account",
        "report_xlsx",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/partner_transaction_wizard_view.xml",
        "report/partner_transaction_xlsx.xml"
    ],
    "installable": True,
    "application": False,
}
