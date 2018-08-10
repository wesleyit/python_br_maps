'''
# BR_MAPS - Gráficos de Mapas do Brasil

Este módulo auxiliar serve para facilitar o processo de criação
de mapas geográficos com estados do Brasil. Ele foi construído
porque até o momento, poucas bibliotecas oferecem suporte
adequado para os mapas locais de forma fácil de usar.

Os mapas utilizam a biblioteca **cartopy** e são baixados
em formato `.shape` do site https://biogeo.ucdavis.edu.
'''


import cartopy.io.shapereader as shp
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import unicodedata as ud
import os


# Definição de arquivos e diretórios
base_dir = os.path.dirname(__file__)
maps_dir = base_dir + '/maps/'
shape_cowntry = maps_dir + 'gadm36_BRA_0.shp' 
shape_states = maps_dir + 'gadm36_BRA_1.shp'
shape_cities = maps_dir + 'gadm36_BRA_2.shp'
shape_districts = maps_dir + 'gadm36_BRA_3.shp'
facecolor = '#333333'
edgecolor = '#CCCCCC'
crs = ccrs.PlateCarree()


# Lista auxiliar com estados e siglas:
states_codes = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MG': 'Minas Gerais',
    'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'SE': 'Sergipe',
    'SP': 'São Paulo',
    'TO': 'Tocantins',
}


def pstr(data):
    '''
    pstr('String to be prepared')
    Prepara uma string para ser comparada com outra,
    tornando-a minúscula e removendo caracteres especiais.
    '''
    normal = ud.normalize('NFKD', data).encode('ASCII', 'ignore')
    return str.lower(str(normal))


def __zoom__(ax, geo):
    X, Y = [], []
    for multipolygon in geo:
        for polygon in multipolygon:
            x, y = polygon.exterior.coords.xy
            X.extend(x)
            Y.extend(y)
    ax.set_extent([max(X), min(X), max(Y), min(Y)], crs=crs)


def search_state(state, plot=False):
    '''
    search_state(state, plot=False)
    Busca por um estado a partir de seu nome.
    Se encontrado, retorna um objeto que pode ser plotado.
    Se plot=True, retorna as coordenadas, que no Jupyter já
    geram um gráfico com o mapa.
    '''
    states = list(shp.Reader(shape_states).records())
    for record in states:
        state_name = record.attributes['NAME_1']
        if pstr(state_name) == pstr(state):
            if plot is False:
                return record
            else:
                return record.geometry


def search_city(city, state, plot=False):
    '''
    search_city(city, state, plot=False)
    Busca por uma cidade a partir de seu nome e do nome
    do estado onde ela está localizada.
    Se encontrada, retorna um objeto que pode ser plotado.
    Se plot=True, retorna as coordenadas, que no Jupyter já
    geram um gráfico com o mapa.
    '''
    cities = list(shp.Reader(shape_cities).records())
    for record in cities:
        state_name = record.attributes['NAME_1']
        city_name = record.attributes['NAME_2']
        if pstr(state_name) == pstr(state) and pstr(city_name) == pstr(city):
            if plot is False:
                return record
            else:
                return record.geometry


def search_district(district, city, state, plot=False):
    '''
    search_district(district, city, state, plot=False):
    Busca por um distrito a partir de seu nome e do nome
    da cidade e do estado onde ele está localizado.
    Se encontrada, retorna um objeto que pode ser plotado.
    Se plot=True, retorna as coordenadas, que no Jupyter já
    geram um gráfico com o mapa.
    '''
    districts = list(shp.Reader(shape_districts).records())
    for record in districts:
        state_name = record.attributes['NAME_1']
        city_name = record.attributes['NAME_2']
        district_name = record.attributes['NAME_3']
        if pstr(state_name) == pstr(state) and \
           pstr(city_name) == pstr(city) and \
           pstr(district_name) == pstr(district):
            if plot is False:
                return record
            else:
                return record.geometry


def plot_brazil(facecolor=facecolor, edgecolor=edgecolor):
    '''
    plot_brazil(facecolor='#333333', edgecolor='#FFFFFF'):
    Plota um mapa do Brasil. Aceita como parâmetros a cor
    do mapa e a cor da borda.
    '''
    states_geo = shp.Reader(shape_states).geometries()
    ax = plt.axes(projection=crs)
    ax.set_extent([-74.5, -34.5, -40, 10], crs=ccrs.PlateCarree())
    ax.add_geometries(states_geo,
                      crs,
                      facecolor=facecolor,
                      edgecolor=edgecolor)
    plt.gca().outline_patch.set_visible(False)
    return ax


def plot_states(s='Distrito Federal',
                zoom=True,
                ax=None,
                facecolor=facecolor,
                edgecolor=edgecolor):
    '''
    plot_states(s='Distrito Federal'):
    plot_states(s='Distrito Federal',
                facecolor='#000000', 
                edgecolor='#DFDFDF'):
    plot_states(s=['Distrito Federal', 'Goiás', 'Tocantins']):
    Plota um estado ou uma lista de estados.
    Permite a especificação das cores do estado e da borda.
    Caso um único estado seja fornecido, ele é plotado
    com zoom. Se mais de um estado for fornecido, o nível
    de zoom é o mesmo equivalente ao mapa completo do Brasil.
    '''
    if type(s) is not list:
        s = [s]
    states = shp.Reader(shape_states).records()
    states_geo = [x.geometry for x in states if pstr(x.attributes['NAME_1'])
                  in list(map(pstr, s))]
    if not ax:
        ax = plt.axes(projection=crs)
    if zoom: __zoom__(ax, states_geo)
    ax.add_geometries(states_geo,
                      crs,
                      facecolor=facecolor,
                      edgecolor=edgecolor)
    plt.gca().outline_patch.set_visible(False)
    ax.set_label(str(s))
    return ax
