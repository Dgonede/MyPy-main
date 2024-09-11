from app.views.products.crud import ProductsStorage

#pylint:disable=(use-implicit-booleaness-not-comparison)
class TestProductStorage:
    def test_get(self):
        storage = ProductsStorage()
        assert storage.get() == []