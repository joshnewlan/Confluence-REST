# Confluence-REST
### Usage
```python
import confluence_rest as con
auth_creds = ('username', 'password')
page_id = '12345678'
page_data = con.get_confluence_page(page_id, auth_creds)
new_content_string = "<h1>Ni hao</h1>"
new_page_data = con.edit_page_content(page_data,new_content_string)
con.post_to_confluence(new_page_data, auth_creds)
```
