import streamlit as st

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
    enviar_confirmacion_solicitud
)
from pdf_utils import generar_pdf_orden



st.set_page_config(
    page_title="Bordaclick Clientes",
    page_icon="🧵",
    layout="centered"
)

if "paso" not in st.session_state:
    st.session_state.paso = 1
    
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

        st.session_state.nombre = nombre
        st.session_state.telefono = telefono
        st.session_state.correo = correo

        st.session_state.paso = 2

        st.rerun()
# ==========================================
# PASO 2
# ==========================================

elif st.session_state.paso == 2:

    st.progress(40)

    st.subheader("🏫 Colegio y Prendas")

    lista_colegios = (
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
        obtener_tipos_prenda()["nombre"]
        .dropna()
        .tolist()
    )

    lista_tallas = (
        obtener_tallas()["nombre"]
        .dropna()
        .tolist()
    )

    lista_marcas = (
        obtener_marcas()["nombre"]
        .dropna()
        .tolist()
    )

    lista_colores = (
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

        st.session_state.prendas_actuales.append(
            {
                "tipo": tipo_prenda,
                "talla": talla,
                "marca": marca,
                "color": color,
                "cantidad": cantidad
            }
        )

        # st.session_state.tipo_prenda_actual = (
        #     lista_tipos_prenda[0]
        # )

        # st.session_state.talla_actual = (
        #     lista_tallas[0]
        # )

        # st.session_state.marca_actual = (
        #     lista_marcas[0]
        # )

        # st.session_state.color_actual = (
        #     lista_colores[0]
        # )

        # st.session_state.cantidad_actual = 1

        st.rerun()
    st.divider()

    st.subheader("📋 Prendas del Colegio")

    if len(st.session_state.prendas_actuales) == 0:

        st.info(
            "Aún no hay prendas agregadas."
        )

    else:

        for i, prenda in enumerate(
            st.session_state.prendas_actuales
        ):

            col1, col2 = st.columns([5,1])

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
                    key=f"eliminar_{i}"
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

    st.divider()

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

    st.progress(60)

    st.subheader("🧵 Bordado")

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

                st.session_state.paso = 4

                st.rerun()
# ==========================================
# PASO 4
# ==========================================

elif st.session_state.paso == 4:

    st.progress(80)

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
            st.session_state.paso = 3
            st.rerun()

    with col2:

        if st.button(
            "Continuar ➡️",
            use_container_width=True
        ):

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

    st.divider()

    st.subheader("🏫 Colegios y Prendas")

    for colegio_data in st.session_state.colegios_agregados:

        st.success(
            f"🏫 {colegio_data['colegio']}"
        )

        for prenda in colegio_data["prendas"]:

            st.write(
                f"• {prenda['tipo']} | "
                f"{prenda['talla']} | "
                f"{prenda['cantidad']}"
            )

    st.divider()

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

    st.divider()

    dias_produccion = int(
        obtener_parametro(
            "dias_produccion"
        ) or 3
    )

    fecha_entrega = (
        date.today() +
        timedelta(days=dias_produccion)
    )

    st.subheader("📅 Entrega")

    st.info(
        f"Fecha estimada de entrega: "
        f"{fecha_entrega.strftime('%d/%m/%Y')}"
    )

    st.divider()

    st.subheader("🚚 Delivery")

    st.write(
        f"Delivery: {st.session_state.delivery}"
    )

    if st.session_state.delivery == "Sí":

        st.write(
            f"Zona: {st.session_state.zona_delivery}"
        )

        st.write(
            f"Costo: ${st.session_state.costo_delivery:.2f}"
        )

    else:

        st.info(
            "📍 Retiro en tienda"
        )

    st.divider()

    st.subheader("💰 Resumen Financiero")

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
            st.session_state.paso = 4
            st.rerun()
    with col2:

        if st.button(
            "✅ Confirmar Solicitud",
            use_container_width=True
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

                st.success(
                    f"✅ Pedido #{orden_id:04d} creado correctamente"
                )

                st.success(
                    "📧 Correo de confirmación enviado."
                )

            except Exception as e:

                st.warning(
                    f"Pedido guardado correctamente, "
                    f"pero ocurrió un problema enviando el correo: {e}"
                )


