from cs50 import SQL
db = SQL("sqlite:///../database.sqlite3")


def sql_Avito(href, title, price, address, metro, description, img, website="avito"):
    rows = db.execute("SELECT title FROM avito_aps WHERE title = ?", title)

    if len(rows) == 0:
        db.execute("INSERT INTO avito_aps(link, title, price, address, metro, description, image, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", href, title, price, address, metro, description, img, website)


def sql_Domclick(href, title, price, address, metro, description, img, website="domclick"):
    rows = db.execute("SELECT title FROM dom_aps WHERE title = ?", title)

    if len(rows) == 0:
        db.execute(f"INSERT INTO dom_aps(link, title, price, address, metro, description, image, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", href, title, price, address, metro, description, img, website)


def sql_Cian(href, title, price, address, metro, description, img, website="cian"):
    rows = db.execute("SELECT title FROM cian_aps WHERE title = ?", title)

    if len(rows) == 0:
        db.execute(f"INSERT INTO cian_aps(link, title, price, address, metro, description, image, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", href, title, price, address, metro, description, img, website)

