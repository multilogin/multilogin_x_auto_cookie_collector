import os
import dotenv
import time
import random
from multilogin import Mlx
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as Ac
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CookieRobot:
    def __init__(
        self,
        email_address: str,
        password: str,
        websites: list,
        profile_id=None,
        folder_id=None,
        token=None,
        browser_type=None,
    ):
        self.folder_id = folder_id
        self.websites = websites
        self.profile_id = profile_id
        self.token = token
        self.mlx = Mlx(email_address, password, token)
        self.browser_type = browser_type

    def allow_cookies(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        time.sleep(10)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            title = driver.title
            if title == "Welcome to superagent!":
                break
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h6[contains(., 'Cookie Preferences')]")
            )
        ).click()
        wait.until(EC.presence_of_element_located((By.NAME, "advertising"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "other"))).click()
        cookie_options_number = len(
            driver.find_elements(By.XPATH, "//h6[contains(., 'Accept')]")
        )
        assert cookie_options_number == 8
        driver.close()

    def automation(self):
        self.allow_cookies()
        main_handle = self.driver.window_handles[0]
        self.driver.switch_to.window(main_handle)

        try:
            for website in self.websites:
                domain = website.split("//")[1].split("/")[0].split(".")[0]
                cookie_counter = 0
                self.driver.get(website)
                while cookie_counter < 15:
                    current_page = self.driver.current_url
                    # Watch Youtube videos
                    if "watch?" in current_page:
                        time.sleep(random.randrange(120, 240))
                    # Watch "Shorts" videos on Youtube
                    elif "shorts" in current_page:
                        time.sleep(random.randrange(60, 90))
                    self.scroll_randomly(random.randint(1, 5))
                    link_elements = self.driver.find_elements(By.TAG_NAME, "a")
                    elements_with_domain = []
                    for element in link_elements:
                        element_url = element.get_attribute("href")
                        if element_url == None:
                            continue
                        if domain in element_url:
                            elements_with_domain.append(element)
                    random_link = random.choice(elements_with_domain)
                    try:
                        Ac(self.driver).move_to_element(random_link).pause(
                            5
                        ).click().perform()
                        cookie_counter += 1
                    except:
                        try:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView(true); arguments[0].click();",
                                random_link,
                            )
                            cookie_counter += 1
                        except:
                            continue
                    finally:
                        time.sleep(random.randint(3, 5))
        except Exception as e:
            print(f"Something happened: {e}")
        finally:
            # Close browser profile and quit driver
            self.driver.quit()
            self.mlx.stop_profile(self.profile_id)

    def scroll_randomly(self, times):
        for _ in range(times):
            total_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            random_position = random.randint(0, total_height)
            self.driver.execute_script(f"window.scrollTo(0, {random_position});")
            time.sleep(random.randint(1, 5))

    def start_profile(self):
        try:
            profile_started = False
            while not profile_started:
                (
                    self.profile_id,
                    self.profile_port,
                    profile_started,
                    message,
                ) = self.mlx.start_normal_profile(self.profile_id, self.folder_id)
                if profile_started:
                    return
                print(
                    f"Profile couldn't be started. Probably downloading core. Will wait for 60 seconds and try again. Here is the message: {message}"
                )
                time.sleep(60)
        except Exception as e:
            print(f"Problem with starting profile: {e}")

    def run(self):
        if self.token == None:
            self.token = self.mlx.signin()
        self.start_profile()
        self.driver = self.mlx.instantiate_driver(self.profile_port, self.browser_type)
        self.automation()


if __name__ == "__main__":

    dotenv.load_dotenv()
    # Add as many websites as you want for cookie collection
    WEBSITES = ["https://stackoverflow.com/", "https://medium.com/"]

    EMAIL = os.getenv("MLX_EMAIL")
    PASSWORD = os.getenv("MLX_PASSWORD")
    EXTENSION = os.getenv("EXTENSION_PATH")
    BROWSER = os.getenv("BROWSER_TYPE")
    PROFILE_ID = os.getenv("PROFILE_ID")
    FOLDER_ID = os.getenv("FOLDER_ID")

    bot = CookieRobot(
        email_address=EMAIL,
        password=PASSWORD,
        websites=WEBSITES,
        browser_type=BROWSER,
        profile_id=PROFILE_ID,
        folder_id=FOLDER_ID,
    )

    bot.run()
