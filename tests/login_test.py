from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_login_invalid_credentials(driver):
    """
    Verifica el manejo correcto al usar credenciales inválidas.
    """
    driver.get("http://localhost:81/Control/login.php")

    username_field = driver.find_element(By.NAME, "user_name")
    password_field = driver.find_element(By.NAME, "user_password")
    username_field.send_keys("invalid_user")
    password_field.send_keys("invalid_pass")

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    error_message = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
    )
    assert (
        error_message is not None
    ), "No se mostró mensaje de error con credenciales inválidas."


def test_login_valid_credentials(driver):
    """
    Verifica el inicio de sesión exitoso con credenciales válidas.
    """
    driver.get("http://localhost:81/Control/login.php")

    username_field = driver.find_element(By.NAME, "user_name")
    password_field = driver.find_element(By.NAME, "user_password")
    username_field.send_keys("admin")
    password_field.send_keys("admin")

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    success_element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "panel-success"))
    )
    assert success_element is not None, "Inicio de sesión fallido"
