import streamlit as st
import pandas as pd
from datetime import (
    date,
    timedelta
)
from database import (
    obtener_colegios,
    obtener_tipos_prenda,
    obtener_tallas,
    obtener_marcas,
    obtener_colores,
    obtener_zonas_delivery,
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
    actualizar_status_orden,
    enviar_notificacion_estado,
    guardar_colegio,
    obtener_colegios
    )
from pdf_utils import (
    generar_pdf_orden,
    generar_excel_orden
)


st.set_page_config(
    page_title="Bordaclick Clientes",
    page_icon="🧵",
    layout="centered"
)

clave_admin = st.sidebar.text_input(
    "Clave Administrador",
    type="password"
)

opciones_menu = [
    "📝 Nueva Solicitud"
]

if clave_admin == "BordaAdmin2026*":

    opciones_menu.extend(
        [
            "📋 Consultas",
            "⚙️ Configuración",
            "🏫 Colegios"
        ]
    )


pagina = st.sidebar.selectbox(
    "Menú",
    opciones_menu
)

if "paso" not in st.session_state:
    st.session_state.paso = 1

if "solicitud_enviada" not in st.session_state:
    st.session_state.solicitud_enviada = False

if "colegios_agregados" not in st.session_state:
    st.session_state.colegios_agregados = []



# ==========================================
# ENCABEZADO
# ==========================================

col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "Logo Bordaclick.JPG",
        width=80
    )

with col2:
    st.title("🧵 Bordaclick")
    st.caption("Solicitud desde Celular")

st.divider()

