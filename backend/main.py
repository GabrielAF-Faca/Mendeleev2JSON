from fastapi import FastAPI, Query
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from mendeleev import element
import json
import pickle

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

    print(properties)

    for el in elements:
        element_data = {}

        for prop in properties:
            try:
                # Recupera o atributo da biblioteca
                attr = getattr(el, prop)
                
                # Verifica se o atributo é um método executável
                if callable(attr):
                    # Se for um método (ex: nvalence), executa e salva o retorno
                    element_data[prop] = attr()
                else:
                    # Se for uma propriedade normal, salva diretamente
                    element_data[prop] = attr
                    
            except AttributeError:
                element_data[prop] = None
            except Exception as e:
                # Tratamento extra caso algum método da biblioteca falhe ou exija argumentos que não passamos
                print(f"Erro ao processar a propriedade '{prop}' no elemento {el.symbol}: {e}")
                element_data[prop] = None

        # --- DICA DE SEGURANÇA ---
        # Garantimos que 'symbol' seja usado como chave apenas se estiver no dicionário.
        # Caso o front-end não envie 'symbol' na requisição, usamos o ID ou outro identificador para evitar KeyError.
        key = element_data.get("symbol", el.symbol) 
        filtered_data[key] = element_data

    headers = {"Content-Disposition": "attachment; filename=custom_table.json"}

    # Opcional: Adicionar default=str no json.dumps se a biblioteca retornar objetos complexos (ex: datas)
    json_formatted = json.dumps(filtered_data, indent=4, default=str)

    return Response(content=json_formatted, media_type="application/json", headers=headers)

@app.get("/available-properties")
def list_properties():
    return {
    "General": [
            "atomic_number", "symbol", "name", "name_origin", "description", 
            "cas", "inchi", "group_id", "period", "block", "series", 
            "is_radioactive", "is_monoisotopic", "nist_webbook_url"
        ],
        "Mass & Particles": [
            "atomic_weight", "atomic_weight_uncertainty", "mass", "mass_str", 
            "mass_number", "electrons", "protons", "neutrons", "isotopes"
        ],
        "Physical": [
            "density", "atomic_volume", "melting_point", "boiling_point", 
            "evaporation_heat", "fusion_heat", "heat_of_formation", 
            "specific_heat_capacity", "specific_heat", "molar_heat_capacity", 
            "thermal_conductivity", "lattice_constant", "lattice_structure", 
            "gas_basicity", "phase_transitions"
        ],
        "Atomic Radii": [
            "atomic_radius", "atomic_radius_rahm"
        ],
        "Covalent Radii": [
            "covalent_radius", "covalent_radius_bragg", "covalent_radius_cordero", 
            "covalent_radius_pyykko", "covalent_radius_pyykko_double", 
            "covalent_radius_pyykko_triple"
        ],
        "Van der Waals Radii": [
            "vdw_radius", "vdw_radius_alvarez", "vdw_radius_bondi", 
            "vdw_radius_truhlar", "vdw_radius_rt", "vdw_radius_batsanov", 
            "vdw_radius_dreiding", "vdw_radius_uff", "vdw_radius_mm3"
        ],
        "Metallic & Ionic Radii": [
            "metallic_radius", "metallic_radius_c12", "ionic_radii"
        ],
        "Electronic & Chemistry": [
            "econf", "nvalence", "electron_affinity", "proton_affinity", 
            "dipole_polarizability", "dipole_polarizability_unc", "c6", "c6_gb", 
            "miedema_molar_volume", "miedema_electron_density", "zeff", 
            "sconst", "screening_constants", "ionenergies", "oxistates", 
            "oxidation_states", "oxides"
        ],
        "Electronegativity": [
            "en_allen", "en_ghosh", "en_miedema", "en_mullay", "en_pauling", 
            "en_gunnarsson_lundqvist", "en_robles_bartolotti", "electronegativity", 
            "electronegativity_allen", "electronegativity_allred_rochow", 
            "electronegativity_cottrell_sutton", "electronegativity_ghosh", 
            "electronegativity_gordy", "electronegativity_li_xue", 
            "electronegativity_martynov_batsanov", "electronegativity_mullay", 
            "electronegativity_mulliken", "electronegativity_nagle", 
            "electronegativity_pauling", "electronegativity_sanderson"
        ],
        "Hardness & Electrophilicity": [
            "hardness", "softness", "electrophilicity"
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
