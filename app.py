from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

def crear_app():
    app = Flask(__name__)
    CORS(app, origins=['*'])

    @app.route("/api/noticias-actualidad")
    def getNoticias():
        url = "https://ultimasnoticias.com.ve/"
        response = requests.get(url, verify=True)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_titulo = soup.find('div', class_='tdi_194').find('h3').text.strip()
            div_noticias = soup.find('div', id='tdi_195').findAll('div', class_='td-cpt-post')

            lista_noticias = []
            for noticia in div_noticias:
                #image_container
                image_container = noticia.find('div', class_='td-image-container')
                href_noticia = image_container.find('a').get('href')
                thum_noticia = image_container.find('span').get('data-img-url')

                #meta_info
                meta_info = noticia.find('div', class_='td-module-meta-info')
                href_categoria = meta_info.find('a').get('href')
                name_href_categoria = meta_info.find('a').text.strip()

                meta_detalle_noticia = meta_info.find('h3')
                href_detalle_noticia = meta_detalle_noticia.find('a').get('href')
                texto_detalle_noticia = meta_detalle_noticia.find('a').text.strip()

                meta_fecha_noticia = meta_info.find('div', class_='td-editor-date')
                fecha_detalle_noticia = meta_fecha_noticia.find('time', class_='td-module-date').text.strip()

                lista_noticias.append(
                    {
                        'thumb_image': thum_noticia,
                        'name_category': name_href_categoria,
                        'href_category': href_categoria,
                        'href_detail_news': href_detalle_noticia,
                        'text_detail_news': texto_detalle_noticia,
                        'date_news': fecha_detalle_noticia
                    }
                )

            return jsonify({'title': div_titulo, 'data': lista_noticias})
        else:
            error = {'error': 'Ocurrio un error interno'}
            return jsonify(error)


    @app.route("/api/obtener-detalle-noticia")
    def getDetalleNoticias():
        urlDetalleNoticia = request.args.get('url')
        headers={'User-Agent':'mozilla/5.0'}
        response = requests.get(urlDetalleNoticia, headers=headers, verify=True)
        print("response", response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            imagen_noticia = soup.find('div', class_='tdb_single_featured_image').find('figure').find('img').get('src')
            titulo_noticia = soup.find('h1', class_='tdb-title-text').text.strip()
            sub_titulo_noticia = soup.find('div', class_='tdb_single_subtitle').find('h2').text.strip()
            textos_noticia = soup.find('div', class_='tdb_single_content').find('div', class_='tdb-block-inner').findAll('p')
            fecha_noticia = soup.find('time', class_='entry-date').text.strip()
            categoria_noticia = soup.find('div', class_='tdb-category').find('a').text.strip()
            link_categoria_noticia = soup.find('div', class_='tdb-category').find('a').get('href')

            texto_noticia = ""
            for texto in textos_noticia:
                texto_noticia += " "+ texto.get_text().strip()

            return jsonify(
                {
                    'image': imagen_noticia,
                    'title': titulo_noticia,
                    'subtitle': sub_titulo_noticia,
                    'content': texto_noticia,
                    'date': fecha_noticia,
                    'name_category': categoria_noticia,
                    'url_category': link_categoria_noticia
                }
            )
        else:
            error = {'error': 'Ocurrio un error interno'}
            return jsonify(error)


    @app.route("/api/obtener-categorias-noticias")
    def getCategoriaNoticias():
        urlCategoriaNoticia = request.args.get('url-categoria')
        headers={'User-Agent':'mozilla/5.0'}
        response = requests.get(urlCategoriaNoticia, headers=headers, verify=True)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_titulo = soup.find('h1', class_='tdb-title-text').text.strip()
            div_noticias = soup.find('div', id='tdi_90').findAll('div', class_='td-cpt-post')
            print("div_noticias", div_noticias)

            lista_noticias = []
            for noticia in div_noticias:
                #image_container
                image_container = noticia.find('div', class_='td-image-container')
                href_noticia = image_container.find('a').get('href')
                thum_noticia = image_container.find('span').get('data-img-url')

                #meta_info
                meta_info = noticia.find('div', class_='td-module-meta-info')
                href_categoria = meta_info.find('a').get('href')
                name_href_categoria = meta_info.find('a').text.strip()

                meta_detalle_noticia = meta_info.find('h3')
                href_detalle_noticia = meta_detalle_noticia.find('a').get('href')
                texto_detalle_noticia = meta_detalle_noticia.find('a').text.strip()

                meta_fecha_noticia = meta_info.find('div', class_='td-editor-date')
                fecha_detalle_noticia = meta_fecha_noticia.find('time', class_='td-module-date').text.strip()

                lista_noticias.append(
                    {
                        'thumb_image': thum_noticia,
                        'name_category': name_href_categoria,
                        'href_category': href_categoria,
                        'href_detail_news': href_detalle_noticia,
                        'text_detail_news': texto_detalle_noticia,
                        'date_news': fecha_detalle_noticia
                    }
                )

            return jsonify({'title': div_titulo, 'data': lista_noticias})
        else:
            error = {'error': 'Ocurrio un error interno'}
            return jsonify(error)
        
    return app

if __name__ == "__main__":
    app = crear_app()
    app.run()