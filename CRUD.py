import psycopg

# Conexión a la base de datos

def connect_db(db_name):
    conexion = f"""
        dbname={db_name}
        user=postgres
        password=cisco
        host=localhost
        port=5432
    """
    conn = psycopg.connect(conexion)
    curs = conn.cursor()
    return conn, curs

# Menú principal
def menu():
    conn = connect_db()
    print("Menú Principal")
    print("1 - Consultar tots els artistes")
    print("2 - Consultar artistes pel seu nom")
    print("3 - Consultar els 5 primers àlbums pel nom de l'artista")
    print("4 - Afegir un artista")
    print("5 - Modificar el nom d'un artista")
    print("6 - Borrar un artista")
    print("7 - Sortir")

    while True:
        
        opcio=input("Selecciona una opció: ")
        if opcio == 1:
                Consultar_tots_els_artistes(conn)
        elif opcio == 2:
                Consultar_artistes_pel_seu_nom(conn)
        elif opcio == 3:
                Consultar_5_primers_albums_per_artista(conn)
        elif opcio == 4:
                Afegir_artista(conn)
        elif opcio == 5:
                Modificar_nom_artista(conn)
        elif opcio == 6:
                Borrar_artista(conn)
        elif opcio == 7:
                print("Sortin del programa...")
                conn.close()
                break   
        else:
            print("Opcio no valida, introdueix una opcio correcta")
            return 

# Consultar tots els artistes
def Consultar_tots_els_artistes(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM artist;")
    artistas = cur.fetchall()
    for artista in artistas:
        print(f"ID: {artista[0]}, NOM: {artista[1]}")
    cur.close()

# Consultar artistes pel seu nom
def Consultar_artistes_pel_seu_nom(conn):
    nom = input("Introdueix el nom de l'artista: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM artist WHERE name ILIKE %s;", (f"%{nom}%",))
    artistas = cur.fetchall()
    if artistas:
        for artista in artistas:
            print(f"ID: {artista[0]}, NOM: {artista[1]}")
    else:
        print("No hi ha cap artista amb aquest nom.")
    cur.close()

# Consultar els 5 primers àlbums pel nom de l'artista
def Consultar_5_primers_albums_per_artista(conn):
    nom = input("Introdueix el nom de l'artista: ")
    cur = conn.cursor()
    cur.execute("""
        SELECT album.album_id, album.title, artist.name 
        FROM album 
        JOIN artist ON album.artist_id = artist.artist_id 
        WHERE artist.name ILIKE %s
        ORDER BY album.album_id 
        LIMIT 5;
    """,(f"%{nom}%",))
    albums = cur.fetchall()
    if albums:
        for album in albums:
            print(f"ID_ALBUM: {album[0]}, NOM_ALBUM: {album[1]}, NOM_ARTISTA: {album[2]}")
    else:
        print("L'artista introduit no existeix o no te albums.")
    cur.close()

# Afegir un artista
def Afegir_artista(conn):
    nom = input("Introdueix el nom de l'artista: ")
    cur = conn.cursor()
    cur.execute("INSERT INTO artist (name) VALUES (%s);", (nom,))
    conn.commit()
    print("S'ha creat l'artista: ",nom)
    cur.close()

# Modificar el nom d'un artista
def Modificar_nom_artista(conn):
    artista = input("Introdueix l'ID del teu artista: ")
    nou_nom = input("Introdueix el nou nom de l'artista: ")
    cur = conn.cursor()
    cur.execute("UPDATE artist SET name = %s WHERE artist_id = %s;", (nou_nom, artista))
    conn.commit()
    print(f"L'artista amb l'ID: {artista}, ara es diu: {nou_nom}")
    cur.close()

# Borrar un artista
def Borrar_artista(conn):
    artista = input("Introdueix l'ID de l'artista: ")
    cur = conn.cursor()
    cur.execute("SELECT name FROM artist WHERE artist_id = %s," (artista,))
    nom = cur.fetchall()
    cur.execute("DELETE FROM artist WHERE artist_id = %s;", (artista,))
    conn.commit()
    print(f"L'artista: {nom} ja no existeix")
    cur.close()

# Executar Menu
if __name__ == "__main__":
    menu()