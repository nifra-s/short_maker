import time
from selenium.webdriver.common.keys import Keys

from seleniumbase import SB

def upload(path, title):
    with SB() as sb:
        sb.open("https://www.tiktok.com")
        sb.load_cookies(name="cookies.txt")
        sb.open("https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=en")
        sb.choose_file('input.jsx-399202212', path, by="css selector", timeout=None)
        sb.type('//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/span/span', title)
        delete_count = 10  # Number of times to press DELETE
        for _ in range(delete_count):
            sb.press_keys('//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/span/span', Keys.DELETE)
        sb.wait_for_element_clickable("/html/body/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[9]/button[1]", timeout=100)
        sb.click("/html/body/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[9]/button[1]")
        time.sleep(10)

        # self.uc_gui_handle_captcha(frame="iframe")
        # self.click_if_visible('button[data-testid="login-button"]', timeout=2)
        # self.click_if_visible('button[data-testid="welcome-login-button"]', timeout=2)
        #
        # self.type("#email-input", "nifras1711@gmail.com")
        #
        # self.type("#password", "mAJ;!%u)iX%3vps")
        # self.click('button:contains("Continue")')
        #
        # self.type("#prompt-textarea", "generate python code to generate to calculate sum of first 10 odd numbers")
        # self.sleep(2)

        # self.click('button[data-testid="send-button"')
        #
        # # self.assert_element('button[data-testid="copy-turn-action-button"')
        #
        # self.click_if_visible('button:contains("Reg")')
        # self.assert_element('button:contains("Copy code")', timeout=10)
        # self.click_if_visible('button:contains("Copy code")')
        #
        # self.sleep(10000)
        # #selector
        # self.click('button[name*="backpack"]')
        # self.assert_element('img[alt="Pony Express"]')
        # self.click_if_visible('button:contains("Play")', timeout=2)