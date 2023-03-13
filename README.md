# Diplodocus

A simple Discord bot to play Diplomacy. It relies on the [diplomacy](https://github.com/diplomacy/diplomacy) Python package, which comes with several variants and supports a [subset](https://github.com/diplomacy/diplomacy/blob/master/diplomacy/README_MAPS.txt) of the [DPJudge format](http://uk.diplom.org/?page=Map) for variant definition.

## Installing and starting

Requirements:

- Python 3
- pip

Installation:

- Run `./setup.sh`.
- Rename or copy `config-model-lua` to `config.lua`. Fill in your Discord bot token.
- Run `./run.sh`

For convenience, an example `systemd` service file is provided, to run the bot as an auto-restart service on a Linux machine. Fill in the correct paths, copy it to `/etc/systemd/system/`, and then start the service with `sudo systemctl start diplodocus`.

## Usage

The bot answers to commands (prefixed `!` by default) in public channels or private messages.

```
adjudicate Adjudicate the current phase
check      Check your orders for this phase
gamestate  Show the game state
help       Shows this message
hint       See all possible valid orders for a province
ping       Ping-pong, baby!
remove     Remove your orders for this phase
send       Send your orders for the phase
simulate   Simulate a set of orders for the current phase
status     Show the current phase
```

## License

Diplodocus is released under the [MIT license](LICENSE).

This project uses the [diplomacy](https://github.com/diplomacy/diplomacy) (AGPL), and the [discord](https://github.com/Rapptz/discord.py) Python packages (MIT license).
