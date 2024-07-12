import re
from playwright.sync_api import Page, expect

def test_access_homepage(page: Page):
    page.goto("http://127.0.0.1:5000")

    expect(page).to_have_title(re.compile("Home Page"))

