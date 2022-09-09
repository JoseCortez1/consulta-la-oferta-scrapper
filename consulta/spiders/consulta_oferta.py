import scrapy # Import the scrapy library
import os
import lxml.html as html
''' 
{
	"ciclop": "202220",
	"cup": "D",
	"majrp": "INCO",
	"crsep": "",
	"materiap": "",
	"horaip": "",
	"horafp": "",
	"edifp": "",
	"aulap": "",
	"dispp": "D",
	"ordenp": "0",
	"mostrarp": "100"
}
'''
class ConsultaSpider(scrapy.Spider):
   
    if(os.path.exists('datos_oferta.json')):
        os.remove('datos_oferta.json')
        
    name = 'oferta'
    materia = '&crsep=I5884'
    url_consulta_oferta_con_0_cupos = 'http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202220&cup=D&majrp=INCO&mostrarp=1000'
    url_consulta_oferta = 'http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202220&cup=D&majrp=INCO&dispp=D&mostrarp=1000'
    ''' not_quotas = getattr('quotas', 'True')
    if(not_quotas):
        if(not_quotas == 'False'):
            not_quotas = False
        else:
            not_quotas = True
        
    
    url = (url_consulta_oferta, url_consulta_oferta_con_0_cupos)[not_quotas] '''
    start_urls = [
        url_consulta_oferta
    ]
    custom_settings = {
        'FEED_URI': 'datos_oferta.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': [''],
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'servicioBot',
        'FEED_EXPORT_ENCODING': 'utf-8',
        
    }
    def parse(self, response):
        
        rows = response.xpath('//table//tr[contains(@style, "background-color")]').getall()
        if rows:
            for row in rows:
                row = html.fromstring(row)
                try:
                    yield {
                        
                        'nrc': row.xpath('//td[1]/text()')[0],
                        'clave': row.xpath('//td/a/text()')[0],
                        'materia': row.xpath('//td[3]/a/text()')[0],
                        'seccion': row.xpath('//td[4]/text()')[0],
                        'horario': row.xpath('//td/table[@class="td1"]//tr/td[2]/text()'),
                        'dias': row.xpath('//td/table[@class="td1"]//tr/td[3]/text()'),
                        'cupos': row.xpath('//td[6]/text()')[0],
                        'disponibles': row.xpath('//td[7]/text()')[0],
                        'profesor': row.xpath('//td/table//td[@class="tdprofesor"]/text()')[1],
                    } 
                
                except:
                    pass
       