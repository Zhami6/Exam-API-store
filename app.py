from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
from typing import List, Dict, Any

app: Flask = Flask(__name__)

# Конфигурация подключения к базе данных MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456789"
app.config["MYSQL_DB"] = "api_shop"

# Инициализация экземпляра MySQL
mysql: MySQL = MySQL(app)


# Маршрут для главной страницы
@app.route("/")
def index() -> any:
    return render_template("index.html")


# Маршрут для получения списка продуктов
@app.route("/products", methods=["GET"])
def get_products() -> any:
    cursor = mysql.connection.cursor()
    cursor.execute("""select * from products""")
    rows: List[Dict[str, Any]] = cursor.fetchall()

    sql_cols: List[str] = [col[0] for col in cursor.description]
    rows = [{sql_cols[i]: row[i] for i in range(len(row))} for row in rows]

    cursor.execute("""select * from categories""")
    categories: List[Dict[str, Any]] = cursor.fetchall()

    sql_cols = [col[0] for col in cursor.description]
    categories = [{sql_cols[i]: row[i] for i in range(len(row))} for row in categories]

    cursor.close()

    return render_template(
        "/products/products.html", rows=rows, len=len(rows), categories=categories
    )


# Маршрут для получения информации о конкретном продукте
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Any:
    cursor = mysql.connection.cursor()
    cursor.execute("""select * from products where id = %s""", (product_id,))
    rows: List[Dict[str, Any]] = cursor.fetchall()

    sql_cols: List[str] = [col[0] for col in cursor.description]
    rows = [{sql_cols[i]: row[i] for i in range(len(row))} for row in rows]

    cursor.close()

    return rows[0]


# Маршрут для добавления нового продукта
@app.route("/products/add", methods=["GET", "POST"])
def add_product() -> Any:
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        cursor.execute("""select * from categories""")
        categories: List[Dict[str, Any]] = cursor.fetchall()
        sql_cols: List[str] = [col[0] for col in cursor.description]
        categories = [
            {sql_cols[i]: row[i] for i in range(len(row))} for row in categories
        ]

        cursor.close()

        return render_template("/products/product_add.html", categories=categories)
    elif request.method == "POST":
        name: str = request.form["name"]
        category: str = request.form["category"]
        if not name or not category:
            return "Имя и категория обязательны", 400
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO products (`name`, `category`) VALUES (%s, %s)",
            (name, category),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect("/products")


# Маршрут для изменения информации о продукте
@app.route("/products/change/<int:product_id>", methods=["GET", "POST"])
def change_product(product_id: int) -> Any:
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        cursor.execute("select * from products where id = %s", (product_id,))
        rows: List[Dict[str, Any]] = cursor.fetchall()
        sql_cols: List[str] = [col[0] for col in cursor.description]
        rows = [{sql_cols[i]: row[i] for i in range(len(row))} for row in rows]

        cursor.execute("""select * from categories""")
        categories: List[Dict[str, Any]] = cursor.fetchall()
        sql_cols = [col[0] for col in cursor.description]
        categories = [
            {sql_cols[i]: row[i] for i in range(len(row))} for row in categories
        ]

        cursor.close()

        return render_template(
            "products/product_change.html",
            row=rows[0],
            product_id=product_id,
            categories=categories,
        )
    elif request.method == "POST":
        name: str = request.form["name"]
        category: str = request.form["category"]
        if not name or not category:
            return "Имя и категория обязательны", 400
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE products SET `name` = %s, `category` = %s WHERE id = %s",
            (name, category, product_id),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect("/products")


# Маршрут для удаления продукта
@app.route("/products/delete/<int:product_id>", methods=["GET"])
def delete_product(product_id: int) -> Any:
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM `products` WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect("/products")


# Маршрут для получения списка категорий
@app.route("/categories", methods=["GET"])
def get_categories() -> Any:
    cursor = mysql.connection.cursor()
    cursor.execute("""select * from categories""")
    rows: List[Dict[str, Any]] = cursor.fetchall()
    sql_cols: List[str] = [col[0] for col in cursor.description]
    cursor.close()
    rows = [{sql_cols[i]: row[i] for i in range(len(row))} for row in rows]
    return render_template("/categories/categories.html", rows=rows, len=len(rows))


# Маршрут для получения информации о конкретной категории
@app.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int) -> Any:
    cursor = mysql.connection.cursor()
    cursor.execute("""select * from categories where id = %s""", (category_id,))
    rows: List[Dict[str, Any]] = cursor.fetchall()
    sql_cols: List[str] = [col[0] for col in cursor.description]
    cursor.close()
    rows = [{sql_cols[i]: row[i] for i in range(len(row))} for row in rows]
    return rows[0]


# Маршрут для добавления новой категории
@app.route("/categories/add", methods=["GET", "POST"])
def add_category() -> Any:
    if request.method == "GET":
        return render_template("/categories/category_add.html")
    elif request.method == "POST":
        print(request.form["name"])
        print(" INSERT INTO categories (`name`) VALUES('" + request.form["name"] + "')")
        cursor = mysql.connection.cursor()
        cursor.execute(
            " INSERT INTO categories (`name`) VALUES('" + request.form["name"] + "')"
        )
        mysql.connection.commit()
        return redirect("/categories")


# Маршрут для изменения информации о категории
@app.route("/categories/change/<int:category_id>", methods=["GET", "POST"])
def change_category(category_id: int) -> Any:
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("select * from categories where id = %s", (category_id,))
        row: List[Dict[str, Any]] = cursor.fetchall()
        sql_cols: List[str] = [col[0] for col in cursor.description]
        cursor.close()
        row = [{sql_cols[i]: row[i] for i in range(len(row))} for row in row]
        print(row)
        return render_template(
            "/categories/category_change.html", row=row[0], category_id=category_id
        )
    elif request.method == "POST":
        sql: str = "UPDATE categories SET `name`= %s WHERE id = %s"
        print(sql)
        cursor = mysql.connection.cursor()
        cursor.execute(sql, (request.form["name"], category_id))
        mysql.connection.commit()
        cursor.close()
        return redirect("/categories")


# Маршрут для удаления категории
@app.route("/categories/delete/<int:category_id>", methods=["GET"])
def delete_category(category_id: int) -> Any:
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM `categories` WHERE id = %s", (category_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect("/categories")


if __name__ == "__main__":
    app.run()
    # serve(app, host="127.0.0.1", port=8080)
    # app.run(debug=True)


# def create_app():
#    return app
