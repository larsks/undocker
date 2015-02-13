## Repositories

The `repositories` file at the top level of a Docker image archive
contains a list of images contained in the image and layer id of the
"topmost" layer:

    {
      "fedora": {
        "21": "834629358fe214f210b0ed606fba2c17827d7a46dd74bd3309afc2a103ad0e89",
        "20": "6cece30db4f924da43969a12fdf47492ada22b372a0968d6ca8b71d25876629f"
      }
    }

## Layers

Each layer contained in the archive contains a file named `json` with
the following format:

    {
      "Size": 0,
      "os": "linux",
      "architecture": "amd64",
      "id": "4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125",
      "parent": "ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2",
      "created": "2014-12-31T22:23:56.943403668Z",
      "container": "83dcf36ad1042b90f4ea8b2ebb60e61b2f1a451a883e04b388be299ad382b259",
      "container_config": {
        "OnBuild": [],
        "MacAddress": "",
        "NetworkDisabled": false,
        "Entrypoint": null,
        "WorkingDir": "",
        "Volumes": null,
        "Image": "ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2",
        "Cmd": [
          "/bin/sh",
          "-c",
          "#(nop) CMD [/bin/sh]"
        ],
        "AttachStdin": false,
        "Cpuset": "",
        "CpuShares": 0,
        "MemorySwap": 0,
        "Memory": 0,
        "User": "",
        "Domainname": "",
        "Hostname": "7f674915980d",
        "AttachStdout": false,
        "AttachStderr": false,
        "PortSpecs": null,
        "ExposedPorts": null,
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": [
          "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ]
      },
      "docker_version": "1.4.1",
      "author": "Jérôme Petazzoni <jerome@docker.com>",
      "config": {
        "OnBuild": [],
        "MacAddress": "",
        "NetworkDisabled": false,
        "Entrypoint": null,
        "WorkingDir": "",
        "Volumes": null,
        "Image": "ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2",
        "Cmd": [
          "/bin/sh"
        ],
        "AttachStdin": false,
        "Cpuset": "",
        "CpuShares": 0,
        "MemorySwap": 0,
        "Memory": 0,
        "User": "",
        "Domainname": "",
        "Hostname": "7f674915980d",
        "AttachStdout": false,
        "AttachStderr": false,
        "PortSpecs": null,
        "ExposedPorts": null,
        "Tty": false,
        "OpenStdin": false,
        "StdinOnce": false,
        "Env": [
          "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ]
      }
    }

