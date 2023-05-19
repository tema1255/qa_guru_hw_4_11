import os
import tests
import allure
from selene import browser, command, have
from selene.support.shared import browser
from selenium import webdriver
from utils import attach
from selenium.webdriver.chrome.options import Options

@allure.title('Successful fill form')
@allure.step('Fill form')
def test_student_registration_form():
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options)
    browser.config.driver = driver

    with allure.step('Open registration form'):
        browser.config.window_width = 1280
        browser.config.window_height = 768
        browser.config.hold_browser_open = True
        browser.open('https://demoqa.com/automation-practice-form')
        browser.driver.execute_script("$('footer').remove()")
        browser.driver.execute_script("$('#fixedban').remove()")

    with allure.step('fill form'):
        browser.element('#firstName').type('Artem')
        browser.element('#lastName').type('Chekanov')
        browser.element('#userEmail').type('tema-42@mail.ru')
        browser.all('[for^=gender-radio]').element_by(have.text('Male')).click()
        browser.element('#userNumber').type('9876543210')

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__year-select').send_keys('1987')
        browser.element('.react-datepicker__month-select').type('April')
        browser.element('option[value="3"]').click()
        browser.element('.react-datepicker__day--002').click()

        browser.element('#subjectsInput').type('math').press_enter().type(
            'eng'
        ).press_enter()
        browser.driver.execute_script('window.scrollTo(0,300)')

        browser.element('[for=hobbies-checkbox-1]').click()
        browser.element('[for=hobbies-checkbox-3]').click()

        browser.element('#uploadPicture').set_value(
            os.path.abspath(
                os.path.join(os.path.dirname(tests.__file__), 'resources/0.jpeg')
            )
        )

        browser.element('#currentAddress').perform(
            command.js.set_value('До востребования!')
        )
        browser.element('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text('Haryana')
        ).click()
        browser.element('#city').click()
        browser.all('[id^=react-select][id*=option]').element_by(
            have.exact_text('Karnal')
        ).click()
        browser.element('#submit').perform(command.js.click)

    with allure.step('Check form results'):
        browser.element('.table').all('td').even.should(
            have.texts(
                'Artem Chekanov',
                'tema-42@mail.ru',
                'Male',
                '9876543210',
                '02 April,1987',
                'Maths, English',
                'Sports, Music',
                '0.jpeg',
                'До востребования!',
                'Haryana Karnal',
            )
        )

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
