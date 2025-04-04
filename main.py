from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Настройки браузера
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

# Открываем страницу Labirint с иностранными книгами
url = "https://www.labirint.ru/foreignbooks/"
driver.get(url)

# Ждём загрузку страницы
time.sleep(7)  # Увеличим время ожидания

# Получаем список книг
books = driver.find_elements(By.CSS_SELECTOR, "div.product")[:10]  # Проверим селектор

book_data = []

for book in books:
    try:
        # Название книги
        try:
            title = book.find_element(By.CSS_SELECTOR, "span.product-title").text.strip()
        except:
            title = "Нет названия"
        print(f"Название: {title}")  # Проверяем вывод

        # Автор книги
        try:
            author = book.find_element(By.CSS_SELECTOR, "div.product-author a").text.strip()
        except:
            author = "Не указан"
        print(f"Автор: {author}")

        # Цена книги
        try:
            price = book.find_element(By.CSS_SELECTOR, "span.price-val span").text.strip()
        except:
            price = "Нет в продаже"
        print(f"Цена: {price}")

        # Рейтинг книги
        try:
            rating = book.find_element(By.CSS_SELECTOR, "div.product-rating").get_attribute("title")
        except:
            rating = "Нет рейтинга"
        print(f"Рейтинг: {rating}")

        # Добавляем данные в список
        book_data.append([title, author, price, rating])

    except Exception as e:
        print(f"❌ Ошибка при обработке книги: {e}")

# Закрываем браузер
driver.quit()

# Записываем в CSV
df = pd.DataFrame(book_data, columns=["Название", "Автор", "Цена", "Рейтинг"])
df.to_csv("labirint_foreign_books.csv", index=False, encoding="utf-8-sig")

print("✅ Данные успешно сохранены в 'labirint_foreign_books.csv'")
