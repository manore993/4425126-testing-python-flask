import re
from playwright.sync_api import Page, expect

def test_access_homepage(page: Page):
    page.goto("http://127.0.0.1:5000")

    expect(page).to_have_title(re.compile("Home Page"))

def test_register_username(page: Page):
    page.goto("http://127.0.0.1:5000")
    expect(page).to_have_title(re.compile("Home Page"))

    page.get_by_role("link", name="Register", exact=True).click()
    expect(page.locator("h3")).to_contain_text(re.compile("Register User"))

    page.get_by_role("textbox", name="name").fill("Hulu")
    page.get_by_role("textbox", name="email").fill("hulu@gmail.com")
    page.get_by_role("textbox", name="password").fill("hulu4789")

    page.get_by_role("button", name="Register").last.click()
    expect(page.locator("h3")).to_contain_text(re.compile("Conversion Page"))
    