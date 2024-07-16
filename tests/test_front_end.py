import re
from playwright.sync_api import Page, expect

address = "http://127.0.0.1:5000"

def test_access_homepage(page: Page):
    page.goto(address)

    expect(page).to_have_title(re.compile("Home Page"))

def test_register_username(page: Page):
    page.goto(address)
    expect(page).to_have_title(re.compile("Home Page"))

    page.get_by_role("link", name="Register", exact=True).click()
    expect(page.locator("h3")).to_contain_text(re.compile("Register User"))

    page.get_by_role("textbox", name="name").fill("Hulu")
    page.get_by_role("textbox", name="email").fill("hulu@gmail.com")
    page.get_by_role("textbox", name="password").fill("hulu4789")

    page.get_by_role("button", name="Register").last.click()
    expect(page.locator("h3")).to_contain_text(re.compile("Conversion Page"))

def test_login(page: Page):
    page.goto(address)
    expect(page).to_have_title(re.compile("Home Page"))

    page.get_by_role("link", name="Login").click()
    expect(page.locator("h3")).to_contain_text(re.compile("Login User"))

    page.get_by_role("textbox", name="email").fill("hulu@gmail.com")
    page.get_by_role("textbox", name="password").fill("hulu4789")

    page.get_by_role("button", name="Login").last.click()
    expect(page.locator("h3")).to_contain_text(re.compile("Conversion Page"))

def test_calculation_base_10_check_saving_history(page: Page):
    page.goto(address)
    expect(page).to_have_title(re.compile("Home Page"))

    page.get_by_role("link", name="Login").click()
    expect(page.locator("h3")).to_contain_text(re.compile("Login User"))

    page.get_by_role("textbox", name="email").fill("hulu@gmail.com")
    page.get_by_role("textbox", name="password").fill("hulu4789")   

    page.get_by_role("button", name="Login").last.click()
    expect(page.locator("h3").first).to_contain_text(re.compile("Conversion Page"))
    
    page.select_option('select#base',value='10')
    page.get_by_role("textbox", name="input").fill("10")
    page.get_by_role("button", name="Calculate").click()
    expect(page.locator("h3").last).to_contain_text(re.compile("Result"))
    expect(page.get_by_text("Decimal: 10")).to_contain_text(re.compile("10"))
    expect(page.get_by_text("Binary: 1010")).to_contain_text(re.compile("1010"))
    expect(page.get_by_text("Hexadecimal: A")).to_contain_text(re.compile("A"))
    
    page.get_by_role("link", name="History").click()
    expect(page.get_by_role("cell", name="Base")).to_contain_text(re.compile("Base"))
    expect(page.get_by_role("cell", name="Input")).to_contain_text(re.compile("Input"))
    expect(page.get_by_role("cell", name="Decimal", exact=True)).to_contain_text(re.compile("Decimal"))
    expect(page.get_by_role("cell", name="Binary")).to_contain_text(re.compile("Binary"))
    expect(page.get_by_role("cell", name="Hexadecimal")).to_contain_text(re.compile("Hexadecimal"))
   
    expect(page.locator("td").first).to_contain_text(re.compile("10"))
    expect(page.locator("td:nth-child(2)").first).to_contain_text(re.compile("10"))
    expect(page.locator("td:nth-child(3)").first).to_contain_text(re.compile("10"))
    expect(page.locator("td:nth-child(4)").first).to_contain_text(re.compile("1010"))
    expect(page.locator("td:nth-child(5)").first).to_contain_text(re.compile("A"))
   

def test_logout(page: Page):
    page.goto(address)
    expect(page).to_have_title(re.compile("Home Page"))

    page.get_by_role("link", name="Login").click()
    expect(page.locator("h3")).to_contain_text(re.compile("Login User"))

    page.get_by_role("textbox", name="email").fill("hulu@gmail.com")
    page.get_by_role("textbox", name="password").fill("hulu4789")

    page.get_by_role("button", name="Login").last.click()
    expect(page.locator("h3")).to_contain_text(re.compile("Conversion Page"))

    page.get_by_role("link", name="Logout").click()
    expect(page.locator("h3")).to_contain_text(re.compile("Login User"))
