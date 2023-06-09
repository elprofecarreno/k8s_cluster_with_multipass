from command import oscmd
from datetime import datetime
import time
from command import cfglog

LOG = cfglog.log()

EXEC_MESSAGE = 'EXECUTE CMD IN %s %s'

# COMMAND DEFINITION
install_multipass = 'snap install multipass -y'
multipass_cmd = 'multipass'
launch = 'launch --name {vm_name} -m {memory} -c {cpus} -d {disk} {os}'
exec_cmd = 'exec {vm_name} -- bash -c "{command}"'
exec_user_cmd = 'exec {vm_name} -- bash -c \'sudo su {user_os} -c "{command}"\''
exec_sudo_cmd = 'exec {vm_name} -- sudo bash -c \'sudo su {user_os} -c "{command}"\''
apt_update = 'sudo apt-get update'
docker_install = 'sudo apt-get install docker.io -y'
docker_start = 'sudo systemctl start docker'
docker_enabled = 'sudo systemctl enable docker'
docker_group = 'sudo usermod -aG docker {user_os}'
docker_version = 'docker --version'
k8s_key_repository = 'https://packages.cloud.google.com/apt/doc/apt-key.gpg'
k8s_repository = 'http://apt.kubernetes.io/ kubernetes-xenial'
add_key_repository = 'curl -s {url} | sudo apt-key add'
add_repository = 'sudo apt-add-repository \'deb {k8s_repository} main\' -y'
k8s_install = 'sudo apt-get install kubeadm kubelet kubectl -y'
k8s_version = 'kubectl version'
k8s_kubeadm_pull = 'sudo kubeadm config images pull'
ip_vm = 'list | grep {vm_name} | awk {{\'print $3\'}}'
ips_vms = 'list | awk \'$1 ~ /^[a-zA-Z]/ {{print $1, $3}}\' | tail -n +2'
master_config = ''
add_hosts = 'sudo echo \'{ips}\' >> /etc/hosts'
ping_c4 = 'ping {host} -c 4'
swap = 'swapoff -a'
k8s_impl = 'sudo kubeadm init --pod-network-cidr={ip_master}/16'
k8s_cluster_join = 'sudo kubeadm token create --print-join-command'
regular_user_k8s_mkdir = 'mkdir -p $HOME/.kube'
regular_user_k8s_cp = 'sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config'
regular_user_k8s_chown = 'sudo chown {user_os}:{user_os} $HOME/.kube/config'
k8s_get_nodes = 'kubectl get nodes'
k8s_red_node = 'kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml'

# INSTALL MULTIPASS WITH SNAP
def install_multipass_snap():
    # COMMAND LIST VM MULTIPASS
    output = oscmd.exec_command([install_multipass])
    output = output.strip()    
    LOG.info('install multipass with snap %s', output)

# VERIFIED EXIST VM MULTIPASS
def is_exists_vm(vm_name):
    # COMMAND LIST VM MULTIPASS
    output = oscmd.exec_command([multipass_cmd + ' list | grep ' + vm_name])
    output = output.strip()
    # RETURN TRUE IS EXISTS, FALSE IS NOT EXISTS
    return output != ''

# STOP AND DELETE VM MULTIPASS
def stop_and_delete_vm(vm_name):
    # COMMAND STOP AND DELETE MULTIPASS VM
    LOG.info('stop %s', vm_name)
    oscmd.exec_command([multipass_cmd + ' stop ' + vm_name + ' && ' + multipass_cmd + ' delete --purge ' + vm_name])
    LOG.info('deleted %s', vm_name)

# STOP AND DELETE VM MULTIPAS IS EXISTS
def exists_stop_and_delete_vm(vm_name):
    # EXIST vm_name VM
    is_vm = is_exists_vm(vm_name)
    LOG.info('is_vm %s : %s', vm_name, is_vm)
    if is_vm:
        #DELETE vm_name VM
        stop_and_delete_vm(vm_name)

# DELETE AND CREATE VM MULTIPASS
def launch_vm(**kwargs):
    str_date = datetime.now().strftime("%d%m%Y_%H%M%S")
    vm_name = f'vm-default{str_date}'    
    memory = '2G'
    cpus = '2'
    disk = '5G'
    os = 'bionic'

    for key, value in kwargs.items():
        if key == 'vm_name' :
            vm_name = value
        if key == 'memory':
            memory = value
        if key == 'cpus':
            cpus = value
        if key == 'disk':
            disk = value        
        if key == 'os':
            os = value

    exists_stop_and_delete_vm(vm_name)
    LOG.info(multipass_cmd + ' ' + 
                launch.format(vm_name=vm_name, memory=memory, cpus=cpus, disk=disk, os=os))    
    output = oscmd.exec_command([multipass_cmd + ' ' + 
                launch.format(vm_name=vm_name, memory=memory, cpus=cpus, disk=disk, os=os)])
        
    if(output.strip() == '' or "configuring" in output.strip().lower()):
        print_correction(output)
    else:
        LOG.error('error: %s', output.strip())
    time.sleep(1)

# PRINT CORRECTION
def print_correction(output):
        lines = output.split('\n')
        for line in lines:
            if(line.strip() != ''):
                LOG.info(line.strip().lower())

