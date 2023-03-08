# Diplodocus

A very rudimentary Discord bot to play Diplomacy (or any other game that requires submitting simultaneous secret orders). All it does it gather players' orders, that can then be revealed publicly all at once.

## Installing and starting

- Run `./setup.sh`. This will download [luvit](https://luvit.io/) and the [Discordia](https://github.com/SinisterRectus/Discordia) library.
- Rename or copy `config-model-lua` to `config.lua`. Fill in your Discord bot token.
- Run `./run.sh`

For convenience, an example `systemd` service file is provided, to run the bot as an auto-restart service on a Linux machine. Fill in the correct paths, copy it to `/etc/systemd/system/`, and then start the service with `sudo systemctl start diplodocus`.

## Usage

The bot answers to commands (prefixed `!` by default) in public channels or private messages.

__Player commands__

- **!send \<orders\>**: send your orders for the current phase. They can be on multiple lines. That will overwrite previously sent orders if any.
- **!check**: check what are your current orders for the phase.
- **!remove**: delete your current orders.
- **!status**: see what the current phase is and how many have submitted orders so far.

__GM commands__ (restricted to public channels for transparency)

- **!startphase \<phase\>**: start a new phase with the given name, which opens order submissions.
- **!stopphase**: stop the current phase and show all the orders submitted during the phase.

## License

Diplodocus is released under the [MIT license](LICENSE).

This project uses [Discordia](https://github.com/SinisterRectus/Discordia) and [Lua](https://lua.org/), both MIT license, and [luvit](https://luvit.io/), Apache License 2.0.
