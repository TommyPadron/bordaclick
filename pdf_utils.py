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