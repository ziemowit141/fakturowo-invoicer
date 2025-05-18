# 🧾 fakturowo-invoicer

Generate invoices on [Fakturowo.pl](https://fakturowo.pl) using a CSV input file and the official API.

---

## 📦 CSV Format

The script reads a file named `invoicer.csv` with the following headers:

```csv
Order number,Ticket number,First Name,Last Name,Email,Twitter,Company,NIP,Title,Featured,Ticket title,Ticket venue,Access code,Discount,Price,Currency,Number of tickets,Paid by (name),Paid by (email),Paid date (UTC),Checkin Date (UTC),Ticket Price Paid
````

### Example:

```csv
CNCFE25226477,CNCFA25249035,Patryk,Gołębiewski,maciej@example.com,,VirtusLab,6751523860,Cloud Engineer,,KCD 2025 Ticket,In-person,,,1000,USD,1,Patryk Gołębiewski,maciej@example.com,2025-03-19 18:35:45+00:00,,1000
```

---

## 🚀 Usage

1. Install dependencies (Python 3 required):

   ```bash
   pip install requests
   ```

2. Add your `API_ID` inside `invoicer.py`.

3. Place your `invoicer.csv` file in the same directory.

4. Run the script:

   ```bash
   ./invoicer.py
   ```

You’ll see invoice confirmation messages along with download and preview URLs.

---

## ⚠️ Important: Company vs. Private Person

Fakturowo requires the following when issuing invoices:
Company invoices (for Polish buyers) must include a valid NIP (tax ID).
If no NIP is provided, the invoice is treated as a private individual.
In that case:
The Company field is ignored.
First name and last name must be provided.
Make sure your CSV is filled accordingly based on buyer type.
