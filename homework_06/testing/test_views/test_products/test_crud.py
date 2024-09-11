from app.views.products.crud import ProductsStorage

class TestProductStorage:
    def test_get(self):
        storage = ProductsStorage() #pylint:disable=use-implicit-booleaness-not-comparison
        assert storage.get() == []