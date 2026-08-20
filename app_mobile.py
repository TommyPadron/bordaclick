import streamlit as st
import pandas as pd
from datetime import date, timedelta

from db_handler import (
    crear_bd,
    obtener_colegios,
    guardar_colegio,
    eliminar_colegio,
    obtener_tipos_prenda,
    guardar_tipo_prenda,
    eliminar_tipo_prenda,
    obtener_tallas,
    guardar_talla,
    eliminar_talla,
    obtener_marcas,
    guardar_marca,
    eliminar_marca,
    obtener_colores,
    guardar_color,
    eliminar_color,
    obtener_zonas_delivery,
    guardar_zona_delivery,
    eliminar_zona_delivery,
    obtener_costo_delivery,
    obtener_parametro,
    guardar_parametro,
    obtener_precio_colegio,
    guardar_orden,
    guardar_detalle,
    obtener_orden_por_id,
    obtener_detalle_orden,
    enviar_pdf_por_correo,
    enviar_confirmacion_solicitud,
    obtener_ordenes,
    registrar_pago,
    obtener_historico_pagos,
    actualizar_status_orden,
    enviar_notificacion_estado
)

from pdf_tools import (
    generar_pdf_orden,
    generar_excel_orden,
    generar_excel_historico
)

# Inicializar Base de Datos de Desarrollo al arrancar
crear_bd()

st.set_page_config(
    page_title="Bordaclick Clientes (DEV)",
    page_icon="🧵",
    layout="centered"
)

clave_admin = st.sidebar.text_input("Clave Administrador", type="password")

opciones_menu = ["📝 Nueva Solicitud"]

if clave_admin == "BordaAdmin2026*":
    opciones_menu.extend([
        "📋 Consultas",
        "⚙️ Configuración",
        "🏫 Colegios",
        "🚚 Delivery",
        "📦 Prendas",
        "🏷️ Marcas",
        "📏 Tallas",
        "🎨 Colores",
        "💾 Respaldo"
    ])

pagina = st.sidebar.selectbox("Menú", opciones_menu)

if "paso" not in st.session_state:
    st.session_state.paso = 1

if "solicitud_enviada" not in st.session_state:
    st.session_state.solicitud_enviada = False

if "colegios_agregados" not in st.session_state:
    st.session_state.colegios_agregados = []

# Encabezado
col1, col2 = st.columns([1, 3])
with col1:
    try:
        st.image("Logo Bordaclick.JPG", width=80)
    except Exception:
        st.write("🧵")

with col2:
    st.title("🧵 Bordaclick")
    st.caption("Solicitud desde Celular (Entorno DEV)")

st.divider()

