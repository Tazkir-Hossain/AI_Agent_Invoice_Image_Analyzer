from services.parser import heuristic_parse
def test_heuristic_parse_basic():
    ocr = """
    ACME Corp
    Invoice # INV-12345
    Invoice Date: 2024-12-01
    Total: $120.00
    """
    data = heuristic_parse(ocr)
    assert data["invoice_number"] == "INV-12345"
    assert data["currency"] == "USD"
    assert data["total"] >= 120.0
