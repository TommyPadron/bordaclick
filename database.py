import sqlite3
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


DATABASE = "bordaclick.db"

def crear_bd():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordenes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT,
    telefono TEXT,
    correo TEXT,
    colegio TEXT,

    cantidad_total INTEGER,

    tipo_logo TEXT,

    nombre_bordado TEXT,

    cantidad_nombre INTEGER,

    delivery TEXT,

    zona_delivery TEXT,

    fecha_entrega TEXT,

    precio_bordado REAL,

    subtotal_bordado REAL,

    subtotal_nombres REAL,

    delivery_costo REAL,

    abono REAL,

    saldo_pendiente REAL,
    
    status TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orden_detalle (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    orden_id INTEGER,

    tipo_prenda TEXT,

    talla TEXT,

    marca TEXT,

    color TEXT,

    cantidad INTEGER,

    FOREIGN KEY (orden_id)
    REFERENCES ordenes(id)

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion_bordados (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        colegio TEXT UNIQUE,

        precio_bordado REAL

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion_general (

        parametro TEXT PRIMARY KEY,

        valor REAL

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colegios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE,

        precio_bordado REAL

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_prenda (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE

    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marcas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE

    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colores (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE

    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tallas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colores (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT UNIQUE

    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zonas_delivery (
            nombre TEXT PRIMARY KEY,
            costo REAL
        )
    """)    

    conn.commit()

    conn.close()

def guardar_orden(
    nombre,
    telefono,
    correo,
    colegio,
    cantidad_total,
    tipo_logo,
    nombre_bordado,
    cantidad_nombre,
    delivery,
    zona_delivery,
    fecha_entrega,
    precio_bordado,
    subtotal_bordado,
    subtotal_nombres,
    delivery_costo,
    abono,
    saldo_pendiente,
    status
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ordenes (
            nombre,
            telefono,
            correo,
            colegio,
            cantidad_total,
            tipo_logo,
            nombre_bordado,
            cantidad_nombre,
            delivery,
            zona_delivery,
            fecha_entrega,
            precio_bordado,
            subtotal_bordado,
            subtotal_nombres,
            delivery_costo,
            abono,
            saldo_pendiente,
            status
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        nombre,
        telefono,
        correo,
        colegio,
        cantidad_total,
        tipo_logo,
        nombre_bordado,
        cantidad_nombre,
        delivery,
        zona_delivery,
        str(fecha_entrega),
        precio_bordado,
        subtotal_bordado,
        subtotal_nombres,
        delivery_costo,
        abono,
        saldo_pendiente,
        status
    ))

    conn.commit()

    orden_id = cursor.lastrowid

    conn.close()

    return orden_id

def guardar_detalle(
    orden_id,
    tipo_prenda,
    talla,
    marca,
    color,
    cantidad
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orden_detalle (

        orden_id,
        tipo_prenda,
        talla,
        marca,
        color,
        cantidad

    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        orden_id,
        tipo_prenda,
        talla,
        marca,
        color,
        cantidad
    ))

    conn.commit()
    conn.close()

def obtener_precio_bordado(colegio):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT precio_bordado
        FROM configuracion_bordados
        WHERE colegio = ?
    """, (colegio,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return 0

def guardar_precio_bordado(
    colegio,
    precio_bordado
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO configuracion_bordados (
            colegio,
            precio_bordado
        )
        VALUES (?, ?)
    """,
    (
        colegio,
        precio_bordado
    ))

    conn.commit()
    conn.close()

def guardar_catalogo_bordados(df):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM configuracion_bordados"
    )

    for _, fila in df.iterrows():

        cursor.execute("""
        INSERT INTO configuracion_bordados (
            colegio,
            precio_bordado
        )
        VALUES (?, ?)
        """,
        (
            fila["colegio"],
            fila["precio_bordado"]
        ))

    conn.commit()

    conn.close()


def obtener_catalogo_bordados():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        colegio,
        precio_bordado
    FROM configuracion_bordados
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def guardar_parametro(
    parametro,
    valor
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO configuracion_general (
        parametro,
        valor
    )
    VALUES (?, ?)
    """,
    (
        parametro,
        valor
    ))

    conn.commit()
    conn.close()

def obtener_parametro(
    parametro
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT valor
    FROM configuracion_general
    WHERE parametro = ?
    """,
    (parametro,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return 0
def guardar_colegio(
    nombre,
    precio_bordado
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO colegios (
            nombre,
            precio_bordado
        )
        VALUES (?, ?)
    """,
    (
        nombre,
        precio_bordado
    ))

    conn.commit()

    conn.close()

def guardar_zona_delivery(
    nombre,
    costo
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO zonas_delivery (
            nombre,
            costo
        )
        VALUES (?, ?)
    """,
    (
        nombre,
        costo
    ))

    conn.commit()

    conn.close()
    

    
def obtener_zonas_delivery():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        nombre,
        costo
    FROM zonas_delivery
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df    

def obtener_ordenes():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        id,
        nombre,
        colegio,
        status,
        fecha_entrega,
        saldo_pendiente
    FROM ordenes
    ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def obtener_orden_por_id(orden_id):

    conn = sqlite3.connect(DATABASE)

    query = f"""
    SELECT *
    FROM ordenes
    WHERE id = {orden_id}
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def obtener_detalle_orden(orden_id):

    conn = sqlite3.connect(DATABASE)

    query = f"""
    SELECT
        tipo_prenda,
        talla,
        marca,
        color,
        cantidad
    FROM orden_detalle
    WHERE orden_id = {orden_id}
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def registrar_pago(
    orden_id,
    monto_pago
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            abono,
            saldo_pendiente
        FROM ordenes
        WHERE id = ?
    """,
    (
        orden_id,
    ))

    resultado = cursor.fetchone()

    abono_actual = resultado[0]
    saldo_actual = resultado[1]

    nuevo_abono = abono_actual + monto_pago

    nuevo_saldo = saldo_actual - monto_pago

    if nuevo_saldo < 0:

        nuevo_saldo = 0

    cursor.execute("""
        UPDATE ordenes
        SET
            abono = ?,
            saldo_pendiente = ?
        WHERE id = ?
    """,
    (
        nuevo_abono,
        nuevo_saldo,
        orden_id
    ))

    conn.commit()

    conn.close()

def actualizar_status_orden(
    orden_id,
    status
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()
    
    print(
    "ID:",
    orden_id,
    type(orden_id)
    )

    cursor.execute("""
        UPDATE ordenes
        SET status = ?
        WHERE id = ?
    """,
    (
        status,
        orden_id
    ))
    
    conn.commit()
    
    print(
    "FILAS AFECTADAS:",
    cursor.rowcount
    )

    conn.close()
    
def obtener_colegios():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        nombre,
        precio_bordado
    FROM colegios
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def obtener_precio_colegio(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT precio_bordado
        FROM colegios
        WHERE nombre = ?
    """,
    (
        nombre,
    ))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        return resultado[0]

    return 0

def guardar_tipo_prenda(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO tipos_prenda (
            nombre
        )
        VALUES (?)
    """,
    (
        nombre,
    ))

    conn.commit()

    conn.close()
def obtener_tipos_prenda():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT nombre
    FROM tipos_prenda
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df
def guardar_marca(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO marcas (
            nombre
        )
        VALUES (?)
    """,
    (
        nombre,
    ))

    conn.commit()

    conn.close()
def obtener_marcas():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT nombre
    FROM marcas
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df
def guardar_color(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO colores (
            nombre
        )
        VALUES (?)
    """,
    (
        nombre,
    ))

    conn.commit()

    conn.close()
def obtener_colores():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT nombre
    FROM colores
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df
def guardar_talla(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO tallas (
            nombre
        )
        VALUES (?)
    """,
    (
        nombre,
    ))

    conn.commit()

    conn.close()
def obtener_tallas():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT nombre
    FROM tallas
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def guardar_color(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO colores (
            nombre
        )
        VALUES (?)
    """,
    (
        nombre,
    ))

    conn.commit()

    conn.close()
    
def obtener_colores():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT nombre
    FROM colores
    ORDER BY nombre
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

def enviar_pdf_por_correo(
    destinatario,
    nombre_cliente,
    orden_id,
    fecha_entrega,
    pdf_path
):

    remitente = "bordaclick@gmail.com"
    password = "niiv nskd qzox xwnr"

    mensaje = MIMEMultipart()

    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = (
        f"Bordaclick - Confirmación de Pedido #{orden_id:04d}"
    )

    cuerpo = f"""
Hola {nombre_cliente},

Gracias por confiar en Bordaclick.

Hemos recibido correctamente tu solicitud de bordado.

Adjunto encontrarás la Orden de Servicio correspondiente a tu pedido, donde podrás consultar los detalles de producción, cantidades, datos de entrega y resumen financiero.

Número de Pedido: #{orden_id:04d}
Fecha de Entrega: {fecha_entrega}

Si necesitas realizar alguna consulta o modificación, puedes responder a este correo y con gusto te atenderemos.

Gracias por elegir Bordaclick.

Saludos,

Equipo Bordaclick
Bordados Escolares Personalizados
"""

    mensaje.attach(
        MIMEText(
            cuerpo,
            "plain",
            "utf-8"
        )
    )

    with open(pdf_path, "rb") as archivo:

        parte = MIMEBase(
            "application",
            "octet-stream"
        )

        parte.set_payload(
            archivo.read()
        )

    encoders.encode_base64(parte)

    parte.add_header(
        "Content-Disposition",
        f"attachment; filename={pdf_path}"
    )

    mensaje.attach(parte)
    
    print("===== INICIO ENVIO EMAIL =====")
    print("DESTINATARIO:", destinatario)
    print("PDF:", pdf_path)
    
    

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()
    
    try:

        servidor.login(
            "bordaclick@gmail.com",
            "niiv nskd qzox xwnr"
        )

        servidor.send_message(
            mensaje
        )

        servidor.quit()

    except Exception as e:

        print(
            f"❌ Error Gmail: {e}"
        )

        raise


def obtener_costo_delivery(
    nombre
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT costo
        FROM zonas_delivery
        WHERE nombre = ?
    """,
    (
        nombre,
    ))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        return resultado[0]

    return 0

def enviar_notificacion_estado(
    destinatario,
    nombre_cliente,
    orden_id,
    fecha_entrega,
    estado,
    delivery
):

    remitente = "bordaclick@gmail.com"
    password = "niiv nskd qzox xwnr"

    mensaje = MIMEMultipart()

    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    if estado == "En Producción":

        mensaje["Subject"] = (
            f"Bordaclick - Tu pedido #{orden_id:04d} está en producción"
        )

        cuerpo = f"""
Hola {nombre_cliente},

Queremos informarte que tu pedido #{orden_id:04d} ya se encuentra en proceso de producción.

Fecha estimada de entrega:
{fecha_entrega}

Gracias por confiar en Bordaclick.

Bordaclick Diseños
Sistema de Gestión de Bordados Escolares
"""

    elif estado == "Listo para Entrega":

        if "Sí" in str(delivery):
        # if delivery == "Sí":

            mensaje["Subject"] = (
                f"Bordaclick - Tu pedido #{orden_id:04d} está listo para entrega"
            )

            cuerpo = f"""
Hola {nombre_cliente},

Nos complace informarte que tu pedido #{orden_id:04d} ya está listo y será entregado mediante nuestro servicio de delivery.

Nos pondremos en contacto contigo para coordinar la entrega.

Gracias por confiar en Bordaclick.

Bordaclick Diseños
Sistema de Gestión de Bordados Escolares
"""

        else:

            mensaje["Subject"] = (
                f"Bordaclick - Tu pedido #{orden_id:04d} está listo para ser retirado"
            )

            cuerpo = f"""
Hola {nombre_cliente},

Nos complace informarte que tu pedido #{orden_id:04d} está listo para ser retirado.

Puedes comunicarte con nosotros para coordinar el retiro o la entrega de tu pedido.

Gracias por confiar en Bordaclick.

Bordaclick Diseños
Sistema de Gestión de Bordados Escolares
"""

    else:
        return

    mensaje.attach(
        MIMEText(
            cuerpo,
            "plain",
            "utf-8"
        )
    )

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()

    servidor.login(
        remitente,
        password
    )

    servidor.send_message(
        mensaje
    )

    servidor.quit()


def contar_pedidos_pendientes():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM ordenes
        WHERE status = 'Recibido'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

    






