# URLINA (WORK IN PROCESS)

Basic testing of sites by Pipeline

## What is it?

URLINA is a easy software for checking HTTP-status codes of your site. It's really best additinal for your Pipeline! And not one corner of the site will be forgotten!

### It's easy work

You need to create a check-list of URL with expected status сode.  Then start URLINA and she will check and compare real and expected status code for any URL. If they is identical - APLINA will return the "OK" status of check. If not - will return the "FAIL" status, unsuccess status code of run command, Fail your Pipeline, arrange global darkening, will erupt all volcanoes on earth, destroy humanity and put out the sun (the last 4 features are still in development).

### It's easy starting

#### First

Create a yaml-file with follow content:

`test.yaml`

```yaml
urlina:
  - url: https://github.com
    code: 200
  - url: http://github.com
    code: 301
  - url: https://github.com/settings/profile
    code: 422
    method: POST
```

Where is:

* **url** (req) - URL for testing.
* **code** (req) - the comparing code status
* **method** - setting a requiest method (default: GET)

#### Second

Start URLINE:

`./urline.py -f test.yaml`

Where is:

* **-f** - a filename with testing list
* **-s** - not failing command, if status codes is do not match

#### Last

See result!