if pagina == "📝 Nueva Solicitud":

    # --- PASO 1: Datos de Contacto ---
    if st.session_state.paso == 1:
        st.progress(25)
        st.subheader("👤 Datos del Cliente")

        nombre = st.text_input("Nombre y Apellido", value=st.session_state.get("nombre", ""))
        telefono = st.text_input("Teléfono", value=st.session_state.get("telefono", ""))
        correo = st.text_input("Correo Electrónico", value=st.session_state.get("correo", ""))

        if st.button("Continuar ➡️", use_container_width=True):
            if not nombre.strip():
                st.error("Debe ingresar el nombre.")
            elif not telefono.strip() or len(telefono.strip()) < 10:
                st.error("Debe ingresar un teléfono válido (mínimo 10 dígitos).")
            elif "@" not in correo or "." not in correo:
                st.error("Debe ingresar un correo electrónico válido.")
            else:
                st.session_state.nombre = nombre
                st.session_state.telefono = telefono
                st.session_state.correo = correo
                st.session_state.paso = 2
                st.rerun()

    # --- PASO 2: Selección de Colegios y Prendas ---
    elif st.session_state.paso == 2:
        st.progress(50)
        st.subheader("🏫 Colegio y Prendas")

        df_col = obtener_colegios()
        lista_colegios = ["Seleccione un colegio..."] + (df_col["nombre"].dropna().tolist() if not df_col.empty else [])
        colegio = st.selectbox("Seleccione el Colegio", lista_colegios)

        st.divider()
        st.subheader("👕 Agregar Prenda")

        df_p = obtener_tipos_prenda()
        lista_tipos_prenda = ["Seleccione una prenda..."] + (df_p["nombre"].dropna().tolist() if not df_p.empty else [])

        df_t = obtener_tallas()
        lista_tallas = ["Seleccione una talla..."] + (df_t["nombre"].dropna().tolist() if not df_t.empty else [])

        df_m = obtener_marcas()
        lista_marcas = ["Seleccione una marca..."] + (df_m["nombre"].dropna().tolist() if not df_m.empty else [])

        df_c = obtener_colores()
        lista_colores = ["Seleccione un color..."] + (df_c["nombre"].dropna().tolist() if not df_c.empty else [])

        tipo_prenda = st.selectbox("Tipo de Prenda", lista_tipos_prenda, key="tipo_prenda_actual")
        talla = st.selectbox("Talla", lista_tallas, key="talla_actual")
        marca = st.selectbox("Marca", lista_marcas, key="marca_actual")
        color = st.selectbox("Color", lista_colores, key="color_actual")
        cantidad = st.number_input("Cantidad", min_value=1, value=1, key="cantidad_actual")

        if "prendas_actuales" not in st.session_state:
            st.session_state.prendas_actuales = []

        if st.button("➕ Agregar Prenda", use_container_width=True):
            if colegio == "Seleccione un colegio...":
                st.error("Debe seleccionar un colegio.")
            elif tipo_prenda == "Seleccione una prenda...":
                st.error("Debe seleccionar un tipo de prenda.")
            elif talla == "Seleccione una talla...":
                st.error("Debe seleccionar una talla.")
            elif marca == "Seleccione una marca...":
                st.error("Debe seleccionar una marca.")
            elif color == "Seleccione un color...":
                st.error("Debe seleccionar un color.")
            else:
                st.session_state.prendas_actuales.append({
                    "tipo": tipo_prenda,
                    "talla": talla,
                    "marca": marca,
                    "color": color,
                    "cantidad": cantidad
                })
                st.rerun()

        st.divider()
        st.subheader("📋 Revise las prendas antes de guardar el colegio")

        if not st.session_state.prendas_actuales:
            st.info("Aún no hay prendas agregadas para el colegio actual.")
        else:
            for i, prenda in enumerate(st.session_state.prendas_actuales):
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.success(f"👕 {prenda['tipo']} | 📏 {prenda['talla']} | 🏷️ {prenda['marca']} | 🎨 {prenda['color']} | 🔢 {prenda['cantidad']}")
                with c2:
                    if st.button("🗑️", key=f"borrar_prenda_{i}"):
                        st.session_state.prendas_actuales.pop(i)
                        st.rerun()

        st.divider()

        if st.button("💾 Guardar Colegio", use_container_width=True):
            if not st.session_state.prendas_actuales:
                st.error("Debe agregar al menos una prenda.")
            else:
                if any(c["colegio"] == colegio for c in st.session_state.colegios_agregados):
                    st.error("Ese colegio ya fue agregado.")
                else:
                    st.session_state.colegios_agregados.append({
                        "colegio": colegio,
                        "prendas": st.session_state.prendas_actuales.copy()
                    })
                    st.session_state.prendas_actuales = []
                    st.success("✅ Colegio guardado correctamente")
                    st.rerun()

        st.subheader("🏫 Colegios Agregados")
        if not st.session_state.colegios_agregados:
            st.info("Aún no hay colegios guardados.")
        else:
            for idx_col, colegio_data in enumerate(st.session_state.colegios_agregados):
                c_lbl, c_btn = st.columns([5, 1])
                with c_lbl:
                    st.success(f"🏫 {colegio_data['colegio']}")
                with c_btn:
                    if st.button("🗑️", key=f"del_col_agregado_{idx_col}"):
                        st.session_state.colegios_agregados.pop(idx_col)
                        st.rerun()

                for prenda in colegio_data["prendas"]:
                    st.write(f"• {prenda['tipo']} ({prenda['talla']}) x {prenda['cantidad']}")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Agregar Otro Colegio", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("Continuar ➡️", use_container_width=True):
                if not st.session_state.colegios_agregados:
                    st.error("Debe guardar al menos un colegio con prendas.")
                else:
                    st.session_state.paso = 3
                    st.rerun()

    # --- PASO 3: Personalización de Bordado y Delivery ---
    elif st.session_state.paso == 3:
        st.progress(75)
        st.subheader("🧵 Bordado y Delivery")

        tipo_logo = st.selectbox("Tipo de Logo", ["Diario", "Deporte", "Preescolar"], key="paso3_tipo_logo")
        bordar_nombre = st.selectbox("¿Desea bordar nombres?", ["Seleccione una opción...", "No", "Sí"], index=0, key="paso3_bordar_nombre")

        nombre_bordado = ""
        cantidad_nombre = 0
        total_prendas = sum(p["cantidad"] for c in st.session_state.colegios_agregados for p in c["prendas"])

        if bordar_nombre == "Sí":
            nombre_bordado = st.text_area("Detalle del nombre a bordar por prenda (ej. Suéter talla 10: Miranda Guerrero)", key="paso3_nombre_bordado")
            cantidad_nombre = st.number_input("Cantidad de Prendas con Nombre", min_value=1, max_value=max(1, int(total_prendas)), value=1, key="paso3_cantidad_nombre")
            st.caption(f"Máximo permitido: {total_prendas} prendas")
        elif bordar_nombre == "No":
            st.success("✅ Sin bordado de nombres")

        st.divider()
        st.subheader("🚚 Delivery")

        delivery = st.selectbox("¿Desea Delivery?", ["Seleccione una opción...", "No", "Sí"], index=0, key="paso3_delivery")
        zona_delivery, costo_delivery = "", 0.0

        if delivery == "Sí":
            df_z = obtener_zonas_delivery()
            lista_zonas = df_z["nombre"].dropna().tolist() if not df_z.empty else []
            zona_delivery = st.selectbox("Zona de Delivery", lista_zonas, key="paso3_zona_delivery")
            try:
                costo_delivery = obtener_costo_delivery(zona_delivery)
                st.success(f"🚚 Costo Delivery: ${costo_delivery:.2f}")
            except Exception:
                st.warning("No se pudo obtener el costo del delivery.")
        elif delivery == "No":
            st.info("📍 Retiro en tienda")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Atrás", use_container_width=True):
                st.session_state.paso = 2
                st.rerun()
        with col2:
            if st.button("Continuar ➡️", use_container_width=True):
                if bordar_nombre == "Seleccione una opción...":
                    st.error("Debe indicar si desea bordar nombres.")
                elif delivery == "Seleccione una opción...":
                    st.error("Debe indicar si desea delivery.")
                elif bordar_nombre == "Sí" and not nombre_bordado.strip():
                    st.error("Debe indicar el detalle del bordado.")
                else:
                    st.session_state.tipo_logo = tipo_logo
                    st.session_state.bordar_nombre = bordar_nombre
                    st.session_state.nombre_bordado = nombre_bordado
                    st.session_state.cantidad_nombre = cantidad_nombre
                    st.session_state.delivery = delivery
                    st.session_state.zona_delivery = zona_delivery
                    st.session_state.costo_delivery = costo_delivery
                    st.session_state.paso = 4
                    st.rerun()

    # --- PASO 4: Resumen y Confirmación ---
    elif st.session_state.paso == 4:
        st.progress(100)
        st.subheader("📋 Resumen de la Solicitud")

        st.success(f"👤 {st.session_state.nombre}")
        st.write(f"📞 {st.session_state.telefono} | 📧 {st.session_state.correo}")

        st.subheader("🧵 Bordado")
        st.write(f"Tipo Logo: {st.session_state.tipo_logo}")
        st.write(f"Bordar Nombre: {st.session_state.bordar_nombre}")
        if st.session_state.bordar_nombre == "Sí":
            st.write(f"Detalle: {st.session_state.nombre_bordado}")
            st.write(f"Cantidad: {st.session_state.cantidad_nombre}")

        dias_produccion = int(obtener_parametro("dias_produccion") or 3)
        fecha_entrega = date.today() + timedelta(days=dias_produccion)

        st.subheader("💰 Resumen Financiero")
        st.write(f"📅 Fecha estimada entrega: {fecha_entrega.strftime('%d/%m/%Y')}")

        subtotal_bordado = 0.0
        for colegio_data in st.session_state.colegios_agregados:
            colegio_nombre = colegio_data["colegio"]
            cantidad_colegio = sum(p["cantidad"] for p in colegio_data["prendas"])
            precio_colegio = obtener_precio_colegio(colegio_nombre)

            if cantidad_colegio >= 6:
                precio_colegio = max(0.0, precio_colegio - 0.50)

            subtotal_colegio = cantidad_colegio * precio_colegio
            subtotal_bordado += subtotal_colegio

            st.write(f"🏫 {colegio_nombre} {'(🎉 Promo desc. 6+ prendas)' if cantidad_colegio >= 6 else ''}")
            st.write(f"   👕 {cantidad_colegio} prendas x ${precio_colegio:.2f} = ${subtotal_colegio:.2f}")

        precio_nombre = float(obtener_parametro("precio_nombre") or 0)
        subtotal_nombres = (st.session_state.cantidad_nombre * precio_nombre) if st.session_state.bordar_nombre == "Sí" else 0.0

        if st.session_state.bordar_nombre == "Sí":
            st.write(f"🔤 {st.session_state.cantidad_nombre} nombres x ${precio_nombre:.2f} = ${subtotal_nombres:.2f}")

        st.write(f"🚚 Delivery = ${st.session_state.costo_delivery:.2f}")
        total_estimado = subtotal_bordado + subtotal_nombres + st.session_state.costo_delivery
        st.success(f"💳 Total Estimado = ${total_estimado:.2f}")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Atrás", use_container_width=True):
                st.session_state.paso = 3
                st.rerun()
        with col2:
            if st.button("✅ Confirmar Solicitud", key="confirmar_solicitud_mobile", use_container_width=True, disabled=st.session_state.solicitud_enviada):
                colegio_orden = "Múltiples Colegios" if len(st.session_state.colegios_agregados) > 1 else st.session_state.colegios_agregados[0]["colegio"]
                cantidad_total = sum(p["cantidad"] for c in st.session_state.colegios_agregados for p in c["prendas"])

                orden_id = guardar_orden(
                    st.session_state.nombre,
                    st.session_state.telefono,
                    st.session_state.correo,
                    colegio_orden,
                    cantidad_total,
                    st.session_state.tipo_logo,
                    st.session_state.nombre_bordado,
                    st.session_state.cantidad_nombre,
                    st.session_state.delivery,
                    st.session_state.zona_delivery,
                    fecha_entrega,
                    0,
                    subtotal_bordado,
                    subtotal_nombres,
                    st.session_state.costo_delivery,
                    0,
                    total_estimado,
                    "Recibido"
                )

                for colegio_data in st.session_state.colegios_agregados:
                    for prenda in colegio_data["prendas"]:
                        guardar_detalle(
                            orden_id,
                            colegio_data["colegio"],
                            prenda["tipo"],
                            prenda["talla"],
                            prenda["marca"],
                            prenda["color"],
                            int(prenda["cantidad"])
                        )

                try:
                    enviar_confirmacion_solicitud(
                        st.session_state.correo,
                        st.session_state.nombre,
                        orden_id,
                        fecha_entrega
                    )
                except Exception as e:
                    st.error(f"Error enviando correo: {e}")

                st.session_state.solicitud_enviada = True
                st.session_state.ultimo_pedido = orden_id
                st.rerun()

        if st.session_state.solicitud_enviada:
            st.success(f"✅ Pedido #{st.session_state.ultimo_pedido:04d} creado correctamente")
            st.success("📧 Correo de confirmación enviado.")
            st.info("Tu solicitud fue recibida correctamente.")

            if st.button("➕ Nueva Solicitud", key="nueva_solicitud_mobile", use_container_width=True):
                st.session_state.clear()
                st.rerun()

