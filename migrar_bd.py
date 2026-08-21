import sqlite3

ORIGEN = "bordaclick.db"
DESTINO = "bordaclick_dev.db"

def migrar():
    print("🚀 Iniciando migración de Producción a Desarrollo...")

    try:
        conn_ori = sqlite3.connect(ORIGEN)
        conn_des = sqlite3.connect(DESTINO)
        
        cursor_ori = conn_ori.cursor()
        cursor_des = conn_des.cursor()

        # Desactivar temporalmente claves foráneas para evitar conflictos en la inserción
        cursor_des.execute("PRAGMA foreign_keys = OFF;")

        tablas = [
            "configuracion_general",
            "colegios",
            "tipos_prenda",
            "marcas",
            "colores",
            "tallas",
            "zonas_delivery",
            "ordenes",
            "orden_detalle"
        ]

        for tabla in tablas:
            # Obtener columnas del destino para asegurar compatibilidad
            cursor_des.execute(f"PRAGMA table_info({tabla})")
            cols_des = [col[1] for col in cursor_des.fetchall()]
            cols_str = ", ".join(cols_des)

            # Obtener columnas del origen
            cursor_ori.execute(f"PRAGMA table_info({tabla})")
            cols_ori = [col[1] for col in cursor_ori.fetchall()]

            # Verificar qué columnas existen en el origen y cuáles faltan (como fecha_pago)
            cols_select = []
            for col in cols_des:
                if col in cols_ori:
                    cols_select.append(col)
                else:
                    cols_select.append("NULL as " + col)

            select_str = ", ".join(cols_select)

            # Extraer e Insertar
            cursor_ori.execute(f"SELECT {select_str} FROM {tabla}")
            filas = cursor_ori.fetchall()

            if filas:
                placeholders = ", ".join(["?"] * len(cols_des))
                cursor_des.executemany(
                    f"INSERT OR REPLACE INTO {tabla} ({cols_str}) VALUES ({placeholders})",
                    filas
                )
                print(f"✅ Tabla '{tabla}': {len(filas)} registros copiados.")
            else:
                print(f"ℹ️ Tabla '{tabla}': Sin registros para copiar.")

        conn_des.commit()
        conn_ori.close()
        conn_des.close()
        print("\n🎉 ¡Migración completada exitosamente!")

    except sqlite3.OperationalError as e:
        print(f"\n❌ Error de archivo o SQLite: {e}")
        print("Asegúrate de que 'bordaclick.db' existe en la carpeta actual.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    migrar()