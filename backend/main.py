from fastapi import FastAPI, Query
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from mendeleev import element
import json

app = FastAPI(title="Dynamic Periodic Table API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

elements_cache = []

def load_elements():
    """
    Loads the Mendeleev library objects into the cache only once.
    """
    global elements_cache
    if not elements_cache:
        elements_cache = [element(i) for i in range(1, 119)]
    return elements_cache


@app.get("/download-custom")
def download_custom_table(
        properties: List[str] = Query(["atomic_number", "name", "symbol"])
):
    """
    Generates a JSON with only the properties chosen by the front-end.
    """
    elements = load_elements()
    filtered_data = {}

    for el in elements:
        element_data = {}

        for prop in properties:
            try:
                element_data[prop] = getattr(el, prop)
            except AttributeError:
                element_data[prop] = None

        filtered_data[element_data["symbol"]] = element_data

    headers = {"Content-Disposition": "attachment; filename=custom_table.json"}

    json_formatted = json.dumps(filtered_data, indent=4)

    return Response(content=json_formatted, media_type="application/json", headers=headers)


@app.get("/available-properties")
def list_properties():
    return {
    "General": [
        "atomic_number", "name", "symbol", "atomic_weight",
        "atomic_weight_uncertainty", "cas", "group_id", "period",
        "block", "is_radioactive", "is_monoisotopic",
        "description", "name_origin"
    ],
    "Physical": [
        "density", "lattice_constant", "lattice_structure",
        "specific_heat_capacity", "molar_heat_capacity",
        "thermal_conductivity", "evaporation_heat",
        "fusion_heat", "heat_of_formation", "gas_basicity"
    ],
    "Atomic Radii": [
        "atomic_radius", "atomic_radius_rahm"
    ],
    "Van der Waals Radii": [
        "vdw_radius", "vdw_radius_alvarez", "vdw_radius_bondi",
        "vdw_radius_truhlar", "vdw_radius_rt", "vdw_radius_batsanov",
        "vdw_radius_dreiding", "vdw_radius_uff", "vdw_radius_mm3"
    ],
    "Covalent Radii": [
        "covalent_radius_bragg", "covalent_radius_cordero",
        "covalent_radius_pyykko", "covalent_radius_pyykko_double",
        "covalent_radius_pyykko_triple"
    ],
    "Metallic Radii": [
        "metallic_radius", "metallic_radius_c12"
    ],
    "Electronegativity": [
        "en_pauling", "en_miedema", "en_mullay", "en_gunnarsson_lundqvist",
        "en_robles_bartolotti", "en_allen", "en_ghosh"
    ],
    "Electronic": [
        "econf", "ec", "electron_affinity", "proton_affinity",
        "dipole_polarizability", "dipole_polarizability_unc",
        "c6", "c6_gb", "miedema_molar_volume", "miedema_electron_density"
    ],
    "History": [
        "discoverers", "discovery_location", "discovery_year"
    ],
    "Abundance & Geology": [
        "abundance_crust", "abundance_sea", "geochemical_class",
        "goldschmidt_class", "glawe_number", "mendeleev_number",
        "pettifor_number"
    ],
    "Economics & Applications": [
        "uses", "sources", "price_per_kg", "recycling_rate",
        "substitutability", "relative_supply_risk",
        "political_stability_of_top_producer",
        "political_stability_of_top_reserve_holder",
        "production_concentration", "reserve_distribution",
        "top_3_producers", "top_3_reserve_holders"
    ],
    "Colors (Visuals)": [
        "jmol_color", "cpk_color", "molcas_gv_color"
    ]
}