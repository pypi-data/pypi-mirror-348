## --- This document is not finished ---

# ikctl (install kit control)

You can use this app to install packages on remote servers (linux).

## Description

This app use ssh protocol to connect on remote servers and running bash script to install packages.

## Getting Started

### Dependencies

* Python 3.12
* paramiko
* pyaml
* envyaml

### Installing

To install ikctl you only need pip command 
```
pip install ikctl
```

When the installation finished you will need to create folder with yours bash scripts and config files:


Create folder
```
mkdir ~/kits
```

Create config file where you add yours servers
```
cat <<EOF | tee ~/kits/config.yaml
servers:
  - name: your-server-name
    user: your-user
    hosts: [10.0.0.67]
    port: 22
    password: $PASSWORD/<your password>
    pkey: "/home/your-home-name/.ssh/id_rsa"
EOF
```

You will need to add a variable called password with the server access password:
```
export PASSWORD="your password"
```

Create ikctl config file where we will indicate our kits.
```
cat <<EOF | tee ~/kits/ikctl.yaml
kits:
  - show-date/ikctl.yaml
EOF
```

Create folder with our kit
```
mkdir ~/kits/show-date
```

In this folder we go to add the follow structure
```
cat <<EOF | tee ~/kits/show-date/date.sh
#!/bin/bash
date
EOF

# And

cat <<EOF | tee ~/kits/show-date/ikclt.yaml
kits:
  uploads:
    - date.sh
  pipeline:
    - date.sh
EOF
```

To finish config we need to add path to config file in "~/.ikctl/config"
```

# editing file config

vim ~/.ikctl/config

context: local
contexts:
  local:
    path_kits: 'path-to-kits/kits'
    path_secrets: '' <= doesn't work, yet
    path_servers: 'path-to-kits/kits'
    mode: 'local'
  remote:
    path_kits: ''
    path_secrets: ''
    path_servers: ''
    mode: 'remote'
```

### Executing program
* Get servers
```
ikctl -l servers
```

* Get kits
```
ikctl -l kits
```

* Run ikctl to execute bash script
```
ikctl -i show-date -n your-server-name
```

## License

This project is licensed under the Apache License License - see the LICENSE.md file for details