import aiohttp
import asyncio
#Potrebne importy pro projekt

async def download_url(url):    #Pomocna funkce pro stazeni kazde poskytnute url adresy
    #url = adresa URL
    async with aiohttp.ClientSession() as session:
        try:        #Pokusime se stahnout url adresu
            async with session.get(url) as response:    #Pokud se podari:
                return (response.status, url)                  #Vracime status,URL adresu
        except aiohttp.ClientError:                     #Pokud se nepodari:
            return ('aiohttp.ClientError', url)                #Vracime ClientError,URL adresu

async def get_urls(urls):
    #urls = lsit obsahujici vsechny adresy URL
    tasks = [asyncio.create_task(download_url(url)) for url in urls] #Vytvorime si list obsahujici jednotlive tasky pro jednotlive URL adresy
    results = await asyncio.gather(*tasks)  #Pomoci asyncion.gather spustime vsechny tasky (jednu pro kazdou URL adresu) najednou a pomoci await pockame na dokonceni vsech tasku
    return results          #Vysledek bude ulozen do results a nasledne results bude vracen funkci get_urls()
    #results je list dvojic (status, URL) vsech URL adres
if __name__ == '__main__':

    urls = ['https://www.fit.vutbr.cz', 'https://www.szn.cz', 'https://www.alza.cz', 'https://office.com', 'https://aukro.cz']

    # for MS Windows

    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    res = asyncio.run(get_urls(urls))

    print(res)
