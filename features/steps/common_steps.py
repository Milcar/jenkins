import os

from behave import given, when

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"


def prepare_browser(context):
    """Abre la tienda, reinicia su estado y prepara los objetos de página."""
    if not hasattr(context, 'driver') or context.driver is None:
        context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)
    context.driver.execute_script("""
        estado.carrito = [];
        estado.cuponAplicado = null;
        renderCatalogo();
        mostrarVista('catalogo');
    """)
    context.catalog = CatalogPage(context.driver)
    context.cart = CartPage(context.driver)
    context.checkout = CheckoutPage(context.driver)


@when('abro el carrito')
def step_impl(context):
    """Abre la vista del carrito."""
    context.catalog.open_cart()


@given('tengo un producto en el carrito')
def step_impl(context):
    """Prepara la tienda con un producto agregado y el carrito abierto."""
    prepare_browser(context)
    context.catalog.add_product('Laptop Pro 15')
    context.catalog.open_cart()


@given('tengo varios productos en el carrito')
def step_impl(context):
    """Prepara la tienda con varios productos y el carrito abierto."""
    prepare_browser(context)
    context.catalog.add_product('Laptop Pro 15')
    context.catalog.add_product('Teclado Mecánico')
    context.catalog.open_cart()


@given('el carrito está vacío')
def step_impl(context):
    """Prepara la tienda con el carrito vacío."""
    prepare_browser(context)
    context.driver.execute_script("estado.carrito = []; renderCarrito();")