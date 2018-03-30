import urllib2
import re
import json
import matplotlib.pyplot as plt
import os
from time import time


def get_categories(base_url):
    # step 1: get 23 categories' urls
    response = urllib2.urlopen(base_url)  
    html = response.read()
    pattern = re.compile('\/data\/list\/\?q=cat:[a-z0-9]{3}\sprovider:tsdl')
    match = pattern.findall(html) # match is a list.
    # /data/list/?q=cat:ecc provider:tsdl
    return match


def parse_subcates(sub_url):
    response = urllib2.urlopen(sub_url)  
    html = response.read()
    pattern = re.compile('\/data\/set\/[a-z0-9]{4}\/[a-z0-9\-]+\"')
    match = pattern.findall(html)
    # /data/set/22tb/exchange-rate-twi-may-1970-aug-1995"
    results = []
    for m in match:
        results.append(m[10:14])
    return results


def download_data(json_url, cat, ids):
    response = urllib2.urlopen(json_url)  
    json_data = response.read()
    list_data = json.loads(json_data)
    title = list_data[0]['title']
    file_name = './' + cat + '/' + ids + '-' + title
    try:
        f = open(file_name +'.txt', 'w')
    except IOError:
        file_name = file_name[:min(20, len(file_name))]
        f = open(file_name +'.txt', 'w')
    final_data = []
    write_data = []
    for d in list_data[0]['data']:
        final_data.append(d[1])
        write_data.append(str(d[1])+'\n')
    f.writelines(write_data)
    f.close()
    # draw
    print len(final_data)
    plt.plot(range(len(final_data)), final_data)
    plt.savefig(file_name+'.png')


if __name__ == '__main__':
    
    url_subcates = get_categories("https://datamarket.com/data/list/?q=provider%3Atsdl")
    for us in url_subcates:
        start = time()
        os.mkdir('./' + us[18:21]+'/')
        sub_url = "https://datamarket.com" + us
        ids = parse_subcates(sub_url)
        for id in ids:
            json_url = "https://datamarket.com/api/v1/list.json?callback=&ds=" + id + "&include_ids=1&include_values=0"
            download_data(json_url, us[18:21], id) # url, ecc, 22tb
        stop = time()
        print(str(stop-start) + "s")
        print ''
    
    