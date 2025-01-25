# Docking Molecular Web App

Esta aplicación permite realizar docking molecular entre un ligando y una proteína usando AutoDock Vina.

## Características
- Subir moléculas en formato SMILES para el ligando.
- Subir proteínas en formato PDB.
- Ejecutar docking molecular y obtener:
  - La mejor pose del complejo.
  - El score de la mejor interacción.

## Requisitos
- Python 3.8+
- AutoDock Vina
- Librerías adicionales (ver `requirements.txt`).

## Cómo usar
1. Suba un archivo SMILES para el ligando.
2. Suba un archivo PDB para la proteína.
3. Ejecute el docking y descargue los resultados.
