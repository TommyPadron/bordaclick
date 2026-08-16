import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)
from openpyxl import Workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Border,
    Side
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

    for colegio in detalle_orden["Colegio"].unique():

        elementos.append(
            Paragraph(
                f"🏫 {colegio}",
                estilos["Heading4"]
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

        df_colegio = detalle_orden[
            detalle_orden["Colegio"] == colegio
        ]

        for _, fila in df_colegio.iterrows():

            datos_tabla.append(
                [
                    str(fila["Tipo Prenda"]),
                    str(fila["Talla"]),
                    str(fila["Marca"]),
                    str(fila["Color"]),
                    str(fila["Cantidad"])
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
            Spacer(1, 10)
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
    
    encabezado_tabla = Font(
        bold=True
    )
    fila_excel = 28

    for colegio in detalle_orden["Colegio"].unique():

        ws[f"A{fila_excel}"] = f"🏫 {colegio}"
        ws[f"A{fila_excel}"].font = titulo

        fila_excel += 1

        ws[f"A{fila_excel}"] = "Tipo Prenda"
        ws[f"B{fila_excel}"] = "Talla"
        ws[f"C{fila_excel}"] = "Marca"
        ws[f"D{fila_excel}"] = "Color"
        ws[f"E{fila_excel}"] = "Cantidad"

        ws[f"A{fila_excel}"].font = encabezado_tabla
        ws[f"B{fila_excel}"].font = encabezado_tabla
        ws[f"C{fila_excel}"].font = encabezado_tabla
        ws[f"D{fila_excel}"].font = encabezado_tabla
        ws[f"E{fila_excel}"].font = encabezado_tabla

        ws[f"A{fila_excel}"].fill = fondo_gris
        ws[f"B{fila_excel}"].fill = fondo_gris
        ws[f"C{fila_excel}"].fill = fondo_gris
        ws[f"D{fila_excel}"].fill = fondo_gris
        ws[f"E{fila_excel}"].fill = fondo_gris

        fila_excel += 1

        df_colegio = detalle_orden[
            detalle_orden["Colegio"] == colegio
        ]

        for _, fila in df_colegio.iterrows():

            ws[f"A{fila_excel}"] = fila["Tipo Prenda"]
            ws[f"B{fila_excel}"] = fila["Talla"]
            ws[f"C{fila_excel}"] = fila["Marca"]
            ws[f"D{fila_excel}"] = fila["Color"]
            ws[f"E{fila_excel}"] = fila["Cantidad"]

            fila_excel += 1

        fila_excel += 1

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
