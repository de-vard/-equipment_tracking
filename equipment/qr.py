import io
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter

from pyzbar.pyzbar import decode
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class PDFGenerator:
    def __init__(self, data, barcode, text):
        # создает объект байтового потока в памяти
        self.pdf_bytes = io.BytesIO()

        # создает объект Canvas из библиотеки ReportLab для генерации PDF-документов.
        self.pdf_canvas = canvas.Canvas(self.pdf_bytes, pagesize=letter)

        # Передаем id что бы с него сформировать qr-code
        self.data = data

        self.text = text

        self.barcode = barcode

    def __setattr__(self, key, value):
        """Проверяем методы на валидность"""
        if key == "barcode":
            if (not value.isdigit()) or (len(value) != 12):
                raise ValueError("Код должен состоять из 12 цифр.")
        return super().__setattr__(key, value)

    @staticmethod
    def generate_barcode_bytes(code):
        """Генерируем штрих код в байта"""
        # создает объект байтового потока в памяти
        buffer = io.BytesIO()

        # Создает объект штрих-кода формата EAN-13 с использованием ImageWriter для создания изображения
        ean = EAN13(code, writer=ImageWriter())

        # Записывает изображение штрих-кода в объект buffer
        ean.write(buffer)

        # возвращение байтового представления штрих-кода
        return buffer.getvalue()

    @staticmethod
    def generate_qr_code_bytes(data):
        """Генерируем qr код в байтах"""

        # создает объект QRCode из библиотеки qrcode
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=40, border=4,
        )

        qr.add_data(data)

        # код генерирует QR-код с определенными цветами и изменяет его размер
        qr_image = qr.make_image(fill_color='black', back_color='white').resize((100, 100))

        # создает объект байтового потока в памяти
        qr_bytes = io.BytesIO()

        # сохраняет изображение QR-кода в байтовый объект в формате PNG
        qr_image.save(qr_bytes, format='PNG')

        # Перемещение указателя в начало что бы qr читался с самого начала
        qr_bytes.seek(0)

        # Возвращает байтовое представление изображения
        return qr_bytes.getvalue()

    def add_image_to_pdf(self):
        """Добавляем qr и штрих код в PDF"""
        qr_code_bytes = self.generate_qr_code_bytes(self.data)
        barcode_bytes = self.generate_barcode_bytes(self.barcode)

        # Открываем изображения
        br_bytes = Image.open(io.BytesIO(barcode_bytes))
        qr_image = Image.open(io.BytesIO(qr_code_bytes))

        # Размеры и позиции изображений
        br_width, br_height = br_bytes.size
        qr_width, qr_height = qr_image.size

        qr_x, qr_y = 25, 680  # Позиция QR-кода
        br_x, br_y = 75, 680  # Позиция штрих-кода

        # Добавляем в PDF qr и штрих код
        self.pdf_canvas.drawInlineImage(qr_image, qr_x, qr_y, width=50, height=50 / (qr_width / qr_height))
        self.pdf_canvas.drawInlineImage(br_bytes, br_x, br_y, width=150, height=80 / (br_width / br_height))

    def add_text_to_pdf(self):
        """Добавляем текст в PDF"""
        # регистрации шрифта TrueType (TTF) в библиотеке ReportLab
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

        # устанавливаем шрифт и его размера в контексте PDF-документа
        self.pdf_canvas.setFont('Arial', 12)

        # используется для рисования строки текста в определенной позиции на странице PDF-документа
        self.pdf_canvas.drawString(25, 630, self.text)

    def close_buffers(self):
        """Закрывает буферы памяти после использования, что бы небыло утечки памяти"""
        self.pdf_bytes.close()  # закрываем буфер PDF

    def generate_pdf_bytes(self):
        self.add_image_to_pdf()
        self.add_text_to_pdf()
        self.pdf_canvas.save()
        self.pdf_bytes.seek(0)
        return self.pdf_bytes.getvalue()


class ReadingQr:
    """Чтение qr кодов"""

    def __init__(self, qr_code="image/vole.jpg"):
        self.img = decode(Image.open(qr_code))

    def get_data_from_image(self):
        return self.img[0].data.decode("utf-8")
