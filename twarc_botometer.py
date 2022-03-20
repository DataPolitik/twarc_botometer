import json
import ijson
import logging
import click
import botometer as bt

from typing import Generator, Set, Dict
from io import TextIOWrapper

from tweepy import TweepError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('')


def generate_config_file(outfile: TextIOWrapper) -> None:
    click.echo('''{
      "rapidapi_key": "YOUR_RAPID_API_KEY",
      "twitter_app_auth": {
            "consumer_key": "CONSUMER_KEY",
            "consumer_secret": "CONSUMER_SECRET",
            "access_token": "ACCESS_TOKEN",
            "access_token_secret": "ACCESS_TOKEN_SECRET"
        }
}''', file=outfile)


@click.command()
@click.option('--infile', required=False, type=click.File('rb'), default='-')
@click.option('--outfile', required=False, type=click.File('w'), default='-')
@click.option('--config', required=False,  type=click.File('r'))
@click.option('--generate_config', required=False,  type=click.File('w'))
def botometer(infile: TextIOWrapper, outfile: TextIOWrapper, config: TextIOWrapper, generate_config: TextIOWrapper):
    if generate_config is not None:
        logger.info("Generating config information file.")
        generate_config_file(generate_config)
        exit(0)

    config_data: Dict or None = None
    try:
        config_data = json.load(config)
    except json.decoder.JSONDecodeError:
        logger.critical("The config file is empty or it has an invalid value.")
        exit(1)

    is_json: bool = True
    try:
        json.loads(infile.readline())
    except ValueError:
        is_json = False
    finally:
        infile.seek(0,0)

    user_ids: Set[str] = set()

    if is_json:
        json_file = ijson.items(infile, '', multiple_values=True)
        tweet_generator: Generator = (o for o in json_file)

        for tweet in tweet_generator:
            user_ids.add(tweet['author_id'])
    else:
        is_next_line: bool = True
        while is_next_line:
            next_line: bytes = infile.readline()
            if not next_line:
                is_next_line = False
            else:
                user_id: str = next_line.decode().strip().replace(',', '')
                user_ids.add(user_id)

    rapidapi_key: str = config_data['rapidapi_key']
    twitter_app_auth: Dict[str, str] = config_data['twitter_app_auth']
    botometer_manager: bt.Botometer = bt.Botometer(wait_on_ratelimit=True,
                                                                 rapidapi_key=rapidapi_key,
                                                                 **twitter_app_auth)

    click.echo("user_id, botometer_score", file=outfile)
    for user_id in user_ids:
        try:
            botometer_result: Dict = botometer_manager.check_account(user_id)
            click.echo("{},{}".format(user_id, botometer_result['cap']['universal']), file=outfile)
        except TweepError as e:
            logger.error("API error with user id: "+ user_id)
            logger.error(e)


if __name__ == '__main__':
    botometer()