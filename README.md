# OHRWhatsNewDiscordBot

A Discord bot that watches for and reports new git commits, changelog updates (whatsnew.txt and IMPORTANT-nightly.txt), nightly builds for the OHRRPGCE, and also new and updated OHRRPGCE games on itch.io and Slime Salad. It also posts embeds when someone links to a game on Slime Salad.

This bot can only be added to one guild (server) at a time.

# Installation:

1. Install Python 3 module requirements: `pip install -r requirements.txt`

2. Fetch ohark with `git submodule init`, `git submodule update`

3. Create a new app at https://discord.com/developers, and on the Installation tab ensure Install Link is "Discord Provided Link", add the "bot" scope to the Guild Install, and add permissions including Connect, Send Messages, Embed Links, Use Embedded Activities. On the Bot tab ensure 'Message Content Intent' is enabled.

4. Make a copy of `OHR-WhatsNewBot/example_config.json`, name it `OHR-WhatsNewBot/config.json` and add your `APP_TOKEN`, `UPDATES_CHANNEL` (where updates go and !check* commands are restricted to) and `ADMIN_ROLES`. Possibly customise other options (see the top of `bot.py` for docs).

The channel IDs can be obtained by right clicking on a channel on discord and selecting "Copy Channel ID". The `APP_TOKEN` is obtained by Resetting the token on the Bot tab at https://discord.com/developers

# Usage 
1. `cd OHR-WhatsNewBot`

2. Launch with: `python3 bot.py` -- Success looks like this:

```
discord.client logging in using static token
discord.gateway Shard ID None has connected to Gateway (Session ID: cdcac418e852ee7fc167f2cb3ab77635).
Logged in as OHR Whats New Bot
Started OHR WhatsNew Bot
------
No/invalid state.json, initialising state
```

The bot will then immediately perform its first check (if this is the first run this will record the current git/SS/itch.io state and report no updates).

3. In any of the allowed channels, users can use `!help`, `!check` and other commands.

4. You can use the `!rewind_commits <n>` command followed by `!check` to test the bot.

5. Or just do nothing and the bot will post devlog updates once a day, and SS gamelist updates 3 times a day, if there are any. It will take up to `MINUTES_PER_CHECK` after nightly builds are built before it posts any git commits (and log changes) made that day. If `MAX_CHECK_DELAY_HOURS` (26) pass without new nightly builds, it'll go ahead and post git commits regardless.

6. Ctrl+C to kill the bot. It'll read `state/state.json` and resume where it left off when restarted, without missing anything.

# Known issues

None.
