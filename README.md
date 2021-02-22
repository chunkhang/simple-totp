# simple-totp

> A simple TOTP CLI

Tired of fumbling around with Google Authenticator just to generate a simple
[TOTP](https://en.wikipedia.org/wiki/Time-based_One-Time_Password) token? Well,
`simple-totp` is the simplest TOTP CLI you will ever need. Just set it up once,
and you are ready to go. `simple-totp` offers nothing fancy beyond printing out
TOTP tokens on the terminal.

## Demonstration

![demonstration](https://i.postimg.cc/hGcCb8HC/demo-min.gif)

## Installation

It should be quite easy to install `simple-totp`, provided you have python >= 3.

```
pip install simple-totp
```

## Usage

Running `simple-totp` cannot be simpler.

```
otp
```

## Configuration

`simple-totp` reads from the configuration file in `~/.otp.yml` to
generate TOTP tokens. All secrets are stored there as plain text, so
just be mindful about it.

Here is the minimal configuration needed to verify that `simple-totp`
is working properly:

```yaml
totp:
  - secret: 7TO66UM5PZ2M5CB2GWZMYZX5YAVWATQX
```

To generate multiple TOTP tokens with proper namespacing:

```yaml
totp:
  - issuer: google
    name: test@example.com
    secret: 7TO66UM5PZ2M5CB2GWZMYZX5YAVWATQX
  - issuer: facebook
    name: test@example.com
    secret: HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ
```

By default, `otp` generates 6-digit TOTP tokens where the refresh
interval is every 30 seconds. If you need to override this
behavior, you may try the following:

```yaml
totp:
  - issuer: google
    name: test@example.com
    secret: 7TO66UM5PZ2M5CB2GWZMYZX5YAVWATQX
    digits: 10
    interval: 60
```


## Development

Before developing, make sure [just](https://github.com/casey/just) is
installed. This project uses `just` as the command runner instead of the
usual `make`.

Start a [virtualenv](https://pypi.org/project/virtualenv/) if needed. It is
highly recommended for development.

Install the dependencies for the project:

```
just setup
```

After that, install `simple-totp` in editable mode:

```
just install
```

Now, you can start developing. You can run the CLI directly:

```
otp
```

Distribution can be done with:

```
just publish
```
