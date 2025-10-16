import logging
from preEntrega.pages.login_page import LoginPage
from preEntrega.pages.inventory_page import HeaderContainer

def test_login_success(driver, caplog):
    caplog.set_level(logging.INFO)
    logging.getLogger().info("Abrir página de login")
    LoginPage(driver).open_login_page()
    logging.getLogger().info("Haciendo login con standard_user")
    LoginPage(driver).login("standard_user", "secret_sauce")

    logging.getLogger().info(f"Assert: verificar que '/inventory.html' está en {driver.current_url}")
    assert "/inventory.html" in driver.current_url, "No se navegó a /inventory.html"

    logging.getLogger().info(f"Assert: titulo contiene 'Swag Labs' -> '{driver.title}'")
    assert "Swag Labs" in driver.title, "Título incorrecto"

    logging.getLogger().info(f"Assert: titulo contiene 'Products' -> '{HeaderContainer.get_inventory_title(driver)}'")
    assert HeaderContainer.get_inventory_title(driver) == "Products", "Título de inventario incorrecto"



