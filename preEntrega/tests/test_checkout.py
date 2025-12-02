import logging

import pytest

from preEntrega.data.data_login import valid_login
from preEntrega.pages.login_page import LoginPage

from preEntrega.pages.inventory_page import InventoryContainer
from preEntrega.pages.inventory_page import HeaderContainer

from preEntrega.pages.cart_page import CartListContainer

from preEntrega.pages.checkout_page import checkoutStepOnePage
from preEntrega.pages.checkout_page import checkoutStepTwoPage
from preEntrega.pages.checkout_page import checkoutCompletePage


@pytest.mark.parametrize("username,password", valid_login, ids=[u for (u, _) in valid_login])
def test_checkout_step_one_validation(driver, caplog, username, password):
    caplog.set_level(logging.INFO)
    LoginPage(driver).open_login_page()
    LoginPage(driver).login(username, password)

    logging.getLogger().info("Clicking the 'Add to cart' button for first item")
    InventoryContainer.click_add_to_cart_by_index(driver, index=0)

    HeaderContainer.click_your_cart_button(driver)
    logging.getLogger().info("Opened cart")

    CartListContainer.click_checkout_button(driver)
    logging.getLogger().info("Navigated to checkout step one")

    logging.getLogger().info("Assert: title is 'Checkout: Your Information'")
    assert HeaderContainer.get_inventory_title(driver) == "Checkout: Your Information"

    # Attempt continue without filling form
    checkoutStepOnePage.click_continue_button(driver)
    logging.getLogger().info("Clicked continue with empty fields")
    error_message = checkoutStepOnePage.get_checkout_error_message(driver)
    logging.getLogger().info(f"Checkout error message: {error_message}")
    assert error_message == "Error: First Name is required"


@pytest.mark.parametrize("username,password", valid_login, ids=[u for (u, _) in valid_login])
def test_checkout_step_two_overview(driver, caplog, username, password):
    caplog.set_level(logging.INFO)
    LoginPage(driver).open_login_page()
    LoginPage(driver).login(username, password)

    logging.getLogger().info("Clicking the 'Add to cart' button for first item")
    InventoryContainer.click_add_to_cart_by_index(driver, index=0)

    HeaderContainer.click_your_cart_button(driver)
    logging.getLogger().info("Opened cart")

    CartListContainer.click_checkout_button(driver)
    logging.getLogger().info("Navigated to checkout step one")

    logging.getLogger().info("Assert: title is 'Checkout: Your Information'")
    assert HeaderContainer.get_inventory_title(driver) == "Checkout: Your Information"

    # Fill form and continue to step two
    logging.getLogger().info("Filling checkout information")
    checkoutStepOnePage.fill_checkout_form(driver)
    checkoutStepOnePage.click_continue_button(driver)
    logging.getLogger().info("Navigated to checkout step two")

    logging.getLogger().info("Assert: title is 'Checkout: Overview'")
    assert HeaderContainer.get_inventory_title(driver) == "Checkout: Overview"

    logging.getLogger().info("Assert: inventory list has items")
    assert InventoryContainer.get_items_count(driver) > 0, "No items found in the inventory list"

    # Step Two detailed validations
    logging.getLogger().info("Validating payment info label & value")
    assert checkoutStepTwoPage.is_checkout_payment_info_label(driver)
    assert checkoutStepTwoPage.is_checkout_payment_info_value(driver)
    payment_value = checkoutStepTwoPage.get_payment_info_value(driver)
    logging.getLogger().info(f"Payment info value: {payment_value}")
    assert payment_value == "SauceCard #31337"

    logging.getLogger().info("Validating shipping info label & value")
    assert checkoutStepTwoPage.is_checkout_shipping_information_label(driver)
    assert checkoutStepTwoPage.is_checkout_shipping_information_value(driver)
    shipping_value = checkoutStepTwoPage.get_shipping_info_value(driver)
    logging.getLogger().info(f"Shipping info value: {shipping_value}")
    assert shipping_value == "Free Pony Express Delivery!"

    logging.getLogger().info("Validating subtotal, tax and total")
    assert checkoutStepTwoPage.is_total_subtotal_label(driver)
    subtotal_text = checkoutStepTwoPage.get_subtotal_text(driver)
    logging.getLogger().info(f"Subtotal text: {subtotal_text}")
    assert subtotal_text == "Item total: $29.99"

    assert checkoutStepTwoPage.is_total_tax_label(driver)
    tax_text = checkoutStepTwoPage.get_tax_text(driver)
    logging.getLogger().info(f"Tax text: {tax_text}")
    assert tax_text == "Tax: $2.40"

    assert checkoutStepTwoPage.is_total_total_label(driver)
    total_text = checkoutStepTwoPage.get_total_text(driver)
    logging.getLogger().info(f"Total text: {total_text}")
    assert total_text == "Total: $32.39"

    # Finish checkout
    logging.getLogger().info("Clicking Finish button")
    checkoutStepTwoPage.click_finish_button(driver)
    logging.getLogger().info("Navigated to Complete page")

    # Final assertions
    logging.getLogger().info("Validating completion page elements")

    assert checkoutCompletePage.is_checkout_congrats_img(driver)
    assert checkoutCompletePage.is_checkout_complete_header(driver)
    assert checkoutCompletePage.is_checkout_complete_text(driver)

    logging.getLogger().info("Assert: title is 'Checkout: Complete!'")
    assert HeaderContainer.get_inventory_title(driver) == "Checkout: Complete!"

    logging.getLogger().info("Clicking Back Home button")
    checkoutCompletePage.click_back_home_button(driver)