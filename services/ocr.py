from typing import List
import io
from PIL import Image
import pytesseract
try:
    import layoutparser as lp
    _LP_OK = True
except Exception:
    _LP_OK = False
from models import BBox
def load_image(file_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    return img
def ocr_with_pytesseract(img: Image.Image):
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(img)
    boxes: List[BBox] = []
    n = len(data.get("text", []))
    for i in range(n):
        t = data["text"][i]
        if not t or t.strip() == "":
            continue
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        conf_raw = data.get("conf", [None])[i]
        try:
            conf = float(conf_raw) if conf_raw is not None else None
        except:
            conf = None
        boxes.append(BBox(x1=int(x), y1=int(y), x2=int(x+w), y2=int(y+h), text=t, confidence=conf))
    return text, boxes
def ocr_with_layoutparser_tesseract(img: Image.Image):
    agent = lp.TesseractAgent(languages="eng")
    layout = agent.detect(img, return_response=True)
    blocks: List[BBox] = []
    for blk in layout:
        (x1, y1, x2, y2) = map(int, blk.block.coordinates)
        txt = getattr(blk, "text", None)
        blocks.append(BBox(x1=x1, y1=y1, x2=x2, y2=y2, text=txt, confidence=None))
    text = agent.recognize(img)
    return text, blocks
def run_ocr(file_bytes: bytes):
    img = load_image(file_bytes)
    if _LP_OK:
        try:
            text, boxes = ocr_with_layoutparser_tesseract(img)
            if text and len(text.strip()) > 5:
                return text, boxes
        except Exception:
            pass
    return ocr_with_pytesseract(img)
