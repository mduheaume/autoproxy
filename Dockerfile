FROM nginx
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install jinja2
ADD config.py config.py
CMD python config.py > /etc/nginx/conf.d/default.conf && nginx -g "daemon off;"
