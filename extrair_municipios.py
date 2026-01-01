from pathlib import Path
import geopandas as gpd

# DEFINIÇÃO DOS CAMINHOS DO PROJETO
# ROOT_DIR aponta para a pasta onde este script está localizado.
# Isso garante que o código funcione independentemente de onde ele for executado.
ROOT_DIR = Path(__file__).resolve().parent

# Pasta onde está o shapefile do IBGE
SHP_DIR = ROOT_DIR / "BR_Municipios_2024"

# Pasta de saída dos arquivos gerados
OUTPUT_DIR = ROOT_DIR / "Dados"

# Arquivo CSV final
OUTPUT_FILE = OUTPUT_DIR / "GeoMunicipios.csv"

# Cria a pasta de saída caso não exista
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# LOCALIZAÇÃO DO SHAPEFILE
# Procura automaticamente qualquer arquivo .shp dentro da pasta
shp_files = list(SHP_DIR.glob("*.shp"))
if not shp_files:
    raise FileNotFoundError("Nenhum arquivo .shp encontrado em /BR_Municipios_2024")

# Usa o primeiro shapefile encontrado
shp_path = shp_files[0]
print(f"Lendo shapefile: {shp_path.name}")

# LEITURA DO SHAPEFILE
# O GeoDataFrame conterá geometrias do tipo Polygon / MultiPolygon
gdf = gpd.read_file(shp_path)

# DEFINIÇÃO DO CRS (SISTEMA DE REFERÊNCIA ESPACIAL)
# Caso o shapefile não possua CRS definido, assumimos o padrão geográfico do IBGE (SIRGAS 2000)
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4674)

# REPROJEÇÃO PARA CÁLCULO CORRETO DO CENTRÓIDE
# NÃO se deve calcular centróide em coordenadas geográficas (graus).
# Por isso, reprojetamos para um CRS projetado em metros
# (EPSG:5880 - projeção adequada para o território brasileiro)
gdf_proj = gdf.to_crs(epsg=5880)

# CÁLCULO DO CENTRÓIDE
# Aqui cada município (polígono) é transformado em um ponto representativo de sua geometria
gdf_proj["geometry"] = gdf_proj.geometry.centroid

# RETORNO PARA COORDENADAS GEOGRÁFICAS (WGS84)
# Após o cálculo do centróide, voltamos para latitude/longitude no padrão mais usado por ferramentas de BI
gdf_points = gdf_proj.to_crs(epsg=4326)

# EXTRAÇÃO DE LATITUDE E LONGITUDE
# A partir da geometria do tipo Point
gdf_points["latitude"] = gdf_points.geometry.y
gdf_points["longitude"] = gdf_points.geometry.x

# SELEÇÃO E RENOMEAÇÃO DE COLUNAS
# Mantemos apenas as colunas relevantes para análises e BI
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

# Mapeamento de nomes técnicos do IBGE para nomes amigáveis
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

# Aplica seleção, renomeação e remove a geometria
df_final = (
    gdf_points[colunas_origem]
    .rename(columns=rename_map)
    .drop(columns=["geometry"], errors="ignore")
)

# EXPORTAÇÃO FINAL
# - Separador de colunas: ;
# - Separador decimal: ,
# - Encoding UTF-8 para compatibilidade ampla
df_final.to_csv(
    OUTPUT_FILE,
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8"
)

#feedback básico para o usuário
print(f"Arquivo gerado com sucesso em: {OUTPUT_FILE}")
