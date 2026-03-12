from typing import Union


class CaptchaSolver:
    def solve(self, image_bytes: Union[bytes, bytearray]) -> str:
        raise NotImplementedError(
            "Integrate a captcha solving service (e.g. 2captcha, anti-captcha, "
            "or a local OCR model) and implement this method."
        )
