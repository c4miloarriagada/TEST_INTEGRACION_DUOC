from conftest import LOCAL_HOST
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_user(driver):
    """
    Verifica que se puede agregar un usuario correctamente.
    """

    driver.get(f"{LOCAL_HOST}/Control/usuarios.php")

    add_user_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))
    )
    add_user_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "myModal"))
    )

    firstname = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "firstname"))
    )
    lastname = driver.find_element(By.ID, "lastname")
    username = driver.find_element(By.ID, "user_name")
    email = driver.find_element(By.ID, "user_email")
    password = driver.find_element(By.ID, "user_password_new")
    repeat_password = driver.find_element(By.ID, "user_password_repeat")
    save_button = driver.find_element(By.ID, "guardar_datos")

    firstname.send_keys("NombreTest")
    lastname.send_keys("ApellidoTest")
    username.send_keys("UsuarioTest")
    email.send_keys("usuariotest@example.com")
    password.send_keys("password123")
    repeat_password.send_keys("password123")

    save_button.click()

    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    assert (
        "La cuenta ha sido creada con éxito." in success_message.text
    ), f"Mensaje de éxito incorrecto: {success_message.text}"
