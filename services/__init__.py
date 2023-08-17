import re
from page_requests import *
from decorators import envelope


@envelope
def get_company_list():
    content = request_index_page()
    pattern_str = '<option value="(.+)\/index.html">(.+)<\/option>'
    pattern = re.compile(pattern_str, re.MULTILINE)
    found = pattern.findall(content)
    return [{'slug': f[0], 'name': f[1]} for f in found]

def get_synth_endpoint(company, synth):
    return f'/companies/{company}/synths/{synth[:-5]}'

def get_company(company):
    content = request_company_page(company)
    title_pattern_str = '<h3 align="center">(.+)</h3>'
    title_pattern = re.compile(title_pattern_str, re.MULTILINE)
    title = title_pattern.search(content).group(1)
    paragrahphs_ptn_str = '<[pP]>(.+)\n'
    paragrahphs_ptn = re.compile(paragrahphs_ptn_str, re.MULTILINE)
    paragraphs = paragrahphs_ptn.findall(content)
    filtered = [p for p in paragraphs if not p.startswith('<font')]
    inner_links_ptn_str = '<a href="([^"]+)">([^<]+)<\/a>'
    inner_links_ptn = re.compile(inner_links_ptn_str)
    for n in range(len(filtered)):
        if filtered[n].endswith('</p>') or filtered[n].endswith('</P>'):
            filtered[n] = filtered[n][:-4]

    about = '\n'.join(filtered)
    inner_links = inner_links_ptn.findall(about)
    links = []
    for n in range(len(inner_links)):
        to_list = list(inner_links[n])
        if to_list[0].find('/') < 0:
            to_list[0] = get_synth_endpoint(company, to_list[0])

        links.append({'url': to_list[0], 'caption': to_list[1]})

    return {
        'title': title,
        'about': about,
        'links': links,
        'synths': get_company_synths_from_content(content, company)
    }

def get_company_synths(company):
    content = request_company_page(company)
    synths = get_company_synths_from_content(content, company)
    synths['company'] = company
    return synths

@envelope
def get_company_synths_from_content(content, company):
    inner_links_ptn_str = '<a href="([^"]+)">([^<]+)<\/a>'
    inner_links_ptn = re.compile(inner_links_ptn_str)
    synth_list_ptn_str = '^(.+)<br/>'
    synth_list = re.compile(synth_list_ptn_str, re.MULTILINE).findall(content)[2:-9]
    synths = []
    for synth in synth_list:
        if synth.find('<a href="') > -1:
            link = inner_links_ptn.findall(synth)
            print(link[0][0])
            synths.append({
                'name': link[0][1],
                'url': get_synth_endpoint(company, link[0][0])
            })

        else:
            synths.append({'name': synth.strip()})

    return synths