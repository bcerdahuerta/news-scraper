import requests
import lxml.html as html
import os
import datetime

#XPath Expressions
HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//a[@class="economiaSect" or @class="kicker globoeconomiaSect"]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_CONTENT = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)

        if response.status_code ==200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                content = parsed.xpath(XPATH_CONTENT)
                
            except IndexError:
                return

            print(title)
            print(summary)
            print(content)
            with open('{}/{}.txt'.format(today, title), 'w', encoding='utf-8') as f:

                    f.write(title)
                    f.write('\n\n')
                    f.write(summary)
                    f.write('\n\n')
                    for p in content:
                        f.write(p)
                        f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

#Getting and parsing Home HTML, also making a dir with today name
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            #Getting URLs with xpath expression
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(len(links_to_notices))
            today = datetime.date.today().strftime('%m-%d-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
                
                for link in links_to_notices:
                    #Getting and parsing HTML for each notice page
                    parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == '__main__':
    run()