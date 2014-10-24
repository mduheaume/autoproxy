# autoproxy

A docker image for reverse proxying to linked web containers.

## Usage

Let's assume you have two docker containers that expose a webserver and you 
have a host at `yourdomain.com` where you run the containers... 

```bash
$ docker run -d -p 81:80 --name foo dekim/foo
$ docker run -d -p 82:80 --name bar dekim/bar
```

But rather than access them as `http://yourdomain.com:81` and 
`http://yourdomain.com:82` you want to use sub domains like so: 
`http://foo.yourdomain.com` and `http://bar.yourdomain.com`.

Simply run the web containers without exposing any ports on the host...

```bash
$ docker run -d --name foo dekim/foo
$ docker run -d --name bar dekim/bar
```

Then run the autoproxy container with links to the two web containers...

```bash
$ docker run -d -p 80:80 --link foo:foo --link bar:bar dekim/autoproxy
```

This will start the autoproxy container listening on port 80. Any requests it 
receives for `foo.yourdomain.com` will be proxied to the `foo` container, and any 
requests for `bar.domain.com` will be proxied to the `bar` container.


You can supply as many linked containers as you like. The autoproxy container 
will automatically proxy requests to linked containers that expose port 80 by 
matching the subdomain in the request's host header to the containers link 
alias.

