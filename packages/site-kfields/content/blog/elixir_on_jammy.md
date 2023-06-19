---
title: "Elixir on Jammy"
date: 2023-06-18 21:23:00
description: Install Elixir on Ubuntu 22.04
cover: "https://i.imgur.com/Uv6nv7k.jpg"
slug: "elixir-jammy"
category: ""
---

https://elixir-lang.org/install.html#gnulinux

WARNING: It appears that a required development package 'automake' is not installed

https://github.com/asdf-vm/asdf-erlang#before-asdf-install

```bash
sudo apt install -y unzip build-essential autoconf m4 libncurses5-dev
```

asdf install erlang 25.0.4
asdf global erlang 25.0.4

asdf install elixir 1.14.0-otp-25
asdf global elixir 1.14.0-otp-25

elixir -v

mix local.hex

mix archive.install hex phx_new

apt-get install inotify-tools