from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def test_add_product(driver):
    """
    Verifica que se puede agregar un producto correctamente.
    """
    driver.get("http://localhost:81/Control/stock.php")

    add_product_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))
    )
    add_product_button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nuevoProducto"))
    )

    # Localizar campos del formulario dentro del modal
    codigo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "codigo"))
    )
    nombre = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nombre"))
    )
    categoria = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "categoria"))
    )
    precio = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "precio"))
    )
    stock = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "stock"))
    )
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "guardar_datos"))
    )

    codigo.send_keys("P001")
    nombre.send_keys("Producto Test")

    select_categoria = Select(categoria)
    select_categoria.select_by_value("5")

    precio.send_keys("100")
    stock.send_keys("50")

    save_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "resultados_ajax_productos"),
            "Producto ha sido ingresado satisfactoriamente",
        )
    )

    success_message = driver.find_element(By.ID, "resultados_ajax_productos").text
    assert (
        "Producto ha sido ingresado satisfactoriamente" in success_message
    ), f"Mensaje de éxito incorrecto: {success_message}"


def test_delete_product(driver):
    """
    Verifica que se puede eliminar un producto correctamente desde su página específica y que desaparece del listado de stock.
    """

    driver.refresh()

    product_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'thumb') and .//strong[text()='Producto Test']]",
            )
        )
    )

    product_link = product_card.find_element(
        By.XPATH, ".//a[contains(@href, 'producto.php')]"
    )
    product_link.click()

    WebDriverWait(driver, 10).until(EC.url_contains("producto.php"))

    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Eliminar']"))
    )
    delete_button.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    WebDriverWait(driver, 10).until(EC.url_contains("stock.php"))
    driver.refresh()

    product_absent = WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'thumb') and .//strong[text()='Producto Test']]",
            )
        )
    )
    assert (
        product_absent
    ), "El producto 'Producto Test' todavía está presente después de eliminarlo."
