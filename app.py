import streamlit as st
import re
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from openpyxl.styles import Border, Side


from openpyxl import Workbook
from datetime import date,timedelta
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
import os

from database import (
    crear_bd,
    guardar_orden,
    guardar_detalle,
    guardar_precio_bordado,
    obtener_precio_bordado,
    obtener_catalogo_bordados,
    guardar_catalogo_bordados,
    guardar_parametro,
    obtener_parametro,
    obtener_ordenes,
    obtener_orden_por_id,
    obtener_detalle_orden,
    actualizar_status_orden,
    guardar_colegio,
    obtener_colegios,
    obtener_precio_colegio,
    guardar_tipo_prenda,
    obtener_tipos_prenda,
    guardar_marca,
    obtener_marcas,
    guardar_color,
    obtener_colores,
    guardar_talla,
    obtener_tallas,
    guardar_color,
    obtener_colores,
    registrar_pago,
    enviar_pdf_por_correo,
    guardar_zona_delivery,
    obtener_zonas_delivery,
    obtener_costo_delivery,
    enviar_notificacion_estado,
    contar_pedidos_pendientes,
)          



st.set_page_config(
    page_title="Bordaclick",
    page_icon="🧵",
    layout="wide"
)

crear_bd()

st.image(

    "Logo Bordaclick.JPG",
    width=250
)


colegios = [
    "San Ignacio",
    "Colegio Don Bosco - Altamira",
    "Colegio Simón Bolívar",
    "IEA",
    "Colegio Valle Abierto",
    "Colegio Santiago de León"
]

clave_admin = st.sidebar.text_input(
    "Clave Administrador",
    type="password"
)

#st.write(repr(clave_admin))


opciones_menu = [
    "Nueva Solicitud"
]

if clave_admin == "BordaAdmin2026*":


    opciones_menu.append(
        "Consultas"
    )

    opciones_menu.append(
        "Catálogo de Bordados"
    )
elif clave_admin:

    st.sidebar.error(
        "❌ Contraseña inválida"
    )

pagina = st.sidebar.selectbox(
    "Menú Principal",
    opciones_menu
)