# EXECUTE COMMAND
def exec_command(vm_name, command):
    LOG.info(EXEC_MESSAGE, vm_name, command)    
    output = oscmd.exec_command([multipass_cmd + ' ' + 
                exec_cmd.format(vm_name=vm_name, command=command)])
    print_correction(output)
    return output

# EXECUTE COMMAND
def exec_command_user(vm_name, command, user_os):
    LOG.info(EXEC_MESSAGE, vm_name, command)
    output = oscmd.exec_command([multipass_cmd + ' ' + 
                exec_user_cmd.format(vm_name=vm_name, command=command, user_os=user_os)])
    print_correction(output)
    return output

# EXECUTE COMMAND
def exec_sudo_command(vm_name, command):
    LOG.info(EXEC_MESSAGE, vm_name, command)
    output = oscmd.exec_command([multipass_cmd + ' ' + 
                exec_cmd.format(vm_name=vm_name, command=command)])
    print_correction(output)
    return output
 
# UPDATE APT
def apt_update_command(vm_name):
    return exec_command(vm_name, apt_update)

# DOCKER INSTALL
def docker_install_command(vm_name):
    return exec_command(vm_name, docker_install)

# DOCKER INSTALL
def docker_start_command(vm_name):
    return exec_command(vm_name, docker_start)

# DOCKER INSTALL
def docker_enabled_command(vm_name):
    return exec_command(vm_name, docker_enabled)

# DOCKER DEFINED GROUP
def docker_group_command(vm_name, user_os):
    return exec_command(vm_name, docker_group.format(user_os=user_os))

# DOCKER VERSION
def docker_version_command(vm_name, user_os):
    return exec_command_user(vm_name, docker_version, user_os)    

# DOCKER
def docker_command(vm_name, user_os):
    apt_update_command(vm_name)
    docker_install_command(vm_name)
    docker_start_command(vm_name)
    docker_enabled_command(vm_name)
    docker_group_command(vm_name, user_os)
    docker_version_command(vm_name, user_os)

# ADD k8s KEY
def add_k8s_key_commad(vm_name):
    return exec_command(vm_name, add_key_repository.format(url=k8s_key_repository))

# ADD k8s REPOSITORY
def add_k8s_repository_commad(vm_name):
    return exec_command(vm_name, add_repository.format(k8s_repository=k8s_repository))

# INSTALL k8s REPOSITORY
def k8s_install_commad(vm_name):
    return exec_command(vm_name, k8s_install.format(url=k8s_key_repository))

# k8s VERSION
def k8s_version_command(vm_name, user_os):
    return exec_command_user(vm_name, k8s_version, user_os)

# k8s VERSION
def k8s_kubeadm_pull_command(vm_name):
    return exec_command(vm_name, k8s_kubeadm_pull)

# k8s
def k8s_command(vm_name, user_os):
    add_k8s_key_commad(vm_name)
    add_k8s_repository_commad(vm_name)
    apt_update_command(vm_name)
    k8s_install_commad(vm_name)
    k8s_version_command(vm_name, user_os)   

# MULTIPASS IP VM
def ip_vm_command(vm_name):
    cmd = multipass_cmd + ' ' + ip_vm.format(vm_name=vm_name)
    LOG.info('EXECUTE FIND IP %s %s', vm_name, cmd)
    output = oscmd.exec_command([cmd])
    output = output.strip().replace('\n', '')
    LOG.info(output)
    return output

# LIST IPS VIRTUAL MACHINES
def ips_vms_command():
    cmd = multipass_cmd + ' ' + ips_vms
    LOG.info('EXECUTE FIND IP %s' , cmd)
    output = oscmd.exec_command([cmd])
    output = output.strip()
    print_correction(output)
    return output

# ADD HOSTS IN /etc/hosts
def add_hosts_command(vm_name, ips_vms):
    exec_sudo_command(vm_name, add_hosts.format(ips=ips_vms))

# VERIFIED HOSTS CONFIGURATION
def verification_hosts_command(vm_name, hosts):
    for host in hosts:
        exec_command(vm_name, ping_c4.format(host=host))

# DISBLAED SWAP
def swap_command(vm_name):
    exec_sudo_command(vm_name, swap)

# k8s IMPLEMENTATION
def k8s_impl_command(vm_name, ip_master):
    exec_command(vm_name, k8s_impl.format(ip_master=ip_master)) 

# JOIN NODE IN CLUSTER
def k8s_join_command(vm_name):
    return exec_command(vm_name, k8s_cluster_join) 

# REGULARIZATION k8s MASTER     
def regular_k8s_command(vm_name, user_os):
    exec_command_user(vm_name, regular_user_k8s_mkdir, user_os)
    exec_command_user(vm_name, regular_user_k8s_cp, user_os)
    exec_command_user(vm_name, regular_user_k8s_chown.format(user_os=user_os), user_os)   

# k8s GET NODES
def k8s_get_nodes_command(vm_name, user_os):
    exec_command_user(vm_name, k8s_get_nodes, user_os)

# k8s CREATE RED NODE
def k8s_red_node_command(vm_name, user_os):
    exec_command_user(vm_name, k8s_red_node, user_os)
    