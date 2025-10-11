import re
from typing import Dict, Any, List, Optional
from models import InvoiceResponse, LineItem, BBox
from config import settings
_GROQ_AVAILABLE = True
try:
    from groq import Groq
except Exception:
    _GROQ_AVAILABLE = False
SYSTEM_PROMPT = ("You are a precise invoice extraction agent. "
    "Given raw OCR text from an invoice, return a strict JSON that matches the schema: "
    "{vendor, invoice_number, invoice_date, currency, subtotal, tax, total, line_items:[{description, quantity, unit_price, amount}]}."
    "Use 'USD' if currency symbol is $. Keep numbers as numeric, not strings. If a field is missing, infer carefully or set empty string/0."
)
def _regex_find(pattern: str, text: str, flags=re.I) -> Optional[str]:
    m = re.search(pattern, text, flags)
    if not m:
        return None
    return m.group(m.lastindex or 1).strip()
def heuristic_parse(ocr_text: str) -> Dict[str, Any]:
    currency = "USD" if "$" in ocr_text else ("EUR" if "€" in ocr_text else ("GBP" if "£" in ocr_text else "BDT" if "৳" in ocr_text else "USD"))
    invoice_no = _regex_find(r"(?:invoice\s*(?:#|no\.?|number)\s*[:#]?\s*)([A-Z0-9-]+)", ocr_text)         or _regex_find(r"([A-Z]{2,}\d{3,})", ocr_text) or ""
    date = _regex_find(r"(?:invoice\s*date|date)\s*:?\s*([0-9]{1,2}[\/-][0-9]{1,2}[\/-][0-9]{2,4})", ocr_text)         or _regex_find(r"(?:invoice\s*date|date)\s*:?\s*([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})", ocr_text)         or ""
    vendor = (_regex_find(r"^(.+)$", ocr_text, flags=re.M) or "Unknown Vendor")
    amounts = re.findall(r"([0-9]+[\,\.][0-9]{2})", ocr_text)
    def to_float(s): return float(s.replace(",","")) if s else 0.0
    total = to_float(amounts[-1]) if amounts else 0.0
    tax = 0.0
    subtotal = max(0.0, total - tax)
    line_items = [dict(description="Items", quantity=1, unit_price=subtotal, amount=subtotal)]
    return dict(vendor=vendor, invoice_number=invoice_no, invoice_date=date, currency=currency,
                subtotal=subtotal, tax=tax, total=total, line_items=line_items)
def parse_with_groq(ocr_text: str) -> Dict[str, Any]:
    if not _GROQ_AVAILABLE or not settings.GROQ_API_KEY:
        return heuristic_parse(ocr_text)
    client = Groq(api_key=settings.GROQ_API_KEY)
    resp = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": ocr_text },
        ],
        temperature=0.0,
    )
    content = resp.choices[0].message.content.strip()
    import json, re as _re
    try:
        data = json.loads(content)
    except Exception:
        m = _re.search(r"\{.*\}", content, _re.S)
        data = json.loads(m.group(0)) if m else heuristic_parse(ocr_text)
    return data
def compose_response(ocr_text: str, layout_boxes: List[BBox]) -> InvoiceResponse:
    parsed = parse_with_groq(ocr_text)
    lis = []
    for li in parsed.get("line_items", []):
        lis.append(LineItem(
            description=str(li.get("description", "")),
            quantity=float(li.get("quantity", 0)),
            unit_price=float(li.get("unit_price", 0)),
            amount=float(li.get("amount", 0)),
            bbox=None,
            confidence=None
        ))
    resp = InvoiceResponse(
        vendor=str(parsed.get("vendor", "")),
        invoice_number=str(parsed.get("invoice_number", "")),
        invoice_date=str(parsed.get("invoice_date", "")),
        currency=str(parsed.get("currency", "USD")),
        subtotal=float(parsed.get("subtotal", 0)),
        tax=float(parsed.get("tax", 0)),
        total=float(parsed.get("total", 0)),
        line_items=lis,
        layout=layout_boxes,
        ocr_text=ocr_text,
        confidence_overall=None
    )
    return resp
