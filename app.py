import os
import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from Bio.PDB import PDBParser, PDBIO
from vina import Vina
import tempfile

# Título de la aplicación
st.title("Docking Molecular Web App")
st.markdown(
    """
    Suba un archivo SMILES para el ligando y un archivo PDB para la proteína.
    La aplicación ejecutará un docking molecular usando **AutoDock Vina** y mostrará la mejor pose.
    """
)

# Cargar el archivo SMILES
smiles = st.text_input("Ingrese el SMILES del ligando")
if smiles:
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            st.success("El SMILES ingresado es válido.")
            mol_file = tempfile.NamedTemporaryFile(suffix=".pdb", delete=False)
            AllChem.EmbedMolecule(mol)
            AllChem.MolToPDBFile(mol, mol_file.name)
        else:
            st.error("El SMILES ingresado no es válido.")
    except Exception as e:
        st.error(f"Error procesando el SMILES: {e}")

# Cargar el archivo PDB para la proteína
pdb_file = st.file_uploader("Suba el archivo PDB de la proteína", type=["pdb"])
if pdb_file:
    protein_pdb_path = tempfile.NamedTemporaryFile(suffix=".pdb", delete=False)
    with open(protein_pdb_path.name, "wb") as f:
        f.write(pdb_file.getbuffer())
    st.success("Archivo PDB cargado exitosamente.")

# Docking
if st.button("Ejecutar Docking") and smiles and pdb_file:
    try:
        # Configurar AutoDock Vina
        vina = Vina(sf_name='vina')

        # Configurar proteína (receptor)
        vina.set_receptor(protein_pdb_path.name)

        # Configurar ligando
        vina.set_ligand_from_file(mol_file.name)

        # Definir la caja de docking (ajustar manualmente si es necesario)
        vina.compute_vina_maps(center=[0, 0, 0], box_size=[20, 20, 20])

        # Ejecutar docking
        st.info("Ejecutando docking, esto puede tomar unos minutos...")
        results = vina.dock(exhaustiveness=8, n_poses=1)

        # Obtener la mejor pose
        vina.write_poses("docked_ligand.pdbqt", n_poses=1)
        st.success("Docking completado!")

        # Mostrar el resultado
        with open("docked_ligand.pdbqt", "r") as f:
            docked_pose = f.read()
        st.download_button("Descargar pose acoplada (PDBQT)", data=docked_pose, file_name="docked_ligand.pdbqt")

        # Score
        score = results[0]["score"]
        st.write(f"**Score (kcal/mol):** {score}")

    except Exception as e:
        st.error(f"Error durante el docking: {e}")
