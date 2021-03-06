import os
from PySide2.QtGui import QFont, QPainter, QPdfWriter, QPen
from PySide2.QtCore import QDate
from math import ceil
from domain.model import Bill, Profile
from typing import List, Generator
from collections import deque

HEADING_FONT = QFont("Times", 22)
normalFont = QFont("Times", 12)
fineFont = QFont("Times", 8)
companyFont = QFont("Times", 18)
MARGIN_PERCENT = 10

normalRowDistance = 250

MAX_LINE = 50


def generate_pdf(bill: Bill, location: str, profile: Profile) -> str:
    if not os.path.exists(location):
        os.mkdir(location)

    mod_name = bill.customer.name.replace("/", "")
    file_name = f"{bill.id}-{mod_name}.pdf"
    file_name = os.path.join(location, file_name)
    doc = QPdfWriter(file_name)

    painter = QPainter()
    painter.begin(doc)
    __print_company_name(painter, profile)
    __print_heading(painter)
    __printInformation(painter, bill, profile)
    __printSpecificationTemplate(painter, profile)
    __printSpecification(painter, bill, profile)
    painter.end()
    return file_name


def __calc_margin(painter: QPainter) -> float:
    doc = painter.device()
    return doc.width() / MARGIN_PERCENT


def __print_company_name(painter: QPainter, profile: Profile) -> None:
    painter.setFont(companyFont)
    for i, txt in enumerate(profile.company_name):
        painter.drawText(50, i * 350 + 200, txt)


def __print_heading(painter: QPainter) -> None:
    """Helper function for printing the header of the bill"""
    painter.setFont(HEADING_FONT)
    doc = painter.device()
    painter.drawText(doc.width() / 2 - 800, doc.height() / 14, "FAKTURA")


def __printInformation(painter: QPainter, bill: Bill, profile: Profile) -> None:
    """Print two columns with information about the bill"""
    doc = painter.device()
    xFirst = doc.width() / 10
    yFirst = doc.height() / 10
    xSecond = doc.width() / 2 + doc.width() / 10
    y, m, d = bill.bill_date.split("-")
    date = QDate(int(y), int(m), int(d))
    dateFormat = "yyyy-MM-dd"
    payDay = date.addDays(profile.days_to_pay)

    painter.setFont(normalFont)

    # first column
    painter.drawText(xFirst, yFirst, "Datum: " + date.toString(dateFormat))
    painter.drawText(
        xFirst, yFirst + normalRowDistance, "Fakturanummer: " + str(bill.id)
    )
    painter.drawText(
        xFirst,
        yFirst + normalRowDistance * 2,
        "Förfallodag: " + payDay.toString(dateFormat),
    )
    painter.drawText(
        xFirst, yFirst + normalRowDistance * 3, "Er Referens: " + bill.reference
    )

    # second column

    if len(bill.customer.name) > 25:
        split = bill.customer.name.rsplit(" ")
        painter.drawText(xSecond, yFirst, " ".join(split[0 : ceil(len(split) / 2)]))
        painter.drawText(
            xSecond, yFirst + normalRowDistance, " ".join(split[ceil(len(split) / 2) :])
        )
        painter.drawText(xSecond, yFirst + normalRowDistance * 2, bill.customer.address)
        painter.drawText(xSecond, yFirst + normalRowDistance * 3, bill.customer.zipcode)
    else:
        painter.drawText(xSecond, yFirst, bill.customer.name)
        painter.drawText(xSecond, yFirst + normalRowDistance, bill.customer.address)
        painter.drawText(xSecond, yFirst + normalRowDistance * 2, bill.customer.zipcode)


