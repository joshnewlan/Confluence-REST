import requests
import json
import urllib

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

confluence_url = "https://confluence.company.com"

def check_page_exists(title,auth_creds):
    title = urllib.quote_plus(title)
    r = requests.get("{}/rest/api/content?title={}".format(confluence_url,title),
        auth=auth_creds)
    if r.json()['results']:
        return True
    else:
        return False


def get_page_id(title,auth_creds):
    title = urllib.quote_plus(title)
    r = requests.get("{}/rest/api/content?title={}".format(confluence_url,title),
        auth=auth_creds)
    return r.json()['results']['id']


def get_user_id(username,auth_creds):
    url = ("{}/rest/prototype/1/search/user.json?"
        "max-results=10&query={}".format(confluence_url,username))
    r = requests.get(url,auth=auth_creds)

    for u in r.json()['result']:
        if u['username'] == username:
            userKey = u['userKey']
            return userKey


def get_confluence_page(page_id, auth_creds):
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
            'ancestors': [{
                'type': 'page',
                'id': d['ancestors'][-1]['id']
            }],
        })

    return update


def post_to_confluence(updated_content, auth_creds):
    try:
        updated_content_json = json.loads(updated_content)
        url = '{}/rest/api/content/{}'.format(
            confluence_url, updated_content_json['id'])
        r = requests.put(
            url, auth=auth_creds, data=updated_content,
            headers={'Content-Type': 'application/json'})
        print r.status_code
        # print r.content
        print "Updated {}".format(updated_content_json['title'])
        # return 
    except Exception as e:
        print e

def create_new_page(parent_id,auth_creds,title=None,content=None,space=None):

    try: 
        parent_id = int(parent_id)
    except ValueError:
        print "Please provide the page parent_id."
        
    if space == None:
        space = "PROD"
    if title == None:
        title = "New Confluence Page"
    if content == None:
        content = "<p>New page content.</p>"

    # title = urllib.quote_plus(title)
    
    page_data = json.dumps(
        {
            "type": "page",
            "title": title,
            "space": {"key": space},
            "body":
            {
                'storage':
                {
                    'representation': 'storage',
                    'value': content,
                }
            },
            'ancestors': [{
                'type': 'page',
                'id': str(parent_id)
            }],
        })

    url = "{}/rest/api/content/".format(confluence_url)

    r = requests.post(
        url, 
        auth=auth_creds, 
        data=page_data,
        headers={'Content-Type': 'application/json'})

    print r
    # print r.content

    page_id = r.json()['id']

    return page_id
