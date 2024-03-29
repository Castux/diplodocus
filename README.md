![Dino](dinosaur.png)

# Diplodocus

A simple Discord bot to play Diplomacy. It relies on the [diplomacy](https://github.com/diplomacy/diplomacy) Python package, which comes with several variants and supports a [subset](https://github.com/diplomacy/diplomacy/blob/master/diplomacy/README_MAPS.txt) of the [DPJudge format](http://uk.diplom.org/?page=Map) for variant definition.

Note that this is a single-game bot. To play several games at once, you'll need to create and run one bot per game.

## Installing and starting

Requirements:

- Python 3
- pip

Preparation:

- Create a bot on your Discord developer page, and invite it to your server. For instance by following [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html).

Installation:

*(This assumes a Linux system. You might have to adapt the commands to fit yours.)*

- Run `./setup.sh`.
- Rename or copy `config-model.json` to `config.json`. Fill in your Discord bot token, and the mapping between usernames and game powers.
- Run `./run.sh`

You can set the `variant` field in the config file to any of the [variants](https://github.com/diplomacy/diplomacy/tree/master/diplomacy/maps) included in the library, or a path to a custom `.map` file.

You can set the `gm` field to a username, which will be the only one able to run `adjudicate`. If you omit the field, everyone will be able to (though only on public channels).

For convenience, an example `systemd` service file is provided, to run the bot as an auto-restart service on a Linux machine. Fill in the correct paths, copy it to `/etc/systemd/system/`, and then start the service with `sudo systemctl start diplodocus`.

## Usage

The bot answers to commands (prefixed `!` by default) in public channels or private messages.

```
adjudicate Adjudicate the current phase
check      Check your orders for this phase
dump       Send a JSON file for the current game state and its history
gamestate  Show the game state
help       Shows this message
hint       See all possible valid orders for a province
history    Show all previous moves in the game
remove     Remove your orders for this phase
send       Send your orders for the phase
simulate   Simulate a set of orders for the current phase
status     Show the current phase
```

## License

Diplodocus is released under the [MIT license](LICENSE).

This project uses the [diplomacy](https://github.com/diplomacy/diplomacy) (AGPL), and the [discord](https://github.com/Rapptz/discord.py) Python packages (MIT license).

Dinosaur logo by Freepik, [Flaticon license](https://www.flaticon.com/free-icon/dinosaur_8013688).
