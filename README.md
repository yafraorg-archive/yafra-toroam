# yafra.org - toroam

## Google App Engine Python

## Development Environment
 * PyCharm Jetbrains IDE
 * Google App Engine Python SDK
 * Google App Engine account and project

### Flexible App Engine

Install the google cloud sdk and cmd line tools: https://cloud.google.com/sdk/

 * Version 2 is based on flexible environment
```bash
pip install --upgrade gcloud
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```

Create a service account and download the json file and add it to your .gitignore file
See also https://developers.google.com/identity/protocols/application-default-credentials#whentouse



## Automatic build and run environment
 * Google: http://toroamgps.appspot.com/

## Further information
read more about yafra on:
 * http://www.yafra.org
 * https://github.com/yafraorg/yafra/wiki
 * raise a ticket related to yafra.org framework: https://github.com/yafraorg/yafra/issues?state=open
 * raise a ticket related to this java code: https://github.com/yafraorg/yafra-java/issues?state=open
