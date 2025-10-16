import logging
from preEntrega.pages.inventory_page import InventoryContainer
from preEntrega.pages.inventory_page import HeaderContainer
from preEntrega.pages.login_page import LoginPage


def test_navigation_flow(driver, caplog, username="standard_user", password="secret_sauce"):
    caplog.set_level(logging.INFO)
    page = LoginPage(driver)
    page.open_login_page()
    page.login(username, password)
    
    logging.getLogger().info(f"Assert: verificar que el logo de la app es visible")
    assert HeaderContainer.is_app_logo_visible(driver), "El logo de la app no es visible"

    logging.getLogger().info(f"Assert: verificar que el menú lateral es visible")
    assert HeaderContainer.is_side_drawer_menu_visible(driver), "El menú lateral no es visible"

    logging.getLogger().info(f"Assert: verificar que '/inventory.html' está en {driver.current_url}")
    assert "/inventory.html" in driver.current_url, "No se navegó a /inventory.html"

    logging.getLogger().info(f"Assert: verificar que el título del inventario es 'Products' -> '{HeaderContainer.get_inventory_title(driver)}'")
    assert HeaderContainer.get_inventory_title(driver) == "Products", "Título de inventario incorrecto"

    logging.getLogger().info(f"Assert: verificar que hay elementos en la lista de inventario")   
    assert InventoryContainer.get_items_count(driver) > 0, "No se encontraron elementos en la lista de inventario"

    logging.getLogger().info(f"Assert: verificar que la lista de inventario es visible")
    assert InventoryContainer.is_inventory_list_visible(driver), "La lista de inventario no es visible"

    logging.getLogger().info(f"Assert: verificar que el precio del primer ítem es '$29.99' -> '{InventoryContainer.get_inventory_price(driver)}'")
    assert InventoryContainer.get_inventory_price(driver) == "$29.99", "Precio del primer ítem incorrecto"

    logging.getLogger().info(f"Assert: verificar que el nombre del primer ítem es 'Sauce Labs Backpack' -> '{InventoryContainer.get_inventory_item_name(driver)}'")
    assert InventoryContainer.get_inventory_item_name(driver) == "Sauce Labs Backpack", "Nombre del primer ítem incorrecto"
    