if pagina == "Catálogo de Bordados":

    st.title("🗂️ Administración de Catálogos")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "⚙️ Configuración",
        "🏫 Colegios",
        "🚚 Delivery",
        "📦 Prendas",
        "🏷️ Marcas",
        "📏 Tallas",
        "🎨 Colores",
        "💾 Respaldo"
    ])
    
    with tab1:

        st.subheader(
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
    

    with tab2:

        st.subheader(
            "📚 Agregar Colegio"
        )
        df_colegios = obtener_colegios()

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

            guardar_colegio(
                nombre_colegio,
                precio_colegio
            )

            st.success(
                "✅ Colegio guardado"
            )

        st.subheader(
            "📚 Colegios Registrados"
        )
        st.dataframe(
            df_colegios,
            use_container_width=True
        )        

    with tab3:

        st.subheader(
            "🚚 Agregar Zona Delivery"
        )

        nombre_zona = st.text_input(
            "Nombre de la Zona"
        )

        costo_zona = st.number_input(
            "Costo Delivery",
            min_value=0.0,
            step=1.0
        )

        if st.button(
            "💾 Guardar Zona Delivery"
        ):

            guardar_zona_delivery(
                nombre_zona,
                costo_zona
            )

            st.success(
                "✅ Zona Delivery guardada"
            )

        df_zonas = obtener_zonas_delivery()

        st.subheader(
            "🚚 Zonas Delivery Registradas"
        )
        st.dataframe(
            df_zonas,
            use_container_width=True
        )

    with tab4:

        st.subheader(
            "📦 Agregar Tipo de Prenda"
        )

        nombre_tipo_prenda = st.text_input(
            "Nombre del Tipo de Prenda"
        )

        if st.button(
            "💾 Guardar Tipo de Prenda"
        ):

            guardar_tipo_prenda(
                nombre_tipo_prenda
            )

            st.success(
                "✅ Tipo de Prenda guardado"
            )

        st.subheader(
            "📦 Tipos de Prenda Registrados"
        )
        df_tipos_prenda = obtener_tipos_prenda()

        st.dataframe(
            df_tipos_prenda,
            use_container_width=True
        )        
        st.divider()
    with tab5:

        st.subheader(
            "🏷️ Agregar Marca"
        )

        nombre_marca = st.text_input(
            "Nombre de la Marca"
        )

        if st.button(
            "💾 Guardar Marca"
        ):

            guardar_marca(
                nombre_marca
            )

            st.success(
                "✅ Marca guardada"
            )

        st.subheader(
            "🏷️ Marcas Registradas"
        )
        df_marcas = obtener_marcas()

        st.dataframe(
            df_marcas,
            use_container_width=True
        )
        st.divider()

    with tab6:

        st.subheader(
            "📏 Agregar Talla"
        )

        nombre_talla = st.text_input(
            "Nombre de la Talla"
        )

        if st.button(
            "💾 Guardar Talla"
        ):

            guardar_talla(
                nombre_talla
            )

            st.success(
                "✅ Talla guardada"
            )

        st.subheader(
            "📏 Tallas Registradas"
        )

        df_tallas = obtener_tallas()

        st.dataframe(
            df_tallas,
            use_container_width=True
        )

        st.divider()

    with tab7:

        st.subheader(
            "🎨 Agregar Color"
        )

        nombre_color = st.text_input(
            "Nombre del Color"
        )

        if st.button(
            "💾 Guardar Color"
        ):

            guardar_color(
                nombre_color
            )

            st.success(
                "✅ Color guardado"
            )

        st.subheader(
            "🎨 Colores Registrados"
        )

        df_colores = obtener_colores()

        st.dataframe(
            df_colores,
            use_container_width=True
        )
                     
    with tab8:

        st.subheader(
            "💾 Respaldo Base de Datos"
        )

        st.info(
            "Descarga una copia completa de la base de datos actual de Bordaclick."
        )

        with open(
            "bordaclick.db",
            "rb"
        ) as archivo:

            st.download_button(
                label="📥 Descargar Base de Datos",
                data=archivo,
                file_name="bordaclick_backup.db",
                mime="application/octet-stream"
            )
        
def generar_pdf_orden(
    orden,
    detalle_orden
):

    nombre_pdf = f"Pedido_{int(orden['id']):04d}.pdf"

    doc = SimpleDocTemplate(nombre_pdf)

    estilos = getSampleStyleSheet()

    elementos = []

    logo = Image(
        "Logo Bordaclick.JPG",
        width=150,
        height=80
    )

    elementos.append(
        logo
    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "ORDEN DE SERVICIO",
            estilos["Heading1"]
        )
    )

    # titulo = Table(
    #     [
    #         ["BORDACLICK"],
    #         ["ORDEN DE SERVICIO"]
    #     ],
    #     colWidths=[300]
    # )

    # titulo.setStyle(
    #     TableStyle([

    #         ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

    #         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

    #         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

    #         ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),

    #         ("FONTSIZE", (0, 0), (-1, 0), 18),

    #         ("FONTSIZE", (0, 1), (-1, 1), 12),

    #         ("ALIGN", (0, 0), (-1, -1), "CENTER"),

    #         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    #         ("TOPPADDING", (0, 0), (-1, 0), 8),

    #         ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

    #         ("GRID", (0, 0), (-1, -1), 1, colors.black)

    #     ])
    # )

    # elementos.append(
    #     titulo
    # )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Spacer(1, 8)
    )

    elementos.append(
        Paragraph(
            f"Pedido #{int(orden['id']):04d}",
            estilos["Heading3"]
        )
    )

    tabla_estado = Table(
        [
            ["Estado", "Fecha Entrega"],
            [
                str(orden["status"]),
                str(orden["fecha_entrega"])
            ]
        ],
        colWidths=[120, 180]
    )

    tabla_estado.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    elementos.append(
        tabla_estado
    )

    elementos.append(
        Spacer(1, 8)
    )
    elementos.append(
        Paragraph(
            " ",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "DATOS DEL CLIENTE",
            estilos["Heading3"]
        )
    )


    elementos.append(
        Paragraph(
            f"Nombre: {orden['nombre']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Telefono: {orden['telefono']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Correo: {orden['correo']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Colegio: {orden['colegio']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            " ",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "DATOS DE PRODUCCION",
            estilos["Heading3"]
        )
    )
  

    elementos.append(
        Paragraph(
            f"Tipo de Logo: {orden['tipo_logo']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Cantidad Total: {orden['cantidad_total']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Nombre Bordado: {orden['nombre_bordado']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Cantidad con Nombre: {orden['cantidad_nombre']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            " ",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "RESUMEN FINANCIERO",
            estilos["Heading3"]
        )
    )

    total_general = (
        orden["subtotal_bordado"]
        + orden["subtotal_nombres"]
        + orden["delivery_costo"]
    )

    tabla_financiera = Table([
        ["Concepto", "Monto"],
        ["Precio Bordado", f"${orden['precio_bordado']:.2f}"],
        ["Subtotal Bordado", f"${orden['subtotal_bordado']:.2f}"],
        ["Subtotal Nombres", f"${orden['subtotal_nombres']:.2f}"],
        ["Delivery", f"${orden['delivery_costo']:.2f}"],
        ["Total General", f"${total_general:.2f}"],
        ["Abono", f"${orden['abono']:.2f}"],
        ["Saldo Pendiente", f"${orden['saldo_pendiente']:.2f}"]
    ])

    tabla_financiera.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("BACKGROUND", (0, -1), (-1, -1), colors.yellow),

            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),

            ("ALIGN", (1, 1), (1, -1), "RIGHT")

        ])
    )

    elementos.append(
        tabla_financiera
    )

    total_general = (
        orden["subtotal_bordado"]
        + orden["subtotal_nombres"]
        + orden["delivery_costo"]
    )

    elementos.append(
        Paragraph(
            " ",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "DESGLOSE DE PRENDAS",
            estilos["Heading3"]
        )
    )

    datos_tabla = [
        [
            "Tipo Prenda",
            "Talla",
            "Marca",
            "Color",
            "Cantidad"
        ]
    ]

    for _, fila in detalle_orden.iterrows():

        datos_tabla.append(
            [
                str(fila["tipo_prenda"]),
                str(fila["talla"]),
                str(fila["marca"]),
                str(fila["color"]),
                str(fila["cantidad"])
            ]
        )

    tabla = Table(
        datos_tabla,
        colWidths=[90, 40, 90, 90, 50]
    )

    tabla.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("ALIGN", (1, 1), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")

        ])
    )

    elementos.append(tabla)
    
    elementos.append(
        Spacer(1, 15)
    )

    elementos.append(
        Paragraph(
            "Bordaclick Diseños",
            estilos["Heading3"]
        )
    )

    elementos.append(
        Paragraph(
            "Sistema de Gestión de Bordados Escolares",
            estilos["Normal"]
        )
    )

    doc.build(elementos)

    return nombre_pdf


