import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import os

class TestWebApp(unittest.TestCase):
    def setUp(self):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('http://localhost:5000')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def clear_database(self):
        """Clear the database to ensure a clean state for testing"""
        if os.path.exists('data.db'):
            conn = sqlite3.connect('data.db')
            conn.execute('DELETE FROM users')
            conn.commit()
            conn.close()

    def test_1_page_title(self):
        """Test if the page title is correct"""
        self.assertEqual(self.driver.title, 'Simple User List')

    def test_2_header_content(self):
        """Test if the header contains the correct information"""
        header = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'header-box'))
        )
        self.assertIn('Assignment 2', header.text)
        self.assertIn('Alyan Abbas', header.text)
        self.assertIn('FA21-BDS-005', header.text)

    def test_3_add_user(self):
        """Test adding a new user"""
        self.clear_database()  # Clear database before test
        input_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, 'name'))
        )
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        
        input_field.send_keys('Test User')
        submit_button.click()
        
        # Wait for the new user to appear in the list
        user_list = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )
        self.assertIn('Test User', user_list.text)

    def test_4_empty_input_validation(self):
        """Test form validation for empty input"""
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()
        
        # The form should not submit and the page should remain the same
        self.assertEqual(self.driver.current_url, 'http://localhost:5000/')

    def test_5_multiple_users(self):
        """Test adding multiple users"""
        self.clear_database()  # Clear database before test
        test_users = ['User 1', 'User 2', 'User 3']
        
        for user in test_users:
            # Wait for and find fresh elements each time
            input_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'name'))
            )
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            
            input_field.clear()
            input_field.send_keys(user)
            submit_button.click()
            
            # Wait for the page to update
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
            )
        
        # Verify all users are in the list
        user_list = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )
        for user in test_users:
            self.assertIn(user, user_list.text)

    def test_6_form_elements_present(self):
        """Test if all form elements are present"""
        input_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, 'name'))
        )
        submit_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        self.assertTrue(input_field.is_displayed())
        self.assertTrue(submit_button.is_displayed())

    def test_7_bootstrap_styles(self):
        """Test if Bootstrap styles are properly loaded"""
        header = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'header-box'))
        )
        card = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card'))
        )
        
        # Check if the elements have the expected classes
        self.assertIn('header-box', header.get_attribute('class'))
        self.assertIn('card', card.get_attribute('class'))
        self.assertIn('shadow', card.get_attribute('class'))

    def test_8_responsive_design(self):
        """Test responsive design elements"""
        container = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'container'))
        )
        row = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row'))
        )
        col = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-md-6'))
        )
        
        self.assertTrue(container.is_displayed())
        self.assertTrue(row.is_displayed())
        self.assertTrue(col.is_displayed())

    def test_9_empty_state(self):
        """Test empty state message"""
        self.clear_database()  # Clear database before test
        self.driver.refresh()  # Refresh the page to show empty state
        
        # First, check if the list group is present
        list_group = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )
        
        # Then check if it contains the empty state message
        self.assertIn('No users yet', list_group.text)

    def test_10_form_submission(self):
        """Test form submission and page reload"""
        self.clear_database()  # Clear database before test
        
        # Find and fill the input field
        input_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, 'name'))
        )
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        
        input_field.send_keys('Test User')
        submit_button.click()
        
        # Wait for the page to reload and the list group to be present
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )
        
        # Wait for and find a fresh input field after page reload
        new_input_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, 'name'))
        )
        
        # Check if the input field is cleared after submission
        self.assertEqual(new_input_field.get_attribute('value'), '')

if __name__ == '__main__':
    unittest.main() 