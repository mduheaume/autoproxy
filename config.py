import os
from jinja2 import Template

template = Template('''
{% for name, link in upstreams.items() -%}
upstream {{ name }} {
    server {{ link }};
}
{% endfor -%}

server {
    listen 80;
    server_name "~^(?<name>[^\.]*)\.(?<domain>.+)$";
    location / {
        proxy_pass http://$name;
        proxy_set_header Host               $http_host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-Proto  $scheme;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_redirect     off;
    }
}
    ''')

upstreams = {os.environ['%s_NAME' % k[:-12]].split('/')[-1]: v.split('/')[-1] \
        for k, v in os.environ.items() if k.endswith('PORT_80_TCP')}
print template.render(upstreams=upstreams)