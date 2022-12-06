# Configuration File

All configurations are defined in `./inventory` file.  The configuration file gives Ansible all the information of target nodes, including:
- Host IP
- Hostname
- Host username
- Docker username
- Docker password.

Without those information, Ansible cannot connect to those target nodes.



# Usage
You can use `./taglist` to check the task you want to run. 
For example, this means to run do `initial setup` (docker login, openfaas login, etc.) and then deploy `floating-point-operation-sine` function.
```
[v] env-init
[v] floating-point-operation-sine
[x] dd-cmd
[x] matrix-multiplication-low
[x] fast-fourier-transform
```
After done all configuration, run the `deploy.sh` file.
```bash
bash deploy.sh
```

