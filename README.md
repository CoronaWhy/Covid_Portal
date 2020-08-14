# Covid_Portal


### preconfig

you need to provide hostname that would be used for traefik reverse proxy

```export traefikhost=<your domain>```

then you simply run 
```docker-compose up -d```

this would start [traefik](https://containo.us/traefik/) container that would route

- `portal.<your domain>` for `covidPortalFrontEnd`

- `portaldb.<your domain>` for `webCovidPortal`

## TODO

currently docker-compose.yml uses prebuild images that have hardcoded env settings for django app host `portaldb.stage.coronawhy.org`. This should be changed in the future

