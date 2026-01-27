import pytest 
from playwright.sync_api import Page
from pages.register_page import RegisterPage
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

@pytest.mark.smoke
def test_successful_registration_all_fields(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    register_page.navigate_to_register()

    # Fill form with faker data
    register_page.register_user(user_data)

    # Verify registration was successful
    register_page.assert_registration_successful()

    print("User registration successful with generated data.")

@pytest.mark.smoke
def test_registration_without_mandatory_fields(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    register_page.navigate_to_register()

    # Fill only non-mandatory fields
    register_page.telephone_input.fill(user_data["telephone"])
    register_page.fax_input.fill(user_data["fax"])
    register_page.company_input.fill(user_data["company"])
    register_page.address_2_input.fill(user_data["address_2"])
    register_page.newsletter_yes_radio.check()
    register_page.agree_to_privacy_policy()
    register_page.click_continue_button()

    # Verify error messages for missing mandatory fields
    register_page.is_error_displayed()
    err = register_page.get_error_message_text()
    register_page.assert_error_displayed()
    print(err)

@pytest.mark.smoke
def test_registration_without_privacy_policy_agreement(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    register_page.navigate_to_register()

    # Fill form without agreeing to privacy policy
    register_page.first_name_input.fill(user_data["first_name"])
    register_page.last_name_input.fill(user_data["last_name"])
    register_page.email_input.fill(user_data["email"])
    register_page.telephone_input.fill(user_data["telephone"])
    register_page.fax_input.fill(user_data["fax"])
    register_page.company_input.fill(user_data["company"])
    register_page.address_1_input.fill(user_data["address_1"])
    register_page.address_2_input.fill(user_data["address_2"])
    register_page.city_input.fill(user_data["city"])
    
    # Select country first to load regions
    register_page.country_dropdown.select_option(label=user_data["country"])
    page.wait_for_timeout(2000)  # Wait for regions to load
    register_page.region_dropdown.select_option(label=user_data["region"])
    register_page.zipcode_input.fill(user_data["zipcode"])
    register_page.login_name_input.fill(user_data["login_name"])
    register_page.password_input.fill(user_data["password"])
    register_page.confirm_password_input.fill(user_data["password"])
    
    if user_data["newsletter"]:
        register_page.newsletter_yes_radio.check()
    else:
        register_page.newsletter_no_radio.check()
    
    # Do not check privacy policy agreement
    register_page.click_continue_button()

    # Verify error message is displayed
    register_page.assert_privacy_policy_error_displayed()

    print("Registration without agreeing to privacy policy displayed error as expected.")

@pytest.mark.smoke
def test_registration_with_mismatched_passwords(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    register_page.navigate_to_register()

    # Fill form with mismatched passwords
    register_page.first_name_input.fill(user_data["first_name"])
    register_page.last_name_input.fill(user_data["last_name"])
    register_page.email_input.fill(user_data["email"])
    register_page.telephone_input.fill(user_data["telephone"])
    register_page.fax_input.fill(user_data["fax"])
    register_page.company_input.fill(user_data["company"])
    register_page.address_1_input.fill(user_data["address_1"])
    register_page.address_2_input.fill(user_data["address_2"])
    register_page.city_input.fill(user_data["city"])
    
    # Select country first to load regions
    register_page.country_dropdown.select_option(label=user_data["country"])
    page.wait_for_timeout(2000)  # Wait for regions to load
    register_page.region_dropdown.select_option(label=user_data["region"])
    register_page.zipcode_input.fill(user_data["zipcode"])
    register_page.login_name_input.fill(user_data["login_name"])
    register_page.password_input.fill(user_data["password"])
    register_page.confirm_password_input.fill("DifferentPassword123!")
    
    if user_data["newsletter"]:
        register_page.newsletter_yes_radio.check()
    else:
        register_page.newsletter_no_radio.check()
    
    register_page.agree_to_privacy_policy()
    register_page.click_continue_button()

    # Verify error message for mismatched passwords is displayed
    register_page.is_error_displayed()
    err = register_page.get_error_message_text()
    register_page.assert_error_displayed()

    print(err)

def test_registration_with_existing_email(page: Page, user_data: dict):
    register_page = RegisterPage(page)
    register_page.navigate_to_register()

    # First, register a user to ensure the email exists
    register_page.register_user(user_data)
    register_page.assert_registration_successful()

    # Logout before attempting to register again
    register_page.logout()
    page.wait_for_timeout(1000)

    # Now, attempt to register again with the same email
    register_page.navigate_to_register()
    register_page.first_name_input.fill(user_data["first_name"])
    register_page.last_name_input.fill(user_data["last_name"])
    register_page.email_input.fill(user_data["email"])  # Same email
    register_page.telephone_input.fill(user_data["telephone"])
    register_page.fax_input.fill(user_data["fax"])
    register_page.company_input.fill(user_data["company"])
    register_page.address_1_input.fill(user_data["address_1"])
    register_page.address_2_input.fill(user_data["address_2"])
    register_page.city_input.fill(user_data["city"])
    
    # Select country first to load regions
    register_page.country_dropdown.select_option(label=user_data["country"])
    page.wait_for_timeout(2000)  # Wait for regions to load
    register_page.region_dropdown.select_option(label=user_data["region"])
    register_page.zipcode_input.fill(user_data["zipcode"])
    register_page.login_name_input.fill(user_data["login_name"] + "_new")  # Different login name
    register_page.password_input.fill(user_data["password"])
    register_page.confirm_password_input.fill(user_data["password"])
    
    if user_data["newsletter"]:
        register_page.newsletter_yes_radio.check()
    else:
        register_page.newsletter_no_radio.check()
    
    register_page.agree_to_privacy_policy()
    register_page.click_continue_button()

    # Verify error message for existing email is displayed
    register_page.is_error_displayed()
    err = register_page.get_error_message_text()
    register_page.assert_error_displayed()

    print(err)
