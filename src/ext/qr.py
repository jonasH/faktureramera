import qrcode
from dataclasses import dataclass
from qrcode.image.pil import PilImage
from PySide2 import QtGui
from PIL.ImageQt import ImageQt


@dataclass
class QR:
    uqr: int = 1
    tp: int = 1
    due_date: str = "20150621"
    amount: float = 3407.0
    org_nr: str = "123456-7890"
    # reference or ocr number
    reference: str = "130065"
    # BG or PG
    account_type: str = "BG"
    account_number: str = "123-4567"
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


def create_qr_image(qr_data: QR) -> PilImage:
    qr_creator = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    data = qr_data.to_data()
    qr_creator.add_data(data)
    qr_creator.make(fit=True)
    img = qr_creator.make_image(fill_color="black", back_color="white")
    return ImageQt(img.get_image())


if __name__ == "__main__":
    img = create_qr_image(QR())
