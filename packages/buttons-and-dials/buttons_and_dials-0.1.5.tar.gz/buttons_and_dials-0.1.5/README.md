# buttons_and_dials

Customizable configs for your packages.

## Use case

You have your `potato` software that somewhere within it's contents contains
a file `default-potato.toml` describing some settings.

Let say you want to enable your users to customize those settings:
- by providing a file `potato-settings.toml` in the CWD.
- by providing a toml file pointed by environment variable POTATO_FILE=some/path
- by passing command line arguments to some script

Then you should use `buttons_and_dials`.

## Snippet

In your code, simply define

```python
from buttons_and_dials import ConfigSet

configs = ConfigSet(
    set_name='potato-settings',
    initial_settings_path='internal/path/default-potato.toml'
    check_cwd=True,
    argv_prefix='--cfg'
)
```

And from now on, you can access attributes of `configs` object and enjoy.

