# Kisesi
Kisesi is a light wrapper around the built-in `logging` module of Python
standard library. This module is written in a hacky way and thus is meant for
personal use.

# Demos
```python
import kisesi


def main() -> None:
    kisesi.basic_config(level=kisesi.DEBUG, incdate=True)

    log = kisesi.get_logger(__name__)
    log.debug("This is a \"debug\" message.")
    log.info("This is a \"info\" message.")
    log.warning("This is a \"warning\" message.")
    log.error("This is a \"error\" message.")
    log.critical("This is a \"critical\" message.")


if __name__ == "__main__":
    main()
```

## Preview
### Maple Font
![Demo Image](https://files.catbox.moe/wmmvsx.png)

### Normal
![Demo Image](https://files.catbox.moe/o9vvpw.png)

# Guide
You are expected to read the [source
code](https://github.com/eeriemyxi/kisesi/blob/main/src/kisesi/__init__.py) to
figure out all the features.

# Installation
Pypi
```shell
user:~$ pip install kisesi
```
Git
```shell
user:~$ pip install git+https://github.com/eeriemyxi/kisesi
```
