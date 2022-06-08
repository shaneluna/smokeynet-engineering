# Weather Notebooks

All datetimes from synoptic mesonet API have been set to be returned in UTC in the request.

## Getting Started

1. Create a copy of `config.json.example` and remove the `.example`

2. Update the `synoptic_api_token` value

In `config.json`:

- weather_neworks format:

```
# from synoptic api
network_id: SHORTNAME
```

- weather_datetime format:

```
YYYYmmddHHMM
```