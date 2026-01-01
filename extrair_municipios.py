from pathlib import Path
import geopandas as gpd

# -----------------------------
# Caminhos do projeto
# -----------------------------
ROOT_DIR = Path(__file__).resolve().parent
SHP_DIR = ROOT_DIR / "BR_Municipios_2024"
OUTPUT_DIR = ROOT_DIR / "Dados"
OUTPUT_FILE = OUTPUT_DIR / "GeoMunicipios.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Localiza o SHP
# -----------------------------
shp_files = list(SHP_DIR.glob("*.shp"))
if not shp_files:
    raise FileNotFoundError("Nenhum arquivo .shp encontrado em /BR_Municipios_2024")

shp_path = shp_files[0]
print(f"Lendo shapefile: {shp_path.name}")

# -----------------------------
# Leitura
# -----------------------------
gdf = gpd.read_file(shp_path)

# -----------------------------
# CRS
# -----------------------------
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4674)

# Reprojeta para CRS projetado (cálculo correto de centróide)
gdf_proj = gdf.to_crs(epsg=5880)

# -----------------------------
# Calcula centróides
# -----------------------------
gdf_proj["geometry"] = gdf_proj.geometry.centroid

# Volta para WGS84
gdf_points = gdf_proj.to_crs(epsg=4326)

# -----------------------------
# Extrai latitude / longitude
# -----------------------------
gdf_points["latitude"] = gdf_points.geometry.y
gdf_points["longitude"] = gdf_points.geometry.x

# -----------------------------
# Seleção e renomeação de colunas
# -----------------------------
colunas_origem = [
    "CD_MUN",
    "NM_MUN",
    "CD_UF",
    "NM_UF",
    "SIGLA_UF",
    "CD_REGIA",
    "NM_REGIA",
    "SIGLA_RG",
    "AREA_KM2",
    "latitude",
    "longitude",
]

rename_map = {
    "CD_MUN": "codigo_municipio",
    "NM_MUN": "municipio",
    "CD_UF": "codigo_uf",
    "NM_UF": "estado",
    "SIGLA_UF": "sigla_uf",
    "CD_REGIA": "codigo_regiao",
    "NM_REGIA": "regiao",
    "SIGLA_RG": "sigla_regiao",
    "AREA_KM2": "area_km2",
    "latitude": "latitude",
    "longitude": "longitude",
}

df_final = (
    gdf_points[colunas_origem]
    .rename(columns=rename_map)
    .drop(columns=["geometry"], errors="ignore")
)

# -----------------------------
# Exportação final
# -----------------------------
df_final.to_csv(
    OUTPUT_FILE,
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8"
)

print(f"Arquivo gerado com sucesso em: {OUTPUT_FILE}")
