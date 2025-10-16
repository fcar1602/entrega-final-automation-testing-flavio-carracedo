import logging
from preEntrega.pages.cart_page import CartListContainer
from preEntrega.pages.inventory_page import InventoryContainer
from preEntrega.pages.inventory_page import HeaderContainer
from preEntrega.pages.login_page import LoginPage


def test_add_to_cart(driver, caplog, username="standard_user", password="secret_sauce"):
    caplog.set_level(logging.INFO)
    page = LoginPage(driver)
    page.open_login_page()
    page.login(username, password)
    

    InventoryContainer.get_items_count(driver)
    logging.getLogger().info(f"Número de ítems en inventario: {InventoryContainer.get_items_count(driver)}")

    logging.getLogger().info(f"Se hizo clic en el botón 'Agregar al carrito'")
    InventoryContainer.click_add_to_cart_by_index(driver, index=0)

    HeaderContainer.click_your_cart_button(driver)
    logging.getLogger().info(f"Se hizo clic en el botón del carrito de compras")

    CartListContainer.get_cart_inventory_qty(driver)
    logging.getLogger().info(f"Número en el badge del carrito de compras: {CartListContainer.get_cart_inventory_qty(driver)}")

    logging.getLogger().info(f"Verificando que exista un ítem en el carrito de compras")
    CartListContainer.is_cart_item_visible(driver)
    assert CartListContainer.is_cart_item_visible(driver) == True