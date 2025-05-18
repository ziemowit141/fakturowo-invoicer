#!/usr/bin/env python3

import csv
import requests

# Fixed seller data - DevBulls LTD
SELLER_DATA = {
    "sprzedawca_nazwa": "DevBulls",
    "sprzedawca_nip": "5273084553",
    "sprzedawca_miasto": "Warszawa",
    "sprzedawca_kod": "00-819",
    "sprzedawca_ulica": "Złota",
    "sprzedawca_budynek": "75A",
    "sprzedawca_lokal": "7",
}

API_ID = ""
API_URL = "https://konto.fakturowo.pl/api"
CSV_FILE = "invoices.csv"

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [field.strip() for field in reader.fieldnames]

    for row in reader:
        buyer_name = f"{row['First Name']} {row['Last Name']}"
        buyer_email = row['Email']
        buyer_company = row['Company'].strip()
        buyer_nip = row.get("NIP", "").strip()  # Add this column if available in CSV

        raw_price = row.get("Price")
        try:
            brutto_price = f"{float(raw_price):.2f}"
        except ValueError:
            print(f"⚠️  Invalid price for {buyer_name}: '{raw_price}', skipping.")
            continue

        print(f"Raw price: {raw_price}")
        print(f"Brutto price: {brutto_price}")

        # Determine buyer type and fields
        buyer_fields = {}
        if buyer_company and buyer_nip:
            buyer_fields = {
                "nabywca_nazwa": buyer_company,
                "nabywca_nip": buyer_nip,
                "nabywca_kraj": "PL",
            }
        else:
            buyer_fields = {
                "nabywca_osoba": "1",
                "nabywca_imie": row["First Name"],
                "nabywca_nazwisko": row["Last Name"],
            }

        # Prepare invoice data
        invoice_data = {
            "api_id": API_ID,
            "api_zadanie": "1",
            "dokument_dostep": "0",
            "dokument_rodzaj": "0",
            "dokument_miejsce": "Warszawa",

            "nabywca_miasto": "N/A",
            "nabywca_kod": "00-000",
            "nabywca_ulica": "N/A",
            "nabywca_budynek": "1",
            "nabywca_lokal": "",

            "produkt_nazwa": row["Ticket title"] or "KCD 2025 Ticket",
            "produkt_ilosc": row["Number of tickets"] or "1",
            "produkt_jm": "szt.",
            "produkt_stawka_vat": "0",
            "produkt_wartosc_brutto": brutto_price,

            "uwagi": f"Order: {row['Order number']}, Ticket: {row['Ticket number']}, Email: {buyer_email}",
        }

        payload = {**invoice_data, **buyer_fields, **SELLER_DATA}

        print("📦 Sending payload:")
        print(payload)

        response = requests.post(API_URL, data=payload)
        print("📨 Raw API response:")
        print(response.text)

        lines = response.text.strip().split("\n")
        if lines[0] == "1":
            print(f"✅ Invoice created for {buyer_name}. API number: {lines[1]}")
            if len(lines) >= 3:
                print(f"📎 PDF download link: {lines[2]}")
            if len(lines) >= 4:
                print(f"🌐 Online preview link: {lines[3]}")
            if len(lines) >= 5:
                print(f"📄 File name: {lines[4]}")
        else:
            print(f"❌ Failed for {buyer_name}: {lines[1]}")
