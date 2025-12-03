# whimdb

micro key-value in-memory database

### Description
lightweight in-memory, key-value databases server & client 

#### TCP packet structure
| Size    | Type    | Content |
|---------|---------|---------|
| 4 bytes | 2 bytes | x bytes |

max packet size up to 5MB

### Features
- client & async server
- `query`, `set`, `remove`, `purge`, `update_ttl` commands
- queries pagination
- database items ttl (time to live) + auto removal of expired ones
- support for multiple databases
- no external dependencies
- fully type hinted

### How to use it
package can be installed via `pip` just add following line to your
`requirements.txt`.

```
whimdb @ git+https://github.com/zNitche/whimdb.git@<version>
```

### CLI
server can by run via

```
whimdb-server --port 8080
```

### Examples
`Client` and `Server` example scripts can be found in `/examples` directory.

### Docker usage

##### Dockerfile.whimdb
```
FROM python:3.12-slim

RUN pip3 install git+https://github.com/zNitche/whimdb.git@v1.2.3
```

##### docker-compose.yml
```
services:
  whimdb:
    command: whimdb-server --port 6000
    container_name: whimdb
    restart: unless-stopped
    build:
      context: .
      dockerfile: Dockerfile.whimdb
```

### Tests
project's test suit can be run via

##### Install tests dependencies
```
pip3 install -r requirements/tests.txt
```

##### Run tests
```
pytest -v tests/
```
