from requests import get
from bs4 import BeautifulSoup


REGION_LINKS = (
    'https://oliygoh.uz/oliygohlar?c=1703',
    'https://oliygoh.uz/oliygohlar?c=1706',
    'https://oliygoh.uz/oliygohlar?c=1708',
    'https://oliygoh.uz/oliygohlar?c=1710',
    'https://oliygoh.uz/oliygohlar?c=1712',
    'https://oliygoh.uz/oliygohlar?c=1714',
    'https://oliygoh.uz/oliygohlar?c=1718',
    'https://oliygoh.uz/oliygohlar?c=1722',
    'https://oliygoh.uz/oliygohlar?c=1724',
    'https://oliygoh.uz/oliygohlar?c=1726',
    'https://oliygoh.uz/oliygohlar?c=1727',
    'https://oliygoh.uz/oliygohlar?c=1730',
    'https://oliygoh.uz/oliygohlar?c=1733',
    'https://oliygoh.uz/oliygohlar?c=1735'
)


with open('databases/institutes.txt', 'w') as file:
    for region_link in REGION_LINKS:
        response = get(region_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # region
        file.write(soup.select_one('h1').text.strip() + '\n')

        # names and links
        institutes = map(
            (lambda anchor: (anchor.text.strip(), anchor.attrs['href'])),
            soup.select('.univerlist-item__left > a')
        )

        for institute in institutes:
            file.write(institute[0] + '\n')
            response = get(institute[1])
            soup = BeautifulSoup(response.content, 'html.parser')

            table = map((lambda r: '|'.join((
                r.select_one('p.text-dark-gray-100').text.strip(),
                r.select_one('.quotes div').text.strip(),
                r.select_one('.td:nth-child(2) .bullet').text.strip(),
                r.select_one('.td:nth-child(2) .bullet:last-child').text.strip(),
                r.select_one('.td:nth-child(3) .bullet').text.strip(),
                r.select_one('.td:last-child .bullet:last-child').text.strip()
            ))), soup.select('.tbody .tr'))

            for row in table:
                file.write(row + '\n')
            else:
                file.write('\n')
        else:
            file.write('\n\n')
