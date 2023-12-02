# commands

### celery
    celery -A projectname worker -l info -P eventlet

### rabbitmq
    docker run -it --rm -name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

### install make using chocklety in windows powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

## install make
    choco install make
    