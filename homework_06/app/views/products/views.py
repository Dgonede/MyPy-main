from http import HTTPStatus
from flask import Blueprint, redirect, request, url_for
from flask import render_template
from werkzeug.exceptions import NotFound
from .models import ProductCreate
from .crud import storage

products_app = Blueprint(
    "products_app",
    __name__,
    url_prefix="/products",
)

@products_app.route("/", endpoint="index")
def get_product_list():
    return render_template(
        "products/index.html",
        products=storage.get(),
        )


@products_app.route("/add/", endpoint="add", methods=["GET", "POST"])
def add_product():
    if request.method != "POST":
        return render_template("products/add.html")

    product_name = request.form.get("product-name") or "Default"
    product_price = request.form.get("product-price") or 0

    product = storage.create(
        product_create=ProductCreate(
            name=product_name,
            price=product_price,
        ),
    )
    new_url = url_for("products_app.details", product_id=product.id)
    return redirect(new_url, code=HTTPStatus.SEE_OTHER)


@products_app.route("/<int:product_id>/", endpoint="details")
def get_products_by_id(product_id):
    product = storage.get_by_id(product_id)
    if not product:
        raise NotFound(f"product # {product_id} not found")
    return render_template(
        "products/details.html",
        product=product,
        )