# --- MÓDULOS DE ADMINISTRACIÓN ---
elif pagina == "📋 Consultas":
    st.title("📋 Consulta de Órdenes")
    df_ordenes = obtener_ordenes()

    if df_ordenes.empty:
        st.info("ℹ️ No hay órdenes registradas en la base de datos.")
    else:
        excel_hist_file = generar_excel_historico(df_ordenes)
        with open(excel_hist_file, "rb") as f:
            st.download_button(
                "📊 Descargar Histórico General de Órdenes (Excel)",
                f,
                file_name=excel_hist_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="btn_descarga_historico_top"
            )

        st.divider()

        df_consulta = df_ordenes[["id", "nombre", "colegio", "status", "fecha_entrega", "saldo_pendiente", "fecha_pago"]].copy()
        df_consulta.columns = ["ID", "Cliente", "Colegio", "Estado", "Entrega", "Saldo", "Último Pago"]
        st.dataframe(df_consulta, use_container_width=True)

        pedido_id = st.selectbox("Seleccione un pedido", df_ordenes["id"].tolist())
        st.info(f"📦 Pedido seleccionado: #{pedido_id:04d}")

        pedido = obtener_orden_por_id(pedido_id).iloc[0]
        st.write(f"👤 {pedido['nombre']} | 📞 {pedido['telefono']} | 📧 {pedido['correo']}")

        detalle_orden = obtener_detalle_orden(pedido_id)
        with st.expander("👕 Prendas"):
            st.dataframe(detalle_orden, use_container_width=True)

        with st.expander("💰 Pagos y Tasa de Cambio (USD / Bs.)"):
            saldo = float(pedido.get("saldo_pendiente", 0))
            st.metric("Saldo Pendiente ($ USD)", f"${saldo:.2f}")

            tasa_actual = float(obtener_parametro("tasa_cambio") or 0.0)
            tasa_input = st.number_input("Tasa de Cambio (Bs / $)", min_value=0.0, value=tasa_actual, step=0.10, format="%.2f", key=f"tasa_pago_{pedido_id}")
            
            if tasa_input > 0 and saldo > 0:
                saldo_bs = saldo * tasa_input
                st.info(f"💡 **Saldo equivalente en Bolívares:** {saldo_bs:,.2f} Bs.")

            if pedido.get("fecha_pago"):
                st.caption(f"📅 Fecha del último pago registrado: {pedido.get('fecha_pago')}")

            if saldo <= 0:
                st.success("💳 Estado Pago: ✅ Pagado")
            else:
                st.warning(f"💳 Estado Pago: 🔴 Pendiente (${saldo:.2f})")

            monto_pago = st.number_input("Monto recibido ($ USD)", min_value=0.0, step=1.0, key=f"monto_in_{pedido_id}")
            
            if monto_pago > 0 and tasa_input > 0:
                monto_bs = round(monto_pago * tasa_input, 2)
                st.write(f"💵 **Equivalente del pago:** {monto_bs:,.2f} Bs.")

            if st.button("💾 Registrar Pago", key=f"reg_pago_{pedido_id}"):
                if monto_pago > saldo and saldo > 0:
                    st.error("❌ El pago excede el saldo pendiente.")
                elif monto_pago <= 0:
                    st.error("❌ Monto inválido.")
                else:
                    registrar_pago(pedido_id, monto_pago, tasa_input)
                    st.success("✅ Pago y registro en Bolívares guardados correctamente.")
                    st.rerun()

            # Mostrar histórico de pagos de esta orden en Bs.
            df_hist_pagos = obtener_historico_pagos(pedido_id)
            if not df_hist_pagos.empty:
                st.subheader("📜 Histórico de Pagos en Bolívares")
                st.dataframe(df_hist_pagos[["monto_usd", "tasa_cambio", "monto_bs", "fecha"]], use_container_width=True)

        with st.expander("📄 Documentos"):
            tasa_doc = st.number_input("Tasa para Comprobante PDF (Opcional)", min_value=0.0, value=float(obtener_parametro("tasa_cambio") or 0.0), step=0.10, key=f"tasa_pdf_{pedido_id}")
            
            if st.button("📄 Generar PDF"):
                pdf_file = generar_pdf_orden(pedido, detalle_orden, tasa_doc)
                with open(pdf_file, "rb") as f:
                    st.download_button("📥 Descargar PDF", f, file_name=pdf_file, mime="application/pdf")

            if st.button("📊 Generar Excel Pedido"):
                excel_file = generar_excel_orden(pedido, detalle_orden)
                with open(excel_file, "rb") as f:
                    st.download_button("📥 Descargar Excel Pedido", f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        with st.expander("📧 Comunicaciones"):
            if st.button("📧 Reenviar Correo"):
                pdf_file = generar_pdf_orden(pedido, detalle_orden)
                enviar_pdf_por_correo(pedido["correo"], pedido["nombre"], pedido["id"], pedido["fecha_entrega"], pdf_file)
                st.success("✅ Correo reenviado")

        with st.expander("🏭 Producción"):
            nuevo_estado = st.selectbox("Cambiar estado", ["Recibido", "En Producción", "Listo para Entrega", "Anulado"])
            if st.button("🔄 Actualizar Estado"):
                actualizar_status_orden(pedido_id, nuevo_estado)
                enviar_notificacion_estado(pedido["correo"], pedido["nombre"], pedido["id"], pedido["fecha_entrega"], nuevo_estado, pedido["delivery"])
                st.success("✅ Estado actualizado correctamente")
                st.rerun()

elif pagina == "⚙️ Configuración":
    st.title("⚙️ Configuración General")
    precio_nombre = st.number_input("Precio Bordado de Nombre", min_value=0.0, value=float(obtener_parametro("precio_nombre") or 0.0), step=0.50)
    dias_produccion = st.number_input("Días de Producción", min_value=1, value=int(obtener_parametro("dias_produccion") or 3), step=1)
    tasa_cambio = st.number_input("Tasa de Cambio Predeterminada (Bs / $)", min_value=0.0, value=float(obtener_parametro("tasa_cambio") or 0.0), step=0.50)

    if st.button("💾 Guardar Configuración"):
        guardar_parametro("precio_nombre", precio_nombre)
        guardar_parametro("dias_produccion", dias_produccion)
        guardar_parametro("tasa_cambio", tasa_cambio)
        st.success("✅ Configuración actualizada")

elif pagina == "🏫 Colegios":
    st.title("🏫 Gestión de Colegios")
    nombre_colegio = st.text_input("Nombre del Colegio")
    precio_colegio = st.number_input("Precio Bordado Colegio", min_value=0.0, step=0.50)

    if st.button("💾 Guardar Colegio"):
        if nombre_colegio:
            guardar_colegio(nombre_colegio, precio_colegio)
            st.success("✅ Colegio guardado/actualizado")
            st.rerun()
        else:
            st.error("Ingrese el nombre del colegio.")

    df_c = obtener_colegios()
    if not df_c.empty:
        st.divider()
        st.subheader("📋 Lista de Colegios Registrados")
        for _, fila in df_c.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"🏫 **{fila['nombre']}** - ${fila['precio_bordado']:.2f}")
            with c2:
                if st.button("🗑️", key=f"del_col_{fila['id']}"):
                    eliminar_colegio(fila['id'])
                    st.rerun()

