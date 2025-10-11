import os, pytest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
@pytest.mark.parametrize("fname", [
    "sample_invoice_1.jpg",
    "sample_invoice_2.jpg",
    "sample_invoice_3.jpg",
    "sample_invoice_4.jpg",
    "sample_invoice_5.jpg",
])
def test_analyze_various_invoices(fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        pytest.skip(f"Test file {fname} not present in tests/data")
    with open(path, "rb") as f:
        files = {"file": (fname, f, "application/octet-stream")}
        r = client.post("/analyze", files=files)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "vendor" in data and "line_items" in data and "layout" in data
    assert isinstance(data["line_items"], list)
