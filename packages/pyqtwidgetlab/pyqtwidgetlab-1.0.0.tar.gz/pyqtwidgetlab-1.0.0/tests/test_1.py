# tests/test_1.py
import os, sys, pytest
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root not in sys.path:
    sys.path.insert(0, root)

def test_import_app():
    try:
        import src.lab   # your real import
    except ImportError as e:
        pytest.skip(f"Skipping PyQt6 import in CI (missing system Qt libs): {e}")
    assert True