def generar_excel_orden(
    orden,
    detalle_orden
):


    nombre_excel = f"Pedido_{int(orden['id']):04d}.xlsx"

    wb = Workbook()

    ws = wb.active
    
    titulo = Font(
    bold=True
    )
    titulo_blanco = Font(
    bold=True,
    color="FFFFFF"
    )

    fondo_azul = PatternFill(
        fill_type="solid",
        start_color="ADD8E6"
    )
        
    borde = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
    )
    fondo_gris = PatternFill(
    fill_type="solid",
    start_color="D9D9D9",
    end_color="D9D9D9"
    )

    
    ws["A1"].font = titulo_blanco
    ws["A2"].font = titulo_blanco

    ws["A1"].fill = fondo_azul
    ws["A2"].fill = fondo_azul   
     
    ws.title = "Orden_Servicio"
    ws.merge_cells("A1:E1")
    ws.merge_cells("A2:E2")

    ws["A1"] = "BORDACLICK"
    ws["A2"] = "ORDEN DE SERVICIO"

    ws["A4"] = "Pedido"
    ws["B4"] = f"#{int(orden['id']):04d}"

    ws["A5"] = "Estado"
    ws["B5"] = orden["status"]

    ws["A6"] = "Fecha Entrega"
    ws["B6"] = str(orden["fecha_entrega"])
    ws["A8"] = "DATOS DEL CLIENTE"

    ws["A9"] = "Nombre"
    ws["B9"] = orden["nombre"]

    ws["A10"] = "Telefono"
    ws["B10"] = orden["telefono"]

    ws["A11"] = "Correo"
    ws["B11"] = orden["correo"]

    ws["A12"] = "Colegio"
    ws["B12"] = orden["colegio"]
    ws["A14"] = "DATOS DE PRODUCCION"

    ws["A15"] = "Tipo Logo"
    ws["B15"] = orden["tipo_logo"]

    ws["A16"] = "Cantidad Total"
    ws["B16"] = orden["cantidad_total"]

    ws["A17"] = "Nombre Bordado"
    ws["B17"] = orden["nombre_bordado"]

    ws["A18"] = "Cantidad con Nombre"
    ws["B18"] = orden["cantidad_nombre"]
    ws["A20"] = "RESUMEN FINANCIERO"

    ws["A21"] = "Subtotal Bordado"
    ws["B21"] = orden["subtotal_bordado"]

    ws["A22"] = "Subtotal Nombres"
    ws["B22"] = orden["subtotal_nombres"]

    ws["A23"] = "Delivery"
    ws["B23"] = orden["delivery_costo"]

    ws["A24"] = "Abono"
    ws["B24"] = orden["abono"]

    ws["A25"] = "Saldo Pendiente"
    ws["B25"] = orden["saldo_pendiente"]
    ws["A27"] = "DESGLOSE DE PRENDAS"
    
    ws["A1"].font = titulo
    ws["A2"].font = titulo

    ws["A8"].font = titulo

    ws["A14"].font = titulo

    ws["A20"].font = titulo

    ws["A27"].font = titulo

    ws["A28"] = "Tipo Prenda"
    ws["B28"] = "Talla"
    ws["C28"] = "Marca"
    ws["D28"] = "Color"
    ws["E28"] = "Cantidad"
    fila_excel = 29

    for _, fila in detalle_orden.iterrows():

        ws[f"A{fila_excel}"] = fila["tipo_prenda"]
        ws[f"B{fila_excel}"] = fila["talla"]
        ws[f"C{fila_excel}"] = fila["marca"]
        ws[f"D{fila_excel}"] = fila["color"]
        ws[f"E{fila_excel}"] = fila["cantidad"]

        fila_excel += 1
    encabezado_tabla = Font(
        bold=True
    )

    ws["A28"].font = encabezado_tabla
    ws["B28"].font = encabezado_tabla
    ws["C28"].font = encabezado_tabla
    ws["D28"].font = encabezado_tabla
    ws["E28"].font = encabezado_tabla
    ws["A28"].fill = fondo_gris
    ws["B28"].fill = fondo_gris
    ws["C28"].fill = fondo_gris
    ws["D28"].fill = fondo_gris
    ws["E28"].fill = fondo_gris

 
    for fila in ws.iter_rows(
        min_row=28,
        max_row=fila_excel - 1,
        min_col=1,
        max_col=5
    ):

        for celda in fila:

            celda.border = borde
    
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 15    

    wb.save(nombre_excel)

    return nombre_excel
        
