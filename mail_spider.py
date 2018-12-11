from urllib import parse
import urllib
import re
import time


def getresponse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    request.add_header('Connection', 'keep-alive')
    response = urllib.request.urlopen(request)

    data = None
    try:
        data = response.read().decode('utf-8', "ignore")
    except UnicodeDecodeError:
        data = response.read()
    return data


def gettiebalistnumbers(name):
    url = 'http://tieba.baidu.com/f?'
    word = {
            'kw': name,
            'pn': 0
            }
    word = parse.urlencode(word)
    url = url + word
    data = getresponse(url)
    # data = data.replace('<!--', '').replace('-->', '')
    guanzhu_restr = '<span class="card_menNum">([\s\S]*?)</span>'
    guanzhu_regex = re.compile(guanzhu_restr, re.IGNORECASE)
    guanzhu_list = re.findall(guanzhu_regex, data)
    guanzhu_number = eval(guanzhu_list[0].replace(',', ''))

    tiezi_restr = '<span class="card_infoNum">([\s\S]*?)</span>'
    tiezi_regex = re.compile(tiezi_restr, re.IGNORECASE)
    tiezi_list = re.findall(tiezi_regex, data)
    tiezi_number = eval(tiezi_list[0].replace(',', ''))

    zhuti_rester = '共有主题数<span class="red_text">([\s\S]*?)</span>个'
    zhuti_regex = re.compile(zhuti_rester, re.IGNORECASE)
    zhuti_list = re.findall(zhuti_regex, data)
    zhuti_number = eval(zhuti_list[0].replace(',', ''))

    return guanzhu_number, tiezi_number, zhuti_number


def gettiebalist(name):
    number_tuple = gettiebalistnumbers(name)
    number = 0
    total = 0
    url_list = []
    while True:
        total = number * 50

        url = 'http://tieba.baidu.com/f?kw=' + name + '&pn=' + str(total)
        url_list.append(url)

        number += 1
        if number_tuple[2] - total < 50:
            break
    return url_list


def gettiezilist(name):
    url_list = gettiebalist(name)
    intro_url_list = []
    for url in url_list:
        data = getresponse(url)
        div_redstr = '<li class=" j_thread_list clearfix" data-field=([\s\S]*?)<div class="threadlist_author pull_right">'
        div_regex = re.compile(div_redstr, re.IGNORECASE)
        # 帖子列表
        div_list = re.findall(div_regex, data)

        href_list = 'href="/p/(\d+)"'
        href_regex = re.compile(href_list, re.IGNORECASE)
        for div_str in div_list:
            href_list = re.findall(href_regex, div_str)
            print('-'*50)
            print(href_list)
            intro_url = 'http://tieba.baidu.com/p/' + href_list[0]
            intro_url_list.append(intro_url)
        # 只抓取第一页,删除抓取所有
        break
        # time.sleep(1)
    return intro_url_list


def getmail(name):
    mail_restr = r'([A-Z0-9_+]+@[A-Z0-9]+\.[A-Z]{2,6})'
    mail_regex = re.compile(mail_restr, re.IGNORECASE)
    intro_url_list = gettiezilist(name)
    for intro_url in intro_url_list:
        data = getresponse(intro_url)
        '''
        去一共几页
        '''
        page_re_str = '共<span class="red">(\d+)</span>页</li>'
        page_re_gex = re.compile(page_re_str, re.IGNORECASE)
        page_re_list = []
        try:
            page_re_list = re.findall(page_re_gex, data)
        except TypeError:
            page_re_list = re.findall(page_re_gex, data.decode())
        print(intro_url)
        print(page_re_list)
        page = eval(page_re_list[0])
        print(page)
        for i in range(page):

            print(i)
            page_url = intro_url + '?pn=' + str(i+1)
            print(page_url)
            data = getresponse(page_url)

            mail_list = []
            try:
                mail_list = re.findall(mail_regex, data)
            except TypeError:
                mail_list = re.findall(mail_regex, data.decode())
            if len(mail_list) > 0:
                print(mail_list)
            print('=' * 20)


def main():
    getmail('python')


if __name__ == "__main__":
    main()
