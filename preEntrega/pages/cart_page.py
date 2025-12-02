from selenium.webdriver.common.by import By
from .base_page import BasePage

class SecondaryHeaderContainer(BasePage):
    APP_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    
    def get_inventory_title(driver):
        return driver.find_element(*SecondaryHeaderContainer.APP_TITLE).text


    
class CartListContainer(BasePage):
    CART_LIST = (By.CSS_SELECTOR, '[data-test="cart-list"]')
    CART_QTY_LABEL = (By.CSS_SELECTOR, '[data-test="cart-quantity-label"]')
    CART_DESCRIPTION_LABEL = (By.CSS_SELECTOR, '[data-test="cart-desc-label"]')
    CART_INVENTORY_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    CART_INVENTORY_QTY = (By.CSS_SELECTOR, '[data-test="item-quantity"]')
    CART_INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    CART_DESCRIPTION = (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')
    CART_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    CART_REMOVE_BUTTON = (By.CLASS_NAME, "cart_button")
    CART_CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, '[data-test="continue-shopping"]')
    CART_CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def is_cart_list_visible(driver):
        return driver.find_element(*CartListContainer.CART_LIST).is_displayed()

    def is_cart_item_visible(driver):
        return driver.find_element(*CartListContainer.CART_INVENTORY_ITEM).is_displayed()

    def get_cart_price(driver):
        return driver.find_element(*CartListContainer.CART_PRICE).text
    
    def get_cart_inventory_item_name(driver):
        return driver.find_element(*CartListContainer.CART_INVENTORY_ITEM_NAME).text
    
    def get_cart_inventory_qty(driver):
        return driver.find_element(*CartListContainer.CART_INVENTORY_QTY).text
    
    def get_cart_description(driver):
        return driver.find_element(*CartListContainer.CART_DESCRIPTION).text

    def get_items_count(driver):
        return len(driver.find_elements(*CartListContainer.CART_LIST))

    def click_remove_from_cart_by_index(driver, index=0):
        buttons = driver.find_elements(*CartListContainer.CART_REMOVE_BUTTON)
        buttons[index].click()

    def click_continue_shopping_button(driver):
        return driver.find_element(*CartListContainer.CART_CONTINUE_SHOPPING_BUTTON).click()
    
    def click_checkout_button(driver):
        return driver.find_element(*CartListContainer.CART_CHECKOUT_BUTTON).click()