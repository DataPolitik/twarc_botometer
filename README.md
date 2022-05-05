# Twarc-botometer
## A botometer-check plugin for twarc

This plugin reads a json file generated by Twarc and retrieve user stats from Botometer (https://botometer.osome.iu.edu/).

## Usage

`main.py -i <INFILE> -o <OUTFILE> [[-l N ] [ -c csv|json] | [-gc]]`

* **-i** | **- -infile**: The path to the input file. It must be a flat twarc json file.
* **-o** | **- -outfile**: The path to the output file.
* **-l** | **- -limit**: Analyses only the firnst N tweets from the file.
* **-c** | **- -config**: Path to the config file.
* **-gc** | **- -generate_config**: Generate a default config file..
 
## Config file

The config file has the following structure:

```javascript
{
      "rapidapi_key": "YOUR_RAPID_API_KEY",
      "twitter_app_auth": {
            "consumer_key": "CONSUMER_KEY",
            "consumer_secret": "CONSUMER_SECRET",
            "access_token": "ACCESS_TOKEN",
            "access_token_secret": "ACCESS_TOKEN_SECRET"
        }
}
```