if pagina == "📝 Nueva Solicitud":
# ==========================================
# PASO 1
# ==========================================


    if st.session_state.paso == 1:

        st.progress(20)

        st.subheader("👤 Datos del Cliente")

        nombre = st.text_input(
            "Nombre y Apellido"
        )

        telefono = st.text_input(
            "Teléfono"
        )

        correo = st.text_input(
            "Correo Electrónico"
        )
        if st.button(
            "Continuar ➡️",
            use_container_width=True
        ):

            if nombre == "":

                st.error(
                    "Debe ingresar el nombre."
                )

            elif telefono == "":

                st.error(
                    "Debe ingresar el teléfono."
                )

            elif correo == "":

                st.error(
                    "Debe ingresar el correo electrónico."
                )

            else:

                st.session_state.nombre = nombre

                st.session_state.telefono = telefono

                st.session_state.correo = correo

                st.session_state.paso = 2

                st.rerun()

    elif st.session_state.paso == 2:

        st.progress(40)

        st.subheader("🏫 Colegio y Prendas")

        lista_colegios = (
            ["Seleccione un colegio..."]
            +
            obtener_colegios()["nombre"]
            .dropna()
            .tolist()
        )    
        colegio = st.selectbox(
            "Seleccione el Colegio",
            lista_colegios
        )

        st.divider()

        lista_tipos_prenda = (
            ["Seleccione una prenda..."]
            +
            obtener_tipos_prenda()["nombre"]
            .dropna()
            .tolist()
        )
        lista_tallas = (
            ["Seleccione una talla..."]
            +
            obtener_tallas()["nombre"]
            .dropna()
            .tolist()
        )
        lista_marcas = (
            ["Seleccione una marca..."]
            +
            obtener_marcas()["nombre"]
            .dropna()
            .tolist()
        )
        lista_colores = (
            ["Seleccione un color..."]
            +
            obtener_colores()["nombre"]
            .dropna()
            .tolist()
        )    
        st.subheader("👕 Agregar Prenda")

        tipo_prenda = st.selectbox(
            "Tipo de Prenda",
            lista_tipos_prenda,
            key="tipo_prenda_actual"
        )

        talla = st.selectbox(
            "Talla",
            lista_tallas,
            key="talla_actual"
        )

        marca = st.selectbox(
            "Marca",
            lista_marcas,
            key="marca_actual"
        )

        color = st.selectbox(
            "Color",
            lista_colores,
            key="color_actual"
        )

        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            value=1,
            key="cantidad_actual"
        )

        if "prendas_actuales" not in st.session_state:
            st.session_state.prendas_actuales = []

        if st.button(
            "➕ Agregar Prenda",
            use_container_width=True
        ):

            if colegio == "Seleccione un colegio...":

                st.error(
                    "Debe seleccionar un colegio."
                )

            elif tipo_prenda == "Seleccione una prenda...":

                st.error(
                    "Debe seleccionar un tipo de prenda."
                )

            elif talla == "Seleccione una talla...":

                st.error(
                    "Debe seleccionar una talla."
                )

            elif marca == "Seleccione una marca...":

                st.error(
                    "Debe seleccionar una marca."
                )

            elif color == "Seleccione un color...":

                st.error(
                    "Debe seleccionar un color."
                )

            else:

                st.session_state.prendas_actuales.append(
                    {
                        "tipo": tipo_prenda,
                        "talla": talla,
                        "marca": marca,
                        "color": color,
                        "cantidad": cantidad
                    }
                )

                st.rerun()

        st.divider()

        st.subheader("📋Revise las prendas agregadas antes de guardar el colegio.")

        if len(st.session_state.prendas_actuales) == 0:

            st.info(
                "Aún no hay prendas agregadas."
            )

        else:

            for i, prenda in enumerate(
                st.session_state.prendas_actuales
            ):

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.success(
                        f"👕 {prenda['tipo']} | "
                        f"📏 {prenda['talla']} | "
                        f"🏷️ {prenda['marca']} | "
                        f"🎨 {prenda['color']} | "
                        f"🔢 {prenda['cantidad']}"
                    )

                with col2:

                    if st.button(
                        "🗑️",
                        key=f"borrar_prenda_{i}"
                    ):

                        st.session_state.prendas_actuales.pop(i)

                        st.rerun()

        st.divider()

        if st.button(
            "💾 Guardar Colegio",
            use_container_width=True
        ):

            if len(st.session_state.prendas_actuales) == 0:

                st.error(
                    "Debe agregar al menos una prenda."
                )

            else:
                st.session_state.colegios_agregados.append(
                    {
                        "colegio": colegio,
                        "prendas": st.session_state.prendas_actuales.copy()
                    }
                )

                st.session_state.prendas_actuales = []

                st.success(
                    "✅ Colegio guardado correctamente"
                )

                st.rerun()            

        st.subheader("🏫 Colegios Agregados")

        if len(st.session_state.colegios_agregados) == 0:

            st.info(
                "Aún no hay colegios guardados."
            )

        else:

            for colegio_data in st.session_state.colegios_agregados:

                st.success(
                    f"🏫 {colegio_data['colegio']}"
                )

                for prenda in colegio_data["prendas"]:

                    st.write(
                        f"• {prenda['tipo']} "
                        f"({prenda['talla']}) "
                        f"x {prenda['cantidad']}"
                    )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "➕ Agregar Otro Colegio",
                use_container_width=True
            ):
                st.rerun()

        with col2:

            if st.button(
                "Continuar ➡️",
                use_container_width=True
            ):


                if len(
                    st.session_state.colegios_agregados
                ) == 0:

                    st.error(
                        "Debe guardar al menos un colegio."
                    )

                else:

                    st.session_state.paso = 3

                    st.rerun()
                
