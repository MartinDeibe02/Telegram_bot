import pymysql

host = "193.144.42.124"
port = 33306
user = "Martin"
password = "1Super-Password"
database = "inferno"  

def get_inf_lvl(nombre):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        if connection.open:
            
            with connection.cursor() as cursor:
                sql_query = f"SELECT * FROM admision WHERE nome = '{nombre.capitalize()}';"
                cursor.execute(sql_query)
                results = cursor.fetchall()
            print(len(results))
            if len(results) != 0:
                message = f"😈 {results[0][1]} esta en el nivel {results[0][2]} por {results[0][3]} 😈"
                return message
            else:
                return f"{nombre} no esta en el infierno 😃😃"



    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
