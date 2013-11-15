# Sublime Scalariver

Format Scala code using [Scalariver](https://github.com/ornicar/scalariver),
a web server using [Scalariform](https://github.com/mdr/scalariform).

## Getting started

1. [Install Scalariver](#install)
2. Select code to format (or select nothing if you want to format the whole file)
3. Format the code :p Choose your way
  - `cmd+shit+c` (on Mac, I didn't figure what mapping would word without being a pain in other system)
  - “scalariver: Format” in command palette
  - Tools > Scalariver > Format

## How it works

The (selected) code is sent to [Scalariver](https://github.com/ornicar/scalariver) with formatting option,
so you might consider to run a personal Scalariver instance on your computer (or in an intranet server).

## Commands

- “Format”: formats selection (and whole file is there is no selection),
- “Format file”: format the whole file whatever there is selection or not.

## Install

### Using Package Control

Install the “Scalariver” package. (hem… when it'll be ready)

### À la pogne

Fetch the sources on [GitHub](https://github.com/dohzya/sublime_scalariver).

## Settings

- `scalariver_url`: The URL of Scalariver instance
- `scalariver_formatonsave`: Format file on each save (`true` by default)
- `scalariver_options`: The Scalariver options (containing Scalariform ones)

### Defining personal key binding

If you want to use your own mapping, add “`{ "keys": ["ctrl+shift+c"], "command": "scalariver"}`”
in your Key Bindings file.

## Credits

Thanks to
- [Scalariver](https://github.com/ornicar/scalariver) ☺
- [Scalariform](https://github.com/mdr/scalariform)