elif pagina == "🚚 Delivery":
    st.title("🚚 Gestión de Delivery")
    nombre_zona = st.text_input("Nombre de la Zona")
    costo_zona = st.number_input("Costo Delivery", min_value=0.0, step=1.0)

    if st.button("💾 Guardar Zona Delivery"):
        if nombre_zona:
            guardar_zona_delivery(nombre_zona, costo_zona)
            st.success("✅ Zona Guardada/Actualizada")
            st.rerun()

    df_z = obtener_zonas_delivery()
    if not df_z.empty:
        st.divider()
        st.subheader("📋 Zonas Registradas")
        for _, fila in df_z.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"🚚 **{fila['nombre']}** - ${fila['costo']:.2f}")
            with c2:
                if st.button("🗑️", key=f"del_zona_{fila['nombre']}"):
                    eliminar_zona_delivery(fila['nombre'])
                    st.rerun()

elif pagina == "📦 Prendas":
    st.title("📦 Gestión de Prendas")
    tipo = st.text_input("Nombre Tipo Prenda")
    if st.button("💾 Guardar"):
        if tipo:
            guardar_tipo_prenda(tipo)
            st.rerun()
    
    df_items = obtener_tipos_prenda()
    if not df_items.empty:
        st.divider()
        for _, fila in df_items.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"👕 {fila['nombre']}")
            with c2:
                if st.button("🗑️", key=f"del_prenda_{fila['id']}"):
                    eliminar_tipo_prenda(fila['id'])
                    st.rerun()

