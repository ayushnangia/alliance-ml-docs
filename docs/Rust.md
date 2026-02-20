# Rust

Other languages:

- English
- [français](Rust_fr.md)

[Rust](https://www.rust-lang.org/) is a multi-paradigm, high-level, general-purpose programming language. Rust emphasizes performance, type safety, and concurrency. Rust enforces memory safety — that is, that all references point to valid memory — without requiring the use of a garbage collector or reference counting present in other memory-safe languages.

## Module

The Rust compiler is available as a [module](Utiliser_des_modules.md).

```
[name@server ~]$ module spider rust

```

## Installing a crate

A package written in Rust is called a [*crate*](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html).

### From Crates.io

1. Load the required modules.

```
[name@server ~]$ module load rust

```

2. Build and install the crate locally. This must be done from a login node.

```
[name@server ~]$ cargo install ungoliant

```

3. Test the binary.

```
[name@server ~]$ $HOME/.cargo/bin/ungoliant -h

```

You can also add `.cargo/bin` to your `$PATH` with: `export PATH="$HOME/.cargo/bin:$PATH"`.

### From a Git repository

1. Load the required modules.

```
[name@server ~]$ module load rust

```

2. Build and install the crate locally. This must be done from a login node.

```
[name@server ~]$ cargo install --git https://github.com/username/repo-name

```

3. Test the binary.

```
[name@server ~]$ $HOME/.cargo/bin/<binname> -h

```

You can also add `.cargo/bin` to your `$PATH` with: `export PATH="$HOME/.cargo/bin:$PATH"`.

## Using the Rust nightly compiler

Since some optimization features are not yet stable they are not part of the stable release, but nonetheless some crates make use of them.
If you require the Rust nightly compiler, you can install it locally.

1. Install the compiler as a local module.

```
[name@server ~]$ eb Rust-1.53.0.eb --try-software-version=nightly --disable-enforce-checksums

```

2. Load the local module.

```
[name@server ~]$ module load rust/nightly

```

## Clean up cache

Cargo cache and registry can eat up a lot of space. You can reclaim space by removing the registry:

```
[name@server ~]$ rm -r ~/.cargo/registry

```