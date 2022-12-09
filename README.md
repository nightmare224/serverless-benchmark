# Configuration File

All configurations are defined in `./inventory` file.  The configuration file gives Ansible all the information of target nodes, including:
- Host IP
- Hostname
- Host username
- Docker username
- Docker password
- Application name
- Pod number

Without those information, Ansible cannot connect to those target nodes.



# Usage
After done all configuration, run the `deploy.sh` file.
```bash
bash deploy.sh
```