def __printSpecificationTemplate(painter: QPainter, profile: Profile) -> None:
    """Draw the specification of the bill"""
    # TODO: maybe shorten this function?
    # TODO: globlaize column sync with below
    doc = painter.device()
    yFirstLine = doc.height() / 3
    yThirdLine = (doc.height() / 4) * 3
    pen = QPen()
    pen.setWidth(10)

    # draw lines
    painter.setPen(pen)
    margin = __calc_margin(painter)
    painter.drawLine(margin, yFirstLine, doc.width() - margin, yFirstLine)
    painter.drawLine(
        margin,
        yFirstLine + normalRowDistance * 2,
        doc.width() - margin,
        yFirstLine + normalRowDistance * 2,
    )
    painter.drawLine(margin, yThirdLine, doc.width() - margin, yThirdLine)
    painter.drawLine(
        doc.width() - margin * 3,
        yThirdLine + normalRowDistance * 3,
        doc.width() - margin,
        yThirdLine + normalRowDistance * 3,
    )
    painter.drawLine(
        margin,
        yThirdLine + normalRowDistance * 5,
        doc.width() - margin,
        yThirdLine + normalRowDistance * 5,
    )
    # text section
    painter.setFont(normalFont)
    painter.drawText(margin, yFirstLine + normalRowDistance, " Specification")
    painter.drawText(margin * 6, yFirstLine + normalRowDistance, " Antal")
    painter.drawText(margin * 7, yFirstLine + normalRowDistance, " a kronor")
    painter.drawText(margin * 8, yFirstLine + normalRowDistance, " Totalt")

    painter.drawText(margin * 7, yThirdLine + normalRowDistance, "Summa: ")
    painter.drawText(margin * 7, yThirdLine + normalRowDistance * 2, "Moms: ")
    painter.drawText(margin * 7, yThirdLine + normalRowDistance * 4, "Totalt: ")

    painter.setFont(fineFont)
    address = profile.address.split("\n")
    painter.drawText(
        margin, yThirdLine + normalRowDistance * 6, "Adress: " + address[0]
    )

    if len(address) > 1:
        for i, a in enumerate(address[1:]):
            painter.drawText(
                margin,
                yThirdLine + normalRowDistance * (6 + i + 1),
                "             " + a,
            )

    painter.drawText(
        margin * 4, yThirdLine + normalRowDistance * 6, "Telefon: " + profile.telephone
    )
    painter.drawText(
        margin * 6, yThirdLine + normalRowDistance * 6, "Mail: " + profile.mail
    )
    painter.drawText(
        margin * 8,
        yThirdLine + normalRowDistance * 6,
        "Momsreg.nr/org.nr: " + profile.org_nr,
    )
    painter.drawText(
        margin * 8,
        yThirdLine + normalRowDistance * 7,
        "Bankgiro " + profile.bank_account,
    )
    painter.drawText(
        margin * 8,
        yThirdLine + normalRowDistance * 8,
        "Företaget innehar F-skattebevis ",
    )


def __split_too_long_words(words: List[str]) -> Generator[str, None, None]:
    words_to_process = deque(words)
    while len(words_to_process) > 0:
        word = words_to_process.popleft()
        if len(word) > MAX_LINE:
            first_part = word[:MAX_LINE]
            yield first_part + "-"
            second_part = word[MAX_LINE:]
            words_to_process.extendleft([second_part])
        else:
            yield word


def split_text(text: str) -> List[str]:
    res = []
    words = list(__split_too_long_words(text.split()))
    line = words[0]
    for word in words[1:]:
        if len(line) + len(word) + 1 > MAX_LINE:  # account for whitespace
            res.append(line)
            line = word
        else:
            line += " " + word
    res.append(line)
    return res


def __print_spec_text(painter: QPainter, y_line: int, margin: float, text: str) -> int:
    splitted_text = split_text(text)
    painter.drawText(margin, y_line, splitted_text[0])
    for t in splitted_text[1:]:
        y_line += normalRowDistance
        painter.drawText(margin, y_line, t)

    return y_line


def __printSpecification(painter: QPainter, bill: Bill, profile: Profile) -> None:
    """"""
    # TODO:  globlaize column sync with above
    doc = painter.device()
    yFirstLine = doc.height() / 3 + (normalRowDistance * 3)
    yThirdLine = (doc.height() / 4) * 3
    margin = __calc_margin(painter)
    secondCol = margin * 6
    thirdCol = margin * 7
    fourthCol = margin * 8
    painter.setFont(normalFont)

    totalSum = 0.0
    y_line = yFirstLine
    for job in bill.jobs:
        y_line = __print_spec_text(painter, y_line, margin, job.text)
        painter.drawText(secondCol, y_line, str(job.number))
        painter.drawText(thirdCol, y_line, "{:10.2f}".format(job.price))
        painter.drawText(fourthCol, y_line, "{:10.2f}".format(job.price * job.number))
        totalSum += job.price * job.number
        y_line += normalRowDistance

    painter.drawText(
        fourthCol, yThirdLine + normalRowDistance, "{:10.2f}".format(totalSum)
    )
    tax = totalSum * profile.tax
    painter.drawText(
        fourthCol, yThirdLine + normalRowDistance * 2, "{:10.2f}".format(tax)
    )
    painter.drawText(
        fourthCol, yThirdLine + normalRowDistance * 4, "{:10.2f}".format(totalSum + tax)
    )
