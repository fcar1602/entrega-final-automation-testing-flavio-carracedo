from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HeaderContainer(BasePage):
    SIDEDRAWER_MENU = (By.ID, 'react-burger-menu-btn')
    APP_LOGO = (By.CLASS_NAME, 'app_logo')
    APP_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    YOUR_CART_BUTTON = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    SHOPPING_CART_BADGE = (By.CLASS_NAME, 'btn_inventory')

    def is_app_logo_visible(driver):
        return driver.find_element(*HeaderContainer.APP_LOGO).is_displayed()
    
    def is_side_drawer_menu_visible(driver):
        return driver.find_element(*HeaderContainer.SIDEDRAWER_MENU).is_displayed()
    
    def get_inventory_title(driver):
        return driver.find_element(*HeaderContainer.APP_TITLE).text

    def click_your_cart_button(driver):
            driver.find_element(*HeaderContainer.YOUR_CART_BUTTON).click()

    def get_shopping_cart_badge_count(driver):
            return len(driver.find_element(*HeaderContainer.SHOPPING_CART_BADGE))

    
class InventoryContainer(BasePage):

    INVENTORY_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"], .inventory_item_price')
    INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"], .inventory_item_name')
    INVENTORY_LIST_ITEM = (By.CSS_SELECTOR, '[data-test="inventory-item"], .inventory_item')
    INVENTORY_ADD_TO_CART_BUTTON = (By.CLASS_NAME, 'btn_inventory')


    def click_add_to_cart_by_index(driver, index=0):
        buttons = driver.find_elements(*InventoryContainer.INVENTORY_ADD_TO_CART_BUTTON)
        buttons[index].click()


    def is_inventory_list_visible(driver):
        return driver.find_element(*InventoryContainer.INVENTORY_LIST_ITEM).is_displayed()

    def get_inventory_price(driver):
        return driver.find_element(*InventoryContainer.INVENTORY_PRICE).text

    def get_inventory_item_name(driver):
        return driver.find_element(*InventoryContainer.INVENTORY_ITEM_NAME).text

    def get_items_count(driver):
        return len(driver.find_elements(*InventoryContainer.INVENTORY_LIST_ITEM))
    
    def click_add_to_cart_button(driver):
        driver.find_element(*InventoryContainer.INVENTORY_ADD_TO_CART_BUTTON).click()