# README.md

# PubStomp

**PubStomp** is an advanced asynchronous pentesting toolkit designed for efficient reconnaissance, vulnerability fuzzing, and reporting against web applications.

## Features
-  Async web crawling and spidering
-  Custom wordlists for fuzzing endpoints
-  Optional XSS payload testing
- 離 Report generation to JSON
-  Colored terminal output with progress bars
-  Configurable output and log file paths

## Installation
Install via pip from source:

```bash
pip install .
```

Or once published:
```bash
pip install pubstomp
```

> ⚠️ If the `pubstomp` command is not found after install, it's likely because `~/.local/bin` is not in your `$PATH`.
> 
> You can fix this by adding the following line to your shell config (e.g., `~/.bashrc`, `~/.zshrc`):
>
> ```bash
> export PATH="$HOME/.local/bin:$PATH"
> ```
>
> Then reload it with:
>
> ```bash
> source ~/.bashrc  # or source ~/.zshrc
> ```
>
> Alternatively, you can create a system-wide symlink:
>
> ```bash
> sudo ln -s ~/.local/bin/pubstomp /usr/local/bin/pubstomp
> ```

## Usage
Set your output and log paths:

```bash
pubstomp --setoutput ~/targets
pubstomp --setlog ~/logs/pubstomp.log
```

Run a scan:
```bash
pubstomp example.com --depth 2 --xss --report
```

Check saved paths:
```bash
pubstomp --showoutput
pubstomp --showlog
```

## CLI Options
```bash
pubstomp -h
```
Prints all command-line options.

## License
This project is licensed under the MIT License.