elif pagina == "🏷️ Marcas":
    st.title("🏷️ Gestión de Marcas")
    marca = st.text_input("Marca")
    if st.button("💾 Guardar"):
        if marca:
            guardar_marca(marca)
            st.rerun()

    df_items = obtener_marcas()
    if not df_items.empty:
        st.divider()
        for _, fila in df_items.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"🏷️ {fila['nombre']}")
            with c2:
                if st.button("🗑️", key=f"del_marca_{fila['id']}"):
                    eliminar_marca(fila['id'])
                    st.rerun()

elif pagina == "📏 Tallas":
    st.title("📏 Gestión de Tallas")
    talla = st.text_input("Talla")
    if st.button("💾 Guardar"):
        if talla:
            guardar_talla(talla)
            st.rerun()

    df_items = obtener_tallas()
    if not df_items.empty:
        st.divider()
        for _, fila in df_items.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"📏 {fila['nombre']}")
            with c2:
                if st.button("🗑️", key=f"del_talla_{fila['id']}"):
                    eliminar_talla(fila['id'])
                    st.rerun()

elif pagina == "🎨 Colores":
    st.title("🎨 Gestión de Colores")
    color = st.text_input("Color")
    if st.button("💾 Guardar"):
        if color:
            guardar_color(color)
            st.rerun()

    df_items = obtener_colores()
    if not df_items.empty:
        st.divider()
        for _, fila in df_items.iterrows():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"🎨 {fila['nombre']}")
            with c2:
                if st.button("🗑️", key=f"del_color_{fila['id']}"):
                    eliminar_color(fila['id'])
                    st.rerun()

elif pagina == "💾 Respaldo":
    st.title("💾 Respaldo de Base de Datos")
    try:
        with open("bordaclick_dev.db", "rb") as f:
            st.download_button("📥 Descargar Base de Datos (DEV)", data=f, file_name="bordaclick_dev_backup.db", mime="application/octet-stream")
    except Exception as e:
        st.error(f"No se pudo cargar la base de datos de desarrollo: {e}")