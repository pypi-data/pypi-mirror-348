# Highlight CLI
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/) - [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined
)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

Highlight strings within streams of text.

## Motivation
It can be useful to highlight text in output to make it easier to find. There are tools that can do this like [`grep`](https://stackoverflow.com/questions/981601/colorized-grep-viewing-the-entire-file-with-highlighted-matches) and `supercat` but these aren't trivial to use. I wanted a tool that is trivial to use and install on machines.

## Alternatives and prior work
It is surprising that there aren't tool that do this. Some tools come close:

* [xpo](https://github.com/ghoseb/xpo) provides similar functionality but [I could not install it](https://github.com/ghoseb/xpo/issues/1)
* [hhighligher](https://github.com/paoloantinori/hhighlighter?tab=readme-ov-file) does this - but it is written in shell and I did not find it easyer to install.
* `grep` supports highlighting. The settings for coloring is complete but difficult to understand and additional regular expressions need to be added to match all lines.

## Installation
You can install hlcli using [pipx](https://github.com/pypa/pipx):

```
pipx install hlcli
```

## Usage
Highlight the sring one
```
echo "hello one three\ntwo\nthree\nfour\nfive\nsix" | hlcli 'one'
```

Match various expressions with different colors:
```
echo "hello one three\ntwo\nthree\nfour\nfive\nsix" | hlcli one --green two --yellow three four --red six
```
Here we highlight `one` in red (the default color), `two` in green, `three` and `four` in yellow and `six` in red

## About me
I am **@readwithai**. I create tools for reading, research and agency sometimes using the markdown editor [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

I also create a [stream of tools](https://readwithai.substack.com/p/my-productivity-tools) that are related to carrying out my work.

I write about lots of things - including tools like this - on [X](https://x.com/readwithai).
My [blog](https://readwithai.substack.com/) is more about reading and research and agency.

[![@readwithai logo](./logo.png)](https://readwithai.substack.com/)
