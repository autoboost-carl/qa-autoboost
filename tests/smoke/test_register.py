import pytest 
import allure
from playwright.sync_api import Page
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from faker import Faker

faker = Faker()

@pytest.fixture
def user_data():
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "telephone": faker.phone_number(),
        "fax": faker.numerify(text='##########'),
        "company": faker.company(),
        "address_1": faker.street_address(),
        "address_2": faker.secondary_address(),
        "city": faker.city(),
        "region": "California",
        "zipcode": faker.postcode(),
        "country": "United States",
        "login_name": f"user_{faker.random_number(digits=5)}",
        "password": "Test12345!",
        "newsletter": True
    }

@allure.feature("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_successful_registration_all_fields(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    login_page = LoginPage(page)

    with allure.step("Navigate to user registration"):
        login_page.navigate_to_login()
        register_page.click_continue_button()

    with allure.step("Fill every field on the form"):
        # Fill form with faker data
        register_page.register_user(user_data)

    with allure.step("Verify registration was successful"):
        # Verify registration was successful
        register_page.assert_registration_successful()

    print("User registration successful with generated data.")

@allure.feature("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_registration_without_mandatory_fields(page: Page, user_data: dict):
    register_page = RegisterPage(page)

    with allure.step("Navigate to user registration form"):
        register_page.navigate_to_register()

    with allure.step("Fill only non-mandatory fields"):
        # Fill only non-mandatory fields
        register_page.telephone_input.fill(user_data["telephone"])
        register_page.fax_input.fill(user_data["fax"])
        register_page.company_input.fill(user_data["company"])
        register_page.address_2_input.fill(user_data["address_2"])
        register_page.newsletter_yes_radio.check()
        register_page.agree_to_privacy_policy()
        register_page.click_continue_button()

    with allure.step("# Verify error messages for missing mandatory fields"):
        # Verify error messages for missing mandatory fields
        register_page.is_error_displayed()
        errors = register_page.get_error_message_text()
        register_page.assert_error_displayed()
        messages = [m.strip() + "!" for m in errors.split("!") if m.strip()]
        print("❌ Validation errors:")
        for m in messages:
            print(f"- {m}")

@allure.feature("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_registration_without_privacy_policy_agreement(page: Page, user_data: dict):
    register_page = RegisterPage(page)

    with allure.step("Navigate to user registration form"):
        register_page.navigate_to_register()

    with allure.step("Select country dropdown to enable the region dropdown"):
        # Select country first to load regions
        register_page.country_dropdown.select_option(label=user_data["country"])
        page.wait_for_load_state("domcontentloaded")  # Wait for regions to load
        register_page.region_dropdown.select_option(label=user_data["region"])

    with allure.step("Fill all input fields"):
        # Fill form without agreeing to privacy policy
        register_page.first_name_input.fill(user_data["first_name"])
        register_page.last_name_input.fill(user_data["last_name"])
        register_page.email_input.fill(user_data["email"])
        register_page.address_1_input.fill(user_data["address_1"])
        register_page.city_input.fill(user_data["city"])
        register_page.zipcode_input.fill(user_data["zipcode"])
        register_page.login_name_input.fill(user_data["login_name"])
        register_page.password_input.fill(user_data["password"])
        register_page.confirm_password_input.fill(user_data["password"])
    
    with allure.step("Check Yes or No to receive the newsletter"):
        if user_data["newsletter"]:
            register_page.newsletter_yes_radio.check()
        else:
            register_page.newsletter_no_radio.check()
    
    with allure.step("Don't check the privacy policy agreement and finish the user registration"):
        # Do not check privacy policy agreement
        register_page.click_continue_button()

    with allure.step("Verify you get an error"):
        # Verify error message is displayed
        register_page.assert_privacy_policy_error_displayed()

    print("Registration without agreeing to privacy policy displayed error as expected.")

@allure.feature("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_registration_with_mismatched_passwords(page: Page, user_data: dict):
    register_page = RegisterPage(page)

    with allure.step("Navigate to user registration form"):
        register_page.navigate_to_register()
    
    with allure.step("Select country dropdown to enable the region dropdown"):
        # Select country first to load regions
        register_page.country_dropdown.select_option(label=user_data["country"])
        page.wait_for_load_state("domcontentloaded")  # Wait for regions to load
        register_page.region_dropdown.select_option(label=user_data["region"])

    with allure.step("Fill form with mistmatched passwords"):
        # Fill form with mismatched passwords
        register_page.first_name_input.fill(user_data["first_name"])
        register_page.last_name_input.fill(user_data["last_name"])
        register_page.email_input.fill(user_data["email"])
        register_page.address_1_input.fill(user_data["address_1"])
        register_page.city_input.fill(user_data["city"])
        register_page.zipcode_input.fill(user_data["zipcode"])
        register_page.login_name_input.fill(user_data["login_name"])
        register_page.password_input.fill(user_data["password"]) # Password
        register_page.confirm_password_input.fill("DifferentPassword123!") # Different password
    

    with allure.step("Check Yes or No to receive the newsletter"):
        if user_data["newsletter"]:
            register_page.newsletter_yes_radio.check()
        else:
            register_page.newsletter_no_radio.check()
    
    with allure.step("Agree to the privacy policy and finish user registration"):
        register_page.agree_to_privacy_policy()
        register_page.click_continue_button()

    with allure.step("Verify you get an error for mismatched passwords"): 
        # Verify error message for mismatched passwords is displayed
        register_page.is_error_displayed()
        err = register_page.get_error_message_text()
        register_page.assert_error_displayed()

    print(err)

@allure.feature("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_registration_with_existing_email(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    login_page = LoginPage(page)

    with allure.step("Navigate to user registration form"):
        register_page.navigate_to_register()

    with allure.step("Register a user to ensure the email exists"):
        # First, register a user to ensure the email exists
        register_page.register_user(user_data)
        register_page.assert_registration_successful()

    with allure.step("Logout before attempting to register a new user"):
        # Logout before attempting to register again
        login_page.logout()
        page.wait_for_load_state("networkidle")

    with allure.step("Navigate to user registration form"):
        register_page.navigate_to_register()

    with allure.step("Try to register a new user with the same email"):
        # Now, attempt to register again with the same email
        # Select country first to load regions
        register_page.country_dropdown.select_option(label=user_data["country"])
        page.wait_for_load_state("domcontentloaded")  # Wait for regions to load
        register_page.region_dropdown.select_option(label=user_data["region"])
        # Fill every input field
        register_page.first_name_input.fill(user_data["first_name"])
        register_page.last_name_input.fill(user_data["last_name"])
        register_page.email_input.fill(user_data["email"])  # Same email as before
        register_page.address_1_input.fill(user_data["address_1"])
        register_page.city_input.fill(user_data["city"])
        register_page.zipcode_input.fill(user_data["zipcode"])
        register_page.login_name_input.fill(user_data["login_name"] + "_new")  # Different login name
        register_page.password_input.fill(user_data["password"])
        register_page.confirm_password_input.fill(user_data["password"])
    
    with allure.step("Check Yes or No to receive the newsletter"):
        if user_data["newsletter"]:
            register_page.newsletter_yes_radio.check()
        else:
            register_page.newsletter_no_radio.check()
    
    with allure.step("Agree to the privacy policy and finish user registration"):
        register_page.agree_to_privacy_policy()
        register_page.click_continue_button()

    with allure.step("Verify you get an error for existing user"): 
        # Verify error message for existing email is displayed
        register_page.is_error_displayed()
        err = register_page.get_error_message_text()
        register_page.assert_error_displayed()

    print(err)
