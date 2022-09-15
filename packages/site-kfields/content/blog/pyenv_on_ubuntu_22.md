---
title: "Install Pyenv on Ubuntu 22.04"
date: 2022-08-21 07:42:34
description: Install Pyenv on Ubuntu 22.04 the Right Way
cover: "https://i.imgur.com/Uv6nv7k.jpg"
slug: "pyenv-ubuntu-22"
category: ""
---

## Get the Required Dependencies

```bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

## Install Pyenv

[https://github.com/pyenv/pyenv-installer](https://github.com/pyenv/pyenv-installer)

```bash
curl https://pyenv.run | bash
```

Make sure this is in your `.bashrc`

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

```bash
pyenv install 3.10.6
```