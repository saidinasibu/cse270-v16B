# test_smokeTest.py
# W06 - Automated User Interface Testing (Smoke Test)
# Runs against local server on http://127.0.0.1:5500 using teton/1.6

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


BASE_URL = "http://127.0.0.1:5500"
TETON = f"{BASE_URL}/teton/1.6"


class TestSmokeTest:
    def setup_method(self, method):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,720")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self, method):
        self.driver.quit()

    # 1) Logo Header and Title
    def test_test1_logo_header_and_title(self):
        self.driver.get(f"{TETON}/index.html")

        # Logo displayed
        logo_imgs = self.driver.find_elements(By.CSS_SELECTOR, ".header-logo img")
        assert len(logo_imgs) > 0

        # Heading text
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h1").text == "Teton Idaho"
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h2").text == "Chamber of Commerce"

        # Browser tab title
        assert self.driver.title == "Teton Idaho CoC"

    # 2) Home Page - Spotlights and Join Feature
    def test_test2_home_spotlights_and_join(self):
        self.driver.get(f"{TETON}/index.html")

        # Make sure page loaded
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "main")))

        # Two spotlights present
        assert len(self.driver.find_elements(By.CSS_SELECTOR, ".spotlight1")) > 0
        assert len(self.driver.find_elements(By.CSS_SELECTOR, ".spotlight2")) > 0

        # Join Us link present and navigates to join page
        join_links = self.driver.find_elements(By.LINK_TEXT, "Join Us")
        assert len(join_links) > 0
        join_links[0].click()

        # Verify join page loaded (form present + first name field present)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
        self.wait.until(EC.presence_of_element_located((By.NAME, "fname")))

    # 3) Directory Grid and List feature
    def test_test3_directory_grid_and_list(self):
        self.driver.get(f"{TETON}/directory.html")

        # Grid view
        self.driver.find_element(By.ID, "directory-grid").click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".directory-cards")))
        # Business present
        assert len(self.driver.find_elements(By.XPATH, "//p[contains(text(),'Teton Turf and Tree')]")) > 0

        # List view
        self.driver.find_element(By.ID, "directory-list").click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".directory-list")))
        assert len(self.driver.find_elements(By.XPATH, "//p[contains(text(),'Teton Turf and Tree')]")) > 0

    # 4) Join Page Data Entry (Step 1 -> Step 2)
    def test_test4_join_page_data_entry(self):
        self.driver.get(f"{TETON}/join.html")

        # Step 1: First Name present
        self.wait.until(EC.presence_of_element_located((By.NAME, "fname")))
        assert len(self.driver.find_elements(By.NAME, "fname")) > 0

        # Fill step 1
        self.driver.find_element(By.NAME, "fname").send_keys("Nasibu")
        self.driver.find_element(By.NAME, "lname").send_keys("Saidi")
        self.driver.find_element(By.NAME, "bizname").send_keys("Print On Namibia")
        self.driver.find_element(By.NAME, "biztitle").send_keys("Owner")

        # Next Step (button value is often "Next Step")
        self.driver.find_element(By.CSS_SELECTOR, "[value='Next Step']").click()

        # Step 2: Email present
        self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        assert len(self.driver.find_elements(By.NAME, "email")) > 0

    # 5) Admin Page Username/Password (invalid login error message)
    def test_test5_admin_invalid_login(self):
        self.driver.get(f"{TETON}/admin.html")

        # Username present
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        assert len(self.driver.find_elements(By.NAME, "username")) > 0

        # Enter incorrect credentials
        self.driver.find_element(By.NAME, "username").send_keys("wronguser")
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.CSS_SELECTOR, ".mysubmit").click()

        # Verify error message
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errorMessage")))
        assert self.driver.find_element(By.CSS_SELECTOR, ".errorMessage").text.strip() == "Invalid username and password."
