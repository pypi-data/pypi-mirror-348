# Urlscan

[![main](https://github.com/firecat53/urlscan/actions/workflows/main.yml/badge.svg)](https://github.com/firecat53/urlscan/actions/workflows/main.yml)

## Contributors

Scott Hansen \<tech@firecat53.net\> (Author and Maintainer)

Maxime Chatelle \<xakz@rxsoft.eu\> (Debian Maintainer)

Daniel Burrows \<dburrows@debian.org\> (Original Author)

## Purpose and Requirements

Urlscan is a small program that is designed to integrate with the "mutt"
mailreader to allow you to easily launch a Web browser for URLs contained in
email messages. It is a replacement for the "urlview" program.

Requires: Python 3.7+ and the python-urwid library

## Features

Urlscan parses an email message or file and scans it for URLs and email
addresses. It then displays the URLs and their context within the message, and
allows you to choose one or more URLs to send to your Web browser.
Alternatively, it send a list of all URLs to stdout.

Relative to urlview, urlscan has the following additional features:

- Support for emails in quoted-printable and base64 encodings. No more stripping
  out =40D from URLs by hand!

- The context of each URL is provided along with the URL. For HTML mails, a
  crude parser is used to render the HTML into text. Context view can be toggled
  on/off with `c`.

- URLs are shortened by default to fit on one line. Viewing full URL (for one or
  all) is toggled with `s` or `S`.

- Jump to a URL by typing the number.

- Incremental case-insensitive search with `/`.

- Execute an arbitrary function (for example, copy URL to clipboard) instead of
  opening URL in a browser.

- Use `l` to cycle through whether URLs are opened using the Python webbrowser
  module (default), xdg-open (if installed) or opened by a function passed on
  the command line with `--run` or `--run-safe`.

- Configure colors and keybindings via ~/.config/urlscan/config.json. Generate
  default config file for editing by running `urlscan -g`. Cycle through
  available palettes with `p`. Set display width with `--width`.

- Set the urwid color mode with `--colors`. Options include 'true' (2**24
  colors), '256', '88', '16', '8', or 'mono'. Default is '16'.

- Copy URL to clipboard with `C` or to primary selection with `P`.  Requires
  xsel or xclip.

- Run a command with the selected URL as the argument or pipe the selected
  URL to a command.

- Show complete help menu with `F1`. Hide header on startup with `--nohelp`.

- Use a custom regular expression with `-E` for matching urls or any
  other pattern. In junction with `-r`, this effectively turns urlscan
  into a general purpose CLI selector-type utility.

- Scan certain email headers for URLs. Currently `Link`, `Archived-At` and
  `List-*` are scanned when `--headers` is passed.

- Queue multiple URLs for opening and open them all at once with `a` and `o`.

## Installation and setup

To install urlscan, install from your distribution repositories, from Pypi, or do
a local development install with pip -e:

    pipx install urlscan

    OR

    pip install --user urlscan

    OR

    cd <path/to/urlscan> && pip install --user -e .

**NOTE**

    The minimum required version of urwid is 1.2.1.

Once urlscan is installed, add the following lines to your .muttrc:

    macro index,pager \cb "<pipe-message> urlscan<Enter>" "call urlscan to
    extract URLs out of a message"

    macro attach,compose \cb "<pipe-entry> urlscan<Enter>" "call urlscan to
    extract URLs out of a message"

Once this is done, Control-b while reading mail in mutt will automatically
invoke urlscan on the message.

> Note for Neomutt users: [As of version
> `2023-05-17`](https://github.com/neomutt/neomutt/releases/tag/20230517) true
> color support was implemented. If you are using true color support with Neomutt,
> or are encountering the error `setupterm: could not find terminfo database`,
> then you should also add `TERM=xterm-256color` to your macro in `.muttrc`.
> See more here [#135](https://github.com/firecat53/urlscan/issues/135). For example:
> `macro index,pager  \cb "<pipe-message>  TERM=xterm-256color urlscan<Enter>" "call urlscan to
extract URLs out of a message"`

To choose a particular browser, set the environment variable BROWSER. If BROWSER
is not set, xdg-open will control which browser is used, if it's available.:

    export BROWSER=/usr/bin/epiphany


## Command Line usage

    urlscan OPTIONS <file>

    OPTIONS [-c, --compact]
            [-d, --dedupe]
            [-E, --regex <expression>]
            [-f, --run-safe <expression>]
            [-g, --genconf]
            [-H, --nohelp]
            [    --headers]
            [-n, --no-browser]
            [-p, --pipe]
            [-r, --run <expression>]
            [-R, --reverse]
            [-s, --single]
            [-w, --width]
            [-W  --whitespace-off]
            [-C, --colors {true,256,88,16,8,mono}]

Urlscan can extract URLs and email addresses from emails or any text file.
Calling with no flags will start the curses browser. Calling with '-n' will just
output a list of URLs/email addressess to stdout. The '-c' flag removes the
context from around the URLs in the curses browser, and the '-d' flag removes
duplicate URLs. The '-R' flag reverses the displayed order of URLs and context.
Files can also be piped to urlscan using normal shell pipe mechanisms: `cat
<something> | urlscan` or `urlscan < <something>`. The '-W' flag condenses the
display output by suppressing blank lines and ellipses lines.

Instead of opening a web browser, the selected URL can be passed as the argument
to a command using `--run-safe "<command> {}"` or `--run "<command> {}"`. Note
the use of `{}` in the command string to denote the selected URL. Alternatively,
the URL can be piped to the command using `--run-safe <command> --pipe` (or
`--run`). Using --run-safe with --pipe is preferred if the command supports it,
as it is marginally more secure and tolerant of special characters in the URL.

## Theming

Run `urlscan -g` to generate ~/.config/urlscan/config.json with the default
color and black & white palettes. This can be edited or added to, as desired.
The first palette in the list will be the default. Configure the palettes
according to the [Urwid display attributes][1].

Partial example from default palette:
```json
        "default": [
            [
                "header",   # Urwid widget name
                "white",    # Standard foreground color
                "dark blue",# Standard background color
                "standout", # Monochrome settings
                "#ffffff",  # Extended foreground color (88 through True colors)
                "#0000aa"   # Extended foreground color (88 through True colors)
            ],
            [
                "footer",
                ...
```

Display width can be set with `--width`.

## Keybindings

Run `urlscan -g` to generate ~/.config/urlscan/config.json. All of the keys will
be listed. You can either leave in place or delete any that will not be altered.

To unset a binding, set it equal to "".  For example: `"P": ""`

The follow actions are supported:

- `add_url` -- add a URL to the queue (default: `a`)
- `all_escape` -- toggle unescape all URLs (default: `u`)
- `all_shorten` -- toggle shorten all URLs (default: `S`)
- `bottom` -- move cursor to last item (default: `G`)
- `clear_screen` -- redraw screen (default: `Ctrl-l`)
- `clipboard` -- copy highlighted URL to clipboard using xsel/xclip (default: `C`)
- `clipboard_pri` -- copy highlighted URL to primary selection using xsel/xclip (default: `P`)
- `context` -- show/hide context (default: `c`)
- `del_url` -- delete URL from the queue (default: `d`)
- `down` -- cursor down (default: `j`)
- `help_menu` -- show/hide help menu (default: `F1`)
- `link_handler` -- cycle link handling (webbrowser, xdg-open, --run-safe or --run) (default: `l`)
- `next` -- jump to next URL (default: `J`)
- `open_queue` -- open all URLs in queue (default: `o`)
- `open_queue_win` -- open all URLs in queue in new window (default: `O`)
- `open_url` -- open selected URL (default: `space` or `enter`)
- `palette` -- cycle through palettes (default: `p`)
- `previous` -- jump to previous URL (default: `K`)
- `quit` -- quit (default: `q` or `Q`)
- `reverse` -- reverse display order (default: `R`)
- `shorten` -- toggle shorten highlighted URL (default: `s`)
- `top` -- move to first list item (default: `g`)
- `up` -- cursor up (default: `k`)

## Known bugs and limitations

- Running urlscan sometimes "messes up" the terminal background. This seems to
  be an urwid bug, but I haven't tracked down just what's going on.

- Extraction of context from HTML messages leaves something to be desired.
  Probably the ideal solution would be to extract context on a word basis rather
  than on a paragraph basis.

- The HTML message handling is a bit kludgy in general.

- multipart/alternative sections are handled by descending into all the
  sub-parts, rather than just picking one, which may lead to URLs and context
  appearing twice. (Bypass this by selecting the '--dedupe' option)

## Build/development

- pyproject.toml is configured for [hatch][2] for building and submitting to pypi.
- flake.nix is available for a development shell or building/testing the package
  if desired. `nix develop`
- To update TLD list: `wget https://data.iana.org/TLD/tlds-alpha-by-domain.txt`
- GitHub Action will upload to TestPyPi on each push to `main`. To create a
  GitHub and PyPi release, create a new tag (formatting below) and push tags.

        <tag name on first line>
        
        * Release note 1
        * Release note 2
        * ...

[1]: http://urwid.org/manual/displayattributes.html#display-attributes  "Urwid display attributes"
[2]: https://hatch.pypa.io/latest/  "Hatch"
