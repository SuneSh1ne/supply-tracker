from models.suppliers import Supplier, add_supplier


def test_supplier_creation():
    s = Supplier(1, "ООО Ромашка")
    assert s.id == 1
    assert s.name == "ООО Ромашка"
    assert str(s) == "ООО Ромашка (ID: 1)"


def test_add_supplier():
    suppliers = []
    s = add_supplier(suppliers, "ЗАО Лилия")
    assert len(suppliers) == 1
    assert s.id == 1
