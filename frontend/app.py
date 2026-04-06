from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    categories = {
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

    fastapi_url = "http://127.0.0.1:8000/download-custom"
    return render_template("index.html", categories=categories, fastapi_url=fastapi_url)


if __name__ == "__main__":
    app.run(debug=True, port=5000)