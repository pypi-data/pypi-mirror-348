# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> GRPC Calls for Python

This module is a part of the [Pip.Services](http://pipservices.org) polyglot microservices toolkit.

The grpc module is used to organize synchronous data exchange using calls through the gRPC protocol. It has implementations of both the server and client parts.

- Note: in this version connection Proto files in runtime does not supports


The module contains the following packages:

- **Build** - factories for creating gRPC services
- **Clients** - basic client components that use the gRPC protocol and Commandable pattern through gRPC
- **Services** - basic service implementations for connecting via the gRPC protocol and using the Commandable pattern via gRPC

<a name="links"></a> Quick links:

* [Configuration](http://docs.pipservices.org/v4/tutorials/beginner_tutorials/configuration/)
* [Protocol buffer](https://github.com/pip-services4-node/pip-services4-grpc-node/blob/master/src/protos/commandable.proto)
* [API Reference](https://pip-services4-python.github.io/pip-services4-grpc-python/index.html)
* [Change Log](CHANGELOG.md)
* [Get Help](http://docs.pipservices.org/v4/get_help/)
* [Contribute](http://docs.pipservices.org/v4/contribute/)


## Use

Install the Python package as
```bash
pip install pip_services4_grpc
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate GRPC protobuf stubs:
```bash
./protogen.ps1
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The Python version of Pip.Services is created and maintained by 
- **Sergey Seroukhov**
- **Danil Prisiazhnyi**
