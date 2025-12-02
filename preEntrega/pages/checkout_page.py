from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from preEntrega.utils.helpers import wait_for_visibility
from .base_page import BasePage

class SecondaryHeaderContainer(BasePage):
    APP_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    
    def get_inventory_title(driver):
        return driver.find_element(*SecondaryHeaderContainer.APP_TITLE).text


    
class checkoutStepOnePage(BasePage):
    CHECKOUT_FIRST_NAME_FIELD = (By.CSS_SELECTOR, '[data-test="firstName"]')
    CHECKOUT_LAST_NAME_FIELD = (By.CSS_SELECTOR, '[data-test="lastName"]')
    CHECKOUT_POSTAL_CODE_FIELD = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CHECKOUT_CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
    CHECKOUT_ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def fill_checkout_form(driver):
        driver.find_element(*checkoutStepOnePage.CHECKOUT_FIRST_NAME_FIELD).send_keys("Flavio")
        driver.find_element(*checkoutStepOnePage.CHECKOUT_LAST_NAME_FIELD).send_keys("Carracedo")
        driver.find_element(*checkoutStepOnePage.CHECKOUT_POSTAL_CODE_FIELD).send_keys("1440")
    
    def get_checkout_continue_button(driver):
        return driver.find_element(*checkoutStepOnePage.CHECKOUT_CONTINUE_BUTTON).is_displayed()
    
    def get_checkout_error_message(driver):
        return driver.find_element(*checkoutStepOnePage.CHECKOUT_ERROR_MESSAGE).text

    def click_continue_button(driver):
        return driver.find_element(*checkoutStepOnePage.CHECKOUT_CONTINUE_BUTTON).click()

class checkoutStepTwoPage(BasePage):
    CHECKOUT_PAYMENT_INFO_LABEL = (By.CSS_SELECTOR, '[data-test="payment-info-label"]')
    CHECKOUT_PAYMENT_INFO_VALUE = (By.CSS_SELECTOR, '[data-test="payment-info-value"]')
    CHECKOUT_SHIPPING_INFORMATION_LABEL = (By.CSS_SELECTOR, '[data-test="shipping-info-label"]')
    CHECKOUT_SHIPPING_INFORMATION_VALUE = (By.CSS_SELECTOR, '[data-test="shipping-info-value"]')
    CHECKOUT_TOTAL_INFO_LABEL = (By.CSS_SELECTOR, '[data-test="total-info-label"]')
    CHECKOUT_SUBTOTAL_LABEL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    CHECKOUT_TAX_LABEL = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    CHECKOUT_TOTAL_LABEL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    CHECKOUT_FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')


    def is_checkout_payment_info_label(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_PAYMENT_INFO_LABEL).is_displayed()

    def is_checkout_payment_info_value(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_PAYMENT_INFO_VALUE).is_displayed()

    def is_checkout_shipping_information_label(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_SHIPPING_INFORMATION_LABEL).is_displayed()
    
    def is_checkout_shipping_information_value(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_SHIPPING_INFORMATION_VALUE).is_displayed()
    
    def is_total_info_label(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_TOTAL_INFO_LABEL).is_displayed()

    def is_total_subtotal_label(driver):
            return driver.find_element(*checkoutStepTwoPage.CHECKOUT_SUBTOTAL_LABEL).is_displayed()
    
    def is_total_tax_label(driver):
            return driver.find_element(*checkoutStepTwoPage.CHECKOUT_TAX_LABEL).is_displayed()
    
    def is_total_total_label(driver):
            return driver.find_element(*checkoutStepTwoPage.CHECKOUT_TOTAL_LABEL).is_displayed()

    def click_finish_button(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_FINISH_BUTTON).click()

    # Text getters
    def get_payment_info_value(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_PAYMENT_INFO_VALUE).text

    def get_shipping_info_value(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_SHIPPING_INFORMATION_VALUE).text

    def get_subtotal_text(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_SUBTOTAL_LABEL).text

    def get_tax_text(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_TAX_LABEL).text

    def get_total_text(driver):
        return driver.find_element(*checkoutStepTwoPage.CHECKOUT_TOTAL_LABEL).text
    

class checkoutCompletePage(BasePage):
    CHECKOUT_CONGRATS_IMG = (By.CLASS_NAME, 'pony_express')
    CHECKOUT_CONGRATS_IMG_ALT = (By.CSS_SELECTOR, 'img[alt="Pony Express"]')
    CHECKOUT_COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')
    CHECKOUT_COMPLETE_TEXT = (By.CSS_SELECTOR, '[data-test="complete-text"]')
    CHECKOUT_BACK_HOME_BUTTON = (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def is_checkout_congrats_img(driver):
        return driver.find_element(*checkoutCompletePage.CHECKOUT_CONGRATS_IMG).is_displayed()
    def is_checkout_complete_header(driver):
        return driver.find_element(*checkoutCompletePage.CHECKOUT_COMPLETE_HEADER).is_displayed()
    def is_checkout_complete_text(driver):  
        return driver.find_element(*checkoutCompletePage.CHECKOUT_COMPLETE_TEXT).is_displayed()
    
    def click_back_home_button(driver):
        return driver.find_element(*checkoutCompletePage.CHECKOUT_BACK_HOME_BUTTON).click()