if pagina == "Consultas":

    st.title(
        "📋 Consulta de Órdenes"
    )

    pendientes = contar_pedidos_pendientes()

    if pendientes > 0:

        st.warning(
            f"🔔 Tienes {pendientes} pedidos nuevos por revisar"
        )

    else:

        st.success(
            "✅ No hay pedidos nuevos pendientes"
        )

    df_ordenes = obtener_ordenes()

    st.dataframe(
        df_ordenes,
        use_container_width=True
    )

    if st.button(
        "📊 Exportar Excel"
    ):

        archivo_excel = "Bordaclick_Ordenes.xlsx"

        with pd.ExcelWriter(
            archivo_excel,
            engine="openpyxl"
        ) as writer:

            df_ordenes.to_excel(
                writer,
                sheet_name="Historico",
                index=False
            )

            hoja = writer.sheets["Historico"]

            for columna in hoja.columns:

                longitud = 0

                for celda in columna:

                    valor = str(celda.value)

                    if len(valor) > longitud:

                        longitud = len(valor)

                hoja.column_dimensions[
                    columna[0].column_letter
                ].width = longitud + 5

        st.success(
            f"✅ Excel generado: {archivo_excel}"
        )

        with open(
            archivo_excel,
            "rb"
        ) as archivo:

            st.download_button(
                "📊 Descargar Histórico",
                data=archivo.read(),
                file_name=archivo_excel,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    if not df_ordenes.empty:

        orden_seleccionada = st.selectbox(
            "Seleccione una Orden",
            df_ordenes["id"]
        )

        datos_orden = obtener_orden_por_id(
            orden_seleccionada
        )

        detalle_orden = obtener_detalle_orden(
            orden_seleccionada
        )

        orden = datos_orden.iloc[0]        
     

        st.divider()

        st.header(
            f"📋 Pedido #{int(orden['id']):04d}"
        )
        
        if orden["saldo_pendiente"] <= 0:

            st.success(
                "🟢 Estado de Pago: Pagado"
            )

        else:

            st.warning(
                "🔴 Estado de Pago: No Pagado"
            )    
            
        col1, col2 = st.columns(2)

        with col1:

            estados = [
                "Recibido",
                "En Producción",
                "En Revisión del Cliente",
                "Listo para Entrega",
                "Entregado",
                "Anulado"
            ]

            estado_actual = orden["status"]

            indice_estado = estados.index(
                estado_actual
            ) if estado_actual in estados else 0

            estado = st.selectbox(
                "Estado",
                estados,
                index=indice_estado
            )
            st.subheader(
                "💰 Registrar Pago"
            )

            monto_pago = st.number_input(
                "Monto del Pago",
                min_value=0.0,
                step=1.0
            )

            if st.button(
                "💰 Registrar Pago"
            ):

                registrar_pago(
                    int(orden["id"]),
                    monto_pago
                )

                st.success(
                    "✅ Pago registrado"
                )

                st.rerun()
            if st.button(
                "💾 Actualizar Estado"
            ):

                actualizar_status_orden(
                    int(orden["id"]),
                    estado
                )

                correo_cliente = str(
                    orden["correo"]
                ).strip()

                if (
                    correo_cliente
                    and
                    "@" in correo_cliente
                ):

                    enviar_notificacion_estado(
                        correo_cliente,
                        orden["nombre"],
                        int(orden["id"]),
                        orden["fecha_entrega"],
                        estado
                    )

                else:

                    st.info(
                        "ℹ️ Este cliente no tiene un correo válido. No se enviará notificación."
                    )

                st.success(
                    "✅ Estado actualizado"
                )

   
        with col2:

            st.info(
                f"Fecha Entrega: {orden['fecha_entrega']}"
            )

        st.header(
            "📋 Orden de Servicio Bordaclick"
        )
 
        if st.button(
            "🖨️ Generar PDF"
        ):

            nombre_pdf = generar_pdf_orden(
                orden,
                detalle_orden
            )
            enviar_pdf_por_correo(
                orden["correo"],
                orden["nombre"],
                int(orden["id"]),
                orden["fecha_entrega"],
                nombre_pdf
            )

            st.success(
                "✅ Correo enviado"
            )
            with open(
                nombre_pdf,
                "rb"
            ) as archivo_pdf:

                st.download_button(
                    "📄 Descargar PDF",
                    data=archivo_pdf,
                    file_name=nombre_pdf,
                    mime="application/pdf"
                )

        if st.button(
            "📑 Exportar Orden Excel"
        ):

            nombre_excel = generar_excel_orden(
                orden,
                detalle_orden
            )

            with open(
                nombre_excel,
                "rb"
            ) as archivo_excel:

                st.download_button(
                    "📊 Descargar Excel",
                    data=archivo_excel,
                    file_name=nombre_excel,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                      
               
        
        st.subheader("👤 Datos del Cliente")

        st.write(
            f"**Nombre:** {orden['nombre']}"
        )

        st.write(
            f"**Teléfono:** {orden['telefono']}"
        )

        st.write(
            f"**Correo:** {orden['correo']}"
        )

        st.write(
            f"**Colegio:** {orden['colegio']}"
        )

        st.subheader("🧵 Datos de Producción")

        st.write(
            f"**Tipo de Logo:** {orden['tipo_logo']}"
        )

        st.write(
            f"**Cantidad Total:** {orden['cantidad_total']}"
        )

        st.write(
            f"**Fecha de Entrega:** {orden['fecha_entrega']}"
        )

        st.write(
            f"**Nombre Bordado:** {orden['nombre_bordado']}"
        )

        st.write(
            f"**Cantidad con Nombre:** {orden['cantidad_nombre']}"
        )

        st.divider()

        st.subheader("💰 Resumen Financiero")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Precio Bordado",
                f"${orden['precio_bordado']:.2f}"
            )

            st.metric(
                "Subtotal Bordado",
                f"${orden['subtotal_bordado']:.2f}"
            )

            st.metric(
                "Subtotal Nombres",
                f"${orden['subtotal_nombres']:.2f}"
            )

        with col2:

            st.metric(
                "Delivery",
                f"${orden['delivery_costo']:.2f}"
            )

            st.metric(
                "Abono",
                f"${orden['abono']:.2f}"
            )

            st.metric(
                "Saldo Pendiente",
                f"${orden['saldo_pendiente']:.2f}"
            )
            total_general = (
                orden["subtotal_bordado"]
                + orden["subtotal_nombres"]
                + orden["delivery_costo"]
            )

            st.metric(
                "Total General",
                f"${total_general:.2f}"
            )

        st.divider()

        st.subheader("👔 Desglose de Prendas")

        st.dataframe(
            detalle_orden,
            use_container_width=True
        )
 
if pagina == "Nueva Solicitud":

    st.subheader("Solicitud de Servicio de Bordado")

    st.header("Datos del Cliente")

    nombre = st.text_input("Nombre y Apellido *")

    telefono = st.text_input("Teléfono / WhatsApp *")

    correo = st.text_input("Correo Electrónico *")

    if telefono:
        if not re.match(r'^\d{10,}$', telefono):
           st.error("El teléfono debe tener solo números y mínimo 10 dígitos.")

    if correo:
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', correo):
            st.error("Correo electrónico inválido.")

    
    df_colegios = obtener_colegios()

    lista_colegios = (
        ["Seleccione un colegio..."]
        +
        df_colegios["nombre"]
        .dropna()
        .tolist()
    )   
    
    colegio = st.selectbox(
        "Colegio",
        lista_colegios
    )
    precio_bordado = obtener_precio_colegio(
        colegio
    )
    
    # if cantidad_total >= 6:

    #     precio_bordado = (
    #         precio_bordado - 0.50
    #     )

    #     st.success(
    #         "🎉 Promoción aplicada: -$0.50 por bordado por cantidad (6 o más prendas)"
    #     )    

    st.info(
        f"💰 Precio del bordado: ${precio_bordado:.2f}"
    )

    st.header("Especificaciones Generales")

    logo = st.radio(
        "Tipo de logo",
        [
            "Logo de diario",
            "Logo de deporte",
            "Logo de preescolar"
        ]
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
    st.info(
    f"📅 Fecha estimada de entrega: {fecha_entrega.strftime('%d/%m/%Y')}"
    )

    import pandas as pd

    st.header("Desglose de Prendas") 

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


    columnas = {
        "Tipo Prenda": st.column_config.SelectboxColumn(
            options=lista_tipos_prenda
        ),

        "Talla": st.column_config.SelectboxColumn(
            options=lista_tallas
        ),

        "Marca": st.column_config.SelectboxColumn(
            options=lista_marcas
        ),

        "Color": st.column_config.SelectboxColumn(
            options=lista_colores
        ),

        "Cantidad": st.column_config.NumberColumn(
            min_value=0,
            step=1
        )
    }

    df = st.data_editor(
        pd.DataFrame(
            columns=[
                "Tipo Prenda",
                "Talla",
                "Marca",
                "Color",
                "Cantidad"
            ]
        ),
        num_rows="dynamic",
        column_config=columnas,
        use_container_width=True
    )
    suma_prendas = 0


    if not df.empty:

        if "Cantidad" in df.columns:

            suma_prendas = df["Cantidad"].fillna(0).sum()

    cantidad_total = int(suma_prendas)
    

    if cantidad_total >= 6:

        precio_bordado = max(
            0,
            precio_bordado - 0.50
        )

        st.success(
            "🎉 Promoción aplicada: -$0.50 por bordado por cantidad (6 o más prendas)"
        )

    subtotal_bordado = (
        cantidad_total *
        precio_bordado
    )

    subtotal_bordado = (
        cantidad_total *
        precio_bordado
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total de Prendas",
            cantidad_total
        )

    with col2:

        st.metric(
            "Subtotal Bordado",
            f"${subtotal_bordado:.2f}"
        )

    cantidades_correctas = cantidad_total > 0


    nombre_bordado = ""

    cantidad_nombre = 0

    delivery = "No"

    zona_delivery = ""

    st.header("Bordado de Nombre")

    bordar_nombre = st.radio(
        "¿Desea bordar un nombre en sus prendas?",
        ["Sí", "No"]
    )

    nombre_bordado = ""
    cantidad_nombre = 0

    precio_nombre = obtener_parametro(
    "precio_nombre"
    )
    subtotal_nombres = 0
    cantidad_nombre = 0
    nombre_bordado = ""  

    if bordar_nombre == "Sí":

        nombre_bordado = st.text_area(
            "Indicar el nombre"
        )

        cantidad_nombre = st.number_input(
            "Cantidad de prendas con el nombre bordado",
            min_value=0,
            max_value=int(cantidad_total),
            step=1
        )

        subtotal_nombres = (
        cantidad_nombre *
        precio_nombre
        )

        st.info(
            f"💰 Precio por nombre: ${precio_nombre:.2f}"
            )

        st.metric(
            "Subtotal Bordado Nombre",
                f"${subtotal_nombres:.2f}"
                )

        if cantidad_nombre > cantidad_total:

            st.error(
                f"No puede bordar nombres en más de {cantidad_total} prendas."
            )

    
    st.header("Delivery")

    delivery = st.radio(
        "¿Desea servicio delivery?",
        [
            "Sí (con costo adicional)",
            "No"
        ]
    )

    zona_delivery = ""
    delivery_costo = 0

    if delivery == "Sí (con costo adicional)":

        df_zonas = obtener_zonas_delivery()

        lista_zonas = (
            ["Seleccione zona de delivery..."]
            +
            df_zonas["nombre"]
            .dropna()
            .tolist()
        )

        zona_delivery = st.selectbox(
            "Zona de entrega",
            lista_zonas
        )

        if zona_delivery != "Seleccione zona de delivery...":

            delivery_costo = obtener_costo_delivery(
                zona_delivery
            )

            st.info(
                f"🚚 Costo Delivery: ${delivery_costo:.2f}"
            )

        st.metric(
            "Subtotal Delivery",
            f"${delivery_costo:.2f}"
        )

    else:

        zona_delivery = ""
        delivery_costo = 0      

    st.header("Información de Pago")

    abono = 0.0
#  abono = st.number_input(
#       "Abono recibido ($)",
#       min_value=0.0,
#       value=0.0,
#       step=1.0
#   )

    saldo_pendiente = (
        subtotal_bordado +
        subtotal_nombres +
        delivery_costo -
        abono
    )

    st.metric(
        "Saldo Pendiente",
        f"${saldo_pendiente:.2f}"
    )
    if "solicitud_guardada" not in st.session_state:
        st.session_state["solicitud_guardada"] = False
    if st.button(
        "Guardar Solicitud",
        disabled=(
            not cantidades_correctas
            or st.session_state["solicitud_guardada"]
        )
    ):
        if colegio == "Seleccione un colegio...":

            st.error(
                "Debe seleccionar un colegio"
            )

            st.stop()
        if (
            delivery == "Sí (con costo adicional)"
            and
            zona_delivery == "Seleccione zona de delivery..."
        ):

            st.error(
                "Debe seleccionar una zona de delivery"
            )

            st.stop()

        status = "Recibido"        

        orden_id = guardar_orden(
            nombre,
            telefono,
            correo,
            colegio,
            cantidad_total,
            logo,
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

        for _, fila in df.iterrows():

            guardar_detalle(
                orden_id,
                fila["Tipo Prenda"],
                fila["Talla"],
                fila["Marca"],
                fila["Color"],
                int(fila["Cantidad"])
            )

        st.success("✅ Solicitud guardada correctamente")
        st.session_state["solicitud_guardada"] = True

    

