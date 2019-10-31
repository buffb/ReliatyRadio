from PyQt5.QtGui import QPixmap, QImage, QIcon


def qicon_from_binary_image(icon,greyscale=False):
    try:
        image = QImage.fromData(icon)
        if greyscale:
            image = image.convertToFormat(QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        result = QIcon(pixmap)
        return True, result
    except:
        return False, None
