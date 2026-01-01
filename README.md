# Centroides Geográficos dos Municípios Brasileiros (IBGE)

Este projeto tem como objetivo **gerar um dataset geográfico limpo, padronizado e pronto para BI**, contendo **um par de coordenadas (latitude e longitude) para o centro de cada município brasileiro**, a partir dos dados oficiais do IBGE.

O resultado final é um **CSV leve e interoperável**, ideal para uso em ferramentas de dados.


## Objetivo do Projeto

Transformar dados geoespaciais oficiais (Shapefile) em um **arquivo tabular simples**, contendo:

- Identificação dos Municípios Estados e Regiões  
- Área territorial  
- **Latitude e longitude representativas (centróide)**  

Tudo isso respeitando **boas práticas cartográficas**, evitando distorções comuns em dados geográficos.


## Fonte dos Dados

- **Instituição:** Instituto Brasileiro de Geografia e Estatística - IBGE 
- **Dataset:** Malhas territoriais dos municípios brasileiros  
- **Ano:** 2024  
- **Formato original:** Shapefile (`.shp`, `.dbf`, `.shx`, `.cpg`, `.prj`)
- **Disponível em:** https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html 


## Abordagem Técnica

Os municípios no dataset do IBGE são representados por **polígonos e multipolígonos**.  
Para gerar um único ponto por município, o script executa os seguintes passos:

1. Reprojeta os dados para um **CRS projetado (EPSG:5880)**;
2. Calcula o **centróide geométrico corretamente**;
3. Reprojeta o resultado para **WGS84 (EPSG:4326)**;
4. Extrai **latitude e longitude**; 
5. Padroniza nomes de colunas;
6. Exporta um CSV pronto.

Essa abordagem evita erros comuns como:
- Cálculo de centróide em coordenadas geográficas;
- Pontos deslocados em municípios extensos;
- Problemas de reconhecimento automático de tipos de dados;


## Estrutura do Projeto

O projeto tem uma extrutura bem simples e didática.

```yaml
CentroidesGeo/
│
├── BR_Municipios_2024/
│ ├── BR_Municipios_2024.shp
│ ├── BR_Municipios_2024.dbf
│ ├── BR_Municipios_2024.shx
│ ├── BR_Municipios_2024.prj
│ └── BR_Municipios_2024.cpg
│
├── Dados/
│ └── GeoMunicipios.csv
│
├── extrair_municipios.py
└── README.md
```

## Estrutura do Dataset Final (`GeoMunicipios.csv`)

- **Separador de colunas:** `;`  
- **Separador decimal:** `,`  

| Coluna | Descrição |
|------|----------|
| `codigo_municipio` | Código IBGE do município |
| `municipio` | Nome do município |
| `codigo_uf` | Código IBGE do estado |
| `estado` | Nome do estado |
| `sigla_uf` | Sigla da UF |
| `codigo_regiao` | Código da grande região |
| `regiao` | Nome da região |
| `sigla_regiao` | Sigla da região |
| `area_km2` | Área territorial do município |
| `latitude` | Latitude do centróide |
| `longitude` | Longitude do centróide |


## Requisitos e Versões das Principais Bibliotecas

- Python 3.13.5 (ou compatível)
- Pandas 2.3.3 (ou compatível)
- Geopandas 1.1.2 (ou compatível)
- Ambiente virtual (recomendado)


## Como Utilizar

`OBS:` Instruções de utilização baseadas em sistemas Linux baseados em Debian (Ubuntu, Linux Mint, Elementary OS, Pop!_OS, etc).

### 1 - Criar ambiente virtual

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```
### 2 - Instalar dependências e bibliotecas auxiliáres
```bash
$ python3 -m pip install --upgrade pip
$ pip install pandas geopandas black
```
> [!NOTE]
> Em sistemas Linux, pode ser necessário instalar dependências do GDAL via gerenciador de pacotes.

```bash
$ sudo apt install gdal-bin python3-gdal -y
```
### 3 - Crie o script `extrair_municipios.py` na raiz do projeto e execute-o.
```bash
$ python3 extrair_municipios.py
```
### Resultado

O arquivo será gerado em: `/Dados/GeoMunicipios.csv`

## Casos de Uso

- Mapas de pontos por município;
- Clusters geográficos;
- Heatmaps;
- Análises regionais;
- Join com bases transacionais usando código IBGE;
- Dashboards que precisam de coordenadas precisas para gerar mapas como o Looker Studio;
- Projetos que precisem comprovar a procedencia dos dados a partir de órgãos oficiais.

## Observações Importantes

- O CSV gerado utiliza formatação PT-BR (; e ,) para melhor compatibilidade com representações visuais na lingua portuguesa;
- Para ingestão em bancos analíticos (BigQuery, DuckDB, PostgreSQL), pode ser recomendada uma versão técnica ("." como separador decimal);
- O centróide representa o centro geográfico do território municipal e pode não coincidir exatamente com o centro urbano do município.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/thaleswillreis/CentroidesGeoIBGE/blob/main/LICEN%C3%87A_PT-BR.md) para mais detalhes.