# ==========================================
# PASO 3
# ==========================================

    elif st.session_state.paso == 3:

        st.progress(75)

        st.subheader("🧵 Bordado y Delivery")

        tipo_logo = st.selectbox(
            "Tipo de Logo",
            [
                "Diario",
                "Deporte",
                "Preescolar"
            ]
        )

        bordar_nombre = st.radio(
            "¿Desea bordar nombres?",
            [
                "Sí",
                "No"
            ]
        )

        nombre_bordado = ""

        cantidad_nombre = 0

        total_prendas = 0

        for colegio_data in st.session_state.colegios_agregados:

            for prenda in colegio_data["prendas"]:

                total_prendas += prenda["cantidad"]

        if bordar_nombre == "Sí":

            nombre_bordado = st.text_area(
                "Detalle del nombre a bordar por cada prenda Ejemplo: Sueter talla 10 colocar Miranda Guerrero detrás de la capucha letras blancas"
            )

            cantidad_nombre = st.number_input(
                "Cantidad de Prendas con Nombre",
                min_value=1,
                max_value=int(total_prendas),
                value=1
            )

            st.caption(
                f"Máximo permitido: {total_prendas} prendas"
            )

            if cantidad_nombre > total_prendas:

                st.error(
                    f"No puede bordar nombres en más de {total_prendas} prendas."
                )

        st.divider()

        st.subheader("🚚 Delivery")

        delivery = st.radio(
            "¿Desea Delivery?",
            [
                "Sí",
                "No"
            ]
        )

        zona_delivery = ""

        costo_delivery = 0

        if delivery == "Sí":

            lista_zonas = (
                obtener_zonas_delivery()["nombre"]
                .dropna()
                .tolist()
            )

            zona_delivery = st.selectbox(
                "Zona de Delivery",
                lista_zonas
            )

            try:

                costo_delivery = obtener_costo_delivery(
                    zona_delivery
                )

                st.success(
                    f"🚚 Costo Delivery: ${costo_delivery:.2f}"
                )

            except:

                st.warning(
                    "No se pudo obtener el costo del delivery."
                )

        else:

            st.info(
                "📍 Retiro en tienda"
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅️ Atrás",
                use_container_width=True
            ):
                st.session_state.paso = 2
                st.rerun()

        with col2:

            if st.button(
                "Continuar ➡️",
                use_container_width=True
            ):

                if (
                    bordar_nombre == "Sí"
                    and cantidad_nombre > total_prendas
                ):

                    st.error(
                        f"No puede bordar nombres en más de {total_prendas} prendas."
                    )

                else:

                    st.session_state.tipo_logo = tipo_logo

                    st.session_state.bordar_nombre = bordar_nombre

                    st.session_state.nombre_bordado = nombre_bordado

                    st.session_state.cantidad_nombre = cantidad_nombre

                    st.session_state.delivery = delivery

                    st.session_state.zona_delivery = zona_delivery

                    st.session_state.costo_delivery = costo_delivery

                    st.session_state.paso = 5

                    st.rerun()                


