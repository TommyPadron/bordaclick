import pandas as pd
from pdf_utils import generar_pdf_orden, generar_excel_orden

orden_prueba = {
    "id": 1,
    "status": "Pendiente",
    "fecha_entrega": "2026-08-25",
    "nombre": "Cliente Prueba",
    "telefono": "+584120000000",
    "correo": "cliente@prueba.com",
    "colegio": "Colegio San Ignacio",
    "tipo_logo": "Bordado Directo",
    "cantidad_total": 5,
    "nombre_bordado": "Carlos",
    "cantidad_nombre": 5,
    "subtotal_bordado": 25.0,
    "subtotal_nombres": 10.0,
    "delivery_costo": 5.0,
    "precio_bordado": 5.0,
    "abono": 20.0,
    "saldo_pendiente": 20.0
}

detalle_prueba = pd.DataFrame([{
    "Colegio": "Colegio San Ignacio",
    "Tipo Prenda": "Camisa",
    "Talla": "M",
    "Marca": "Guillermo",
    "Color": "Azul",
    "Cantidad": 5
}])

print("Generando PDF...")
pdf_resultado = generar_pdf_orden(orden_prueba, detalle_prueba)

print("Generando Excel...")
excel_resultado = generar_excel_orden(orden_prueba, detalle_prueba)

print(f"\n¡Éxito! Archivos creados correctamente:\n - {pdf_resultado}\n - {excel_resultado}")