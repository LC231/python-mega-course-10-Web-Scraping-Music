def read(extracted):
     row = extracted.split(",")
     row = [item.strip() for item in row]
     band, city, date = row
     cursor = connection.cursor()
     cursor.execute("SELECT * FROM events WHERE band=? \
                    AND city=? AND date=?", (band, city, date))
     rows = cursor.fetchall()
     print(rows)
     return rows