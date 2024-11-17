import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

##! CAMBIAR URL DONDE SE HAGAN LAS PRUEBAS.
LOCAL_HOST = "http://localhost:81"


@pytest.fixture(scope="session")
def driver():
    chromedriver_autoinstaller.install()

    options = Options()
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()
