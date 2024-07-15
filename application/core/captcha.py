import random

from captcha.image import ImageCaptcha


def generate_captcha():
    code = str(random.randint(1000, 9999))
    captcha = ImageCaptcha()
    captcha_image = captcha.generate(code)
    return code, captcha_image