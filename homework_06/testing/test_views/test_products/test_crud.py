from app.views.products.crud import ProductsStorage

class TestProductStorage:
    def test_get(self):
        storage = ProductsStorage()
        assert storage.get() == []