import requests
import json

"""
Usage: 

import confluence_rest as con

auth_creds = ('username', 'password')
page_id = '12345678'

page_data = con.get_confluence_page(page_id, auth_creds)
new_content_string = "<h1>Ni hao</h1>"
new_page_data = con.edit_page_content(page_data,new_content_string)

con.post_to_confluence(new_page_data, auth_creds)

"""

confluence_url = "https://confluence-address.com"

def get_confluence_page(page_id, auth_creds):
    """auth_creds is a two-element tuple of username and password"""

    req_string = ("{}/rest/api/content/{}?expand=body.storage,"
                  "version,ancestors,space").format(confluence_url, page_id)
    try:
        r = requests.get(req_string, auth=auth_creds)
        if r.status_code == 500:
            print r.json()['message']
            return
        page_data = r.json()
        return page_data
    except Exception as e:
        print e


def get_content(page_data):
    try:
        text = page_data['body']['storage']['value']
        content = text.encode('utf-8')
        return content
    except Exception as e:
        print e


def edit_page_content(page_data, content):

    if content == "":
        return "No content"

    d = page_data
    version_num = int(d['version']['number']) + 1

    update = json.dumps(
        {
            'id': d['id'],
            'type': d['type'],
            'title': d['title'],
            'space': {'key': d['space']['key']},
            "version": {"number": version_num},
            'body':
            {
                'storage':
                {
                    'representation': 'storage',
                    'value': content,
                }
            },
            'ancestors': d['ancestors'],
        })

    return update


def post_to_confluence(updated_content, auth_creds):
    try:
        updated_content_json = json.loads(updated_content)
        url = '{}/rest/api/content/{}'.format(
            confluence_url, updated_content_json['id'])
        requests.put(
            url, auth=auth_creds, data=updated_content,
            headers={'Content-Type': 'application/json'})
        return "Updated {}".format(updated_content_json['title'])
    except Exception as e:
        print e
