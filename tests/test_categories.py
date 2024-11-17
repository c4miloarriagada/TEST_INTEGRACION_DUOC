from conftest import LOCAL_HOST
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_category(driver):
    """
    Verifica que se puede agregar una categoría correctamente desde un modal.
    """

    driver.get(f"{LOCAL_HOST}/Control/categorias.php")

    open_modal_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))
    )
    open_modal_button.click()

    WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.ID, "nuevoCliente"))
    )

    nombre = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "nombre"))
    )
    descripcion = driver.find_element(By.ID, "descripcion")
    guardar = driver.find_element(By.ID, "guardar_datos")

    nombre.send_keys("TEST")
    descripcion.send_keys("TEST")

    guardar.click()

    success_message = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )

    assert (
        "¡Bien hecho! Categoría ha sido ingresada satisfactoriamente."
        in success_message.text
    ), "El mensaje de éxito no coincide o no se mostró."


def test_delete_category(driver):
    """
    Verifica que se puede eliminar una categoría correctamente y desaparezca la fila del DOM.
    """
    driver.refresh()

    target_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='TEST']]"))
    )

    print("Fila encontrada antes de eliminar:", target_row.get_attribute("outerHTML"))

    delete_link = target_row.find_element(By.XPATH, ".//a[@title='Borrar categoría']")
    delete_link.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"Texto de la alerta: {alert.text}")
    alert.accept()

    try:
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, "//tr[td[text()='TEST']]"))
        )
        print("La fila con 'TEST' desapareció correctamente.")
    except Exception as e:
        raise AssertionError(
            "La fila con 'TEST' no fue eliminada correctamente."
        ) from e