# ==========================================
# PASO 5
# ==========================================

    elif st.session_state.paso == 5:

        st.progress(100)

        st.subheader("📋 Resumen de la Solicitud")

        st.success(
            f"👤 {st.session_state.nombre}"
        )

        st.write(
            f"📞 {st.session_state.telefono}"
        )

        st.write(
            f"📧 {st.session_state.correo}"
        )

    #    st.divider()
        st.progress(100)
        st.subheader("🧵 Bordado")

        st.write(
            f"Tipo Logo: {st.session_state.tipo_logo}"
        )

        st.write(
            f"Bordar Nombre: {st.session_state.bordar_nombre}"
        )

        if st.session_state.bordar_nombre == "Sí":

            st.write(
                f"Nombres: {st.session_state.nombre_bordado}"
            )

            st.write(
                f"Cantidad: {st.session_state.cantidad_nombre}"
            )
        dias_produccion = int(
            obtener_parametro(
                "dias_produccion"
            ) or 3
        )

        fecha_entrega = (
            date.today() +
            timedelta(days=dias_produccion)
        )
        st.progress(100)
    #    st.divider()

        st.subheader("💰 Resumen Financiero")

        st.write(
            f"📅 Entrega: "
            f"{fecha_entrega.strftime('%d/%m/%Y')}"
        )

        subtotal_bordado = 0

        for colegio_data in st.session_state.colegios_agregados:

            colegio_nombre = colegio_data["colegio"]

            cantidad_colegio = 0

            for prenda in colegio_data["prendas"]:

                cantidad_colegio += prenda["cantidad"]

            precio_colegio = obtener_precio_colegio(
                colegio_nombre
            )

            if cantidad_colegio >= 6:

                precio_colegio = max(
                    0,
                    precio_colegio - 0.50
                )

            subtotal_colegio = (
                cantidad_colegio *
                precio_colegio
            )

            subtotal_bordado += subtotal_colegio

            if cantidad_colegio >= 6:

                st.write(
                    f"🏫 {colegio_nombre} | "
                    f"🎉 Promoción aplicada"
                )

            else:

                st.write(
                    f"🏫 {colegio_nombre}"
                )

            st.write(
                f"👕 {cantidad_colegio} prendas x "
                f"${precio_colegio:.2f} = "
                f"${subtotal_colegio:.2f}"
            )

        precio_nombre = float(
            obtener_parametro(
                "precio_nombre"
            ) or 0
        )

        subtotal_nombres = 0

        if st.session_state.bordar_nombre == "Sí":

            subtotal_nombres = (
                st.session_state.cantidad_nombre
                *
                precio_nombre
            )

            st.write(
                f"🔤 {st.session_state.cantidad_nombre} nombres "
                f"x ${precio_nombre:.2f} = "
                f"${subtotal_nombres:.2f}"
            )

        st.write(
            f"🚚 Delivery = "
            f"${st.session_state.costo_delivery:.2f}"
        )

        total_estimado = (
            subtotal_bordado
            +
            subtotal_nombres
            +
            st.session_state.costo_delivery
        )

        st.success(
            f"💳 Total Estimado = "
            f"${total_estimado:.2f}"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅️ Atrás",
                use_container_width=True
            ):
                st.session_state.paso = 3
                st.rerun()

        with col2:

            if st.button(
                "✅ Confirmar Solicitud",
                key="confirmar_solicitud_mobile",
                use_container_width=True,
                disabled=st.session_state.solicitud_enviada
            ):

                if len(st.session_state.colegios_agregados) > 1:

                    colegio_orden = "Múltiples Colegios"

                else:

                    colegio_orden = (
                        st.session_state.colegios_agregados[0]["colegio"]
                    )

                cantidad_total = 0

                for colegio_data in st.session_state.colegios_agregados:

                    for prenda in colegio_data["prendas"]:

                        cantidad_total += prenda["cantidad"]

                status = "Recibido"

                abono = 0

                saldo_pendiente = total_estimado

                precio_bordado = 0

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
                    precio_bordado,
                    subtotal_bordado,
                    subtotal_nombres,
                    st.session_state.costo_delivery,
                    abono,
                    saldo_pendiente,
                    status
                )

                for colegio_data in st.session_state.colegios_agregados:

                    colegio_nombre = colegio_data["colegio"]

                    for prenda in colegio_data["prendas"]:

                        guardar_detalle(
                            orden_id,
                            colegio_nombre,
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

                    st.error(
                        f"Error enviando correo: {e}"
                    )

                st.session_state.solicitud_enviada = True
                st.session_state.ultimo_pedido = orden_id

                st.rerun()
            if st.session_state.solicitud_enviada:

                st.empty()

                st.success(
                    f"✅ Pedido #{st.session_state.ultimo_pedido:04d} creado correctamente"
                )

                st.success(
                    "📧 Correo de confirmación enviado."
                )

                st.info(
                    "Tu solicitud fue recibida correctamente y será revisada por nuestro equipo."
                )

                if st.button(
                    "➕ Nueva Solicitud",
                    key="nueva_solicitud_mobile",
                    use_container_width=True
                ):

                    st.session_state.clear()

                    st.rerun()
            st.stop()
if pagina == "📋 Consultas":

    st.title(
        "📋 Consulta de Órdenes"
    )

    df_ordenes = obtener_ordenes()

    df_consulta = df_ordenes[
        [
            "id",
            "nombre",
            "colegio",
            "status",
            "fecha_entrega",
            "saldo_pendiente"
        ]
    ].copy()

    df_consulta.columns = [
        "ID",
        "Cliente",
        "Colegio",
        "Estado",
        "Entrega",
        "Saldo"
    ]

    st.dataframe(
        df_consulta,
        use_container_width=True
    )
    pedido_id = st.selectbox(
        "Seleccione un pedido",
        df_ordenes["id"].tolist()
    )

    st.info(
        f"📦 Pedido seleccionado: #{pedido_id:04d}"
    )
    pedido = obtener_orden_por_id(
        pedido_id
    )

    pedido = pedido.iloc[0]

    estado = pedido["status"]

    if estado == "Recibido":

        st.warning(
            "🟡 Estado: Recibido"
        )

    elif estado == "En Producción":

        st.info(
            "🔵 Estado: En Producción"
        )

    elif estado == "Listo para Entrega":

        st.success(
            "🟢 Estado: Listo para Entrega"
        )

    elif estado == "Anulado":

        st.error(
            "🔴 Estado: Anulado"
        )

    st.info(
        f"👤 {pedido['nombre']} | "
        f"📞 {pedido['telefono']} | "
        f"📧 {pedido['correo']}"
    )    
    detalle_orden = obtener_detalle_orden(
        pedido_id
    )

    with st.expander(
        "👕 Prendas"
    ):

        st.dataframe(
            detalle_orden,
            use_container_width=True
        )
    with st.expander(
        "💰 Pagos"
    ):

        saldo = float(
            pedido.get(
                "saldo_pendiente",
                0
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Saldo",
                f"${saldo:.2f}"
            )

        with col2:

            st.metric(
                "Total",
                f"${saldo:.2f}"
            )

        if saldo <= 0:

            st.success(
                "💳 Estado Pago: ✅ Pagado"
            )

        else:

            st.warning(
                f"💳 Estado Pago: 🔴 Pendiente (${saldo:.2f})"
            )

            st.divider()

            monto_pago = st.number_input(
                "Monto recibido",
                min_value=0.0,
                step=1.0
            )

            if st.button(
                "💾 Registrar Pago",
                key=f"registrar_pago_{pedido_id}"
            ):

                if monto_pago > saldo:

                    st.error(
                        "❌ El pago no puede exceder el saldo pendiente."
                    )

                elif monto_pago <= 0:

                    st.error(
                        "❌ Debe ingresar un monto válido."
                    )

                else:

                    registrar_pago(
                        pedido_id,
                        monto_pago
                    )

                    st.success(
                        "✅ Pago registrado correctamente."
                    )

                    st.rerun()                    
        with st.expander(
            "📄 Documentos"
        ):

            if st.button(
                "📄 Generar PDF"
            ):

                detalle_orden = obtener_detalle_orden(
                    pedido_id
                )

                pdf_file = generar_pdf_orden(
                    pedido,
                    detalle_orden
                )

                st.success(
                    "✅ PDF generado"
                )

                with open(
                    pdf_file,
                    "rb"
                ) as archivo:

                    st.download_button(
                        "📥 Descargar PDF",
                        archivo,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

            st.divider()

            if st.button(
                "📊 Generar Excel Pedido"
            ):

                detalle_orden = obtener_detalle_orden(
                    pedido_id
                )

                excel_file = generar_excel_orden(
                    pedido,
                    detalle_orden
                )

                st.success(
                    "✅ Excel generado"
                )

                with open(
                    excel_file,
                    "rb"
                ) as archivo:

                    st.download_button(
                        "📥 Descargar Excel Pedido",
                        archivo,
                        file_name=excel_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            st.divider()
        if st.button(
            "📋 Generar Excel Bordaclick Ordenes"
        ):

            df_ordenes_excel = obtener_ordenes()

            excel_nombre = "Bordaclick_Ordenes.xlsx"

            with pd.ExcelWriter(
                excel_nombre,
                engine="openpyxl"
            ) as writer:

                df_ordenes_excel.to_excel(
                    writer,
                    index=False,
                    sheet_name="Ordenes"
                )

            st.success(
                "✅ Excel general generado"
            )

            with open(
                excel_nombre,
                "rb"
            ) as archivo:

                st.download_button(
                    "📥 Descargar Excel Bordaclick Ordenes",
                    data=archivo,
                    file_name=excel_nombre,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    with st.expander(
        "📧 Comunicaciones"
    ):

        st.info(
            f"Correo registrado: {pedido['correo']}"
        )

        if st.button(
            "📧 Reenviar Correo"
        ):

            detalle_orden = obtener_detalle_orden(
                pedido_id
            )

            pdf_file = generar_pdf_orden(
                pedido,
                detalle_orden
            )

            enviar_pdf_por_correo(
                pedido["correo"],
                pedido["nombre"],
                pedido["id"],
                pedido["fecha_entrega"],
                pdf_file
            )

            st.success(
                "✅ Correo enviado correctamente"
            )
    with st.expander(
        "🏭 Producción"
    ):

        if st.session_state.get(
            "estado_actualizado",
            False
        ):

            st.success(
                "✅ Estado actualizado correctamente"
            )

            st.session_state["estado_actualizado"] = False

        st.write(
            f"Estado actual: {pedido['status']}"
        )

        estados = [
            "Recibido",
            "En Producción",
            "Listo para Entrega",
            "Anulado"
        ]

        indice_estado = (
            estados.index(pedido["status"])
            if pedido["status"] in estados
            else 0
        )

        nuevo_estado = st.selectbox(
            "Cambiar estado",
            estados,
            index=indice_estado
        )

        if st.button(
            "🔄 Actualizar Estado",
            key=f"actualizar_estado_{pedido_id}"
        ):

            actualizar_status_orden(
                pedido_id,
                nuevo_estado
            )

            if nuevo_estado in [
                "En Producción",
                "Listo para Entrega"
            ]:

                enviar_notificacion_estado(
                    pedido["correo"],
                    pedido["nombre"],
                    pedido["id"],
                    pedido["fecha_entrega"],
                    nuevo_estado,
                    pedido["delivery"]
                )

            st.session_state[
                "estado_actualizado"
            ] = True

            st.rerun()

        st.divider()

        st.write(
            f"📅 Entrega: {pedido['fecha_entrega']}"
        )

        st.write(
            f"🚚 Delivery: {pedido['delivery']}"
        )

        st.write(
            f"📍 Zona: {pedido['zona_delivery']}"
        )
if pagina == "⚙️ Configuración":

    st.title(
        "⚙️ Configuración General"
    )

    precio_nombre = st.number_input(
        "Precio Bordado de Nombre",
        min_value=0.0,
        value=float(
            obtener_parametro(
                "precio_nombre"
            )
        ),
        step=0.50
    )

    dias_produccion = st.number_input(
        "Días de Producción",
        min_value=1,
        value=int(
            obtener_parametro(
                "dias_produccion"
            ) or 3
        ),
        step=1
    )

    if st.button(
        "💾 Guardar Configuración"
    ):

        guardar_parametro(
            "precio_nombre",
            precio_nombre
        )

        guardar_parametro(
            "dias_produccion",
            dias_produccion
        )

        st.success(
            "✅ Configuración actualizada"
        )
if pagina == "🏫 Colegios":

    st.title(
        "🏫 Gestión de Colegios"
    )

    df_colegios = obtener_colegios()

    st.subheader(
        "📚 Agregar Colegio"
    )

    nombre_colegio = st.text_input(
        "Nombre del Colegio"
    )

    precio_colegio = st.number_input(
        "Precio Bordado Colegio",
        min_value=0.0,
        step=0.50
    )

    if st.button(
        "💾 Guardar Colegio"
    ):

        if nombre_colegio == "":

            st.error(
                "Debe ingresar el nombre del colegio."
            )

        else:

            guardar_colegio(
                nombre_colegio,
                precio_colegio
            )

            st.success(
                "✅ Colegio guardado"
            )

            st.rerun()

    st.divider()

    st.subheader(
        "📚 Colegios Registrados"
    )

    st.dataframe(
        df_colegios,
        use_container_width=True
    )    
        
                                