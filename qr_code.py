import qrcode
from dataclasses import dataclass


qr = qrcode.QRCode(
    version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,
)


@dataclass
class QR:
    uqr: int = 1
    tp: int = 1
    due_date: str = "20150621"
    amount: float = 1000.0
    org_nr: str = "123456-7890"
    # reference or ocr number
    reference: str = "hej"
    # BG or PG or IBAN
    account_type: str = "BG"
    account_number: str = "8103-4,9748992779"
    company_name: str = "dsreda DEMO"

    def to_data(self):
        data = {
            "uqr": self.uqr,
            "tp": self.tp,
            "nme": self.company_name,
            "cid": self.org_nr,
            "iref": self.reference,
            "ddt": self.due_date,
            "due": self.amount,
            "pt": self.account_type,
            "acc": self.account_number,
        }
        return data


#data = QR().to_data()

data = {
    "acc":  "8103-4,9748992779",
    "am": 123.23,
    "rf": "hej",
    "dt": 20200612,
    "msg": "betala faktura xxx"
}
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr1.png", "PNG")
