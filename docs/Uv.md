# Uv

Other languages:

- English
- [français](Uv_fr.md)

Not supported

uv is currently **not** supported on our clusters.

uv is an extremely fast Python package and project manager written in Rust. While you may be able to use it to install some packages, it will likely fail for others.

Some issues and pitfalls you may encounter:

- some packages are distributed in a format that is incompatible with our clusters, but uv tries to install them nonetheless;
- uv is unaware of the Python packages provided by loaded modules;
- uv can quickly fill up your /home directory quota since it stores a very large number of files in its cache.

# Installing Python packages

To install packages on our clusters, use `pip`; see [Python](Python.md).

Make sure to use at least `pip>=25.0`.

```
(ENV) [name@server ~] pip install --no-index --upgrade pip

```

# Troubleshooting

## Clearing the cache

To clear the uv cache, use

```
[name@server ~]$ uv cache clean

```

Then, to avoid using the cache, use `uv --no-cache`.