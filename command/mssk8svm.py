from command import msscmd as mu
from tqdm import tqdm
from command import cfglog

LOG = cfglog.log()

master_k8s_name='master-k8s'
workers_k8s_name='worker-{worker_id}-k8s'
workers=2
user_os= 'ubuntu'
hosts = []
nodes = []

def case_exec(index):
    match index:
        case 1:
            # INSTALL MULTIPASS
            LOG.info('VERIFIED INSTALL MULTIPASS...')            
            #mu.install_multipass_snap()
        case 2:
            LOG.info('CREATE CLUSER KUBERNETES...')
            LOG.info('CREATE VM WITH MULTIPASS...')
            # MASTER
            LOG.info('CREATE VM WITH MULTIPASS... %s', master_k8s_name)
            mu.launch_vm(vm_name=master_k8s_name)
            hosts.append(master_k8s_name)
        case 3:
            # WORKERS
            for i in range(0, workers):
                worker_name = workers_k8s_name.format(worker_id=i+1)
                LOG.info('CREATE VM WITH MULTIPASS... %s', worker_name)
                nodes.append(worker_name)
                hosts.append(worker_name)
                mu.launch_vm(vm_name=worker_name)
            LOG.info('hosts: %s', hosts)
            LOG.info('nodes: %s', nodes)
        case 4:
            # INSTALL DOCKER + KUBERNETES (MASTER NODE)
            LOG.info('INSTALL DOCKER + KUBERNETES VM WITH MULTIPASS (MASTER NODE)... %s', master_k8s_name)
            mu.docker_command(master_k8s_name, user_os)
            mu.k8s_command(master_k8s_name, user_os)
            mu.docker_version_command(master_k8s_name, user_os)
        case 5:
            # INSTALL DOCKER + KUBERNETES
            LOG.info('INSTALL DOCKER + KUBERNETES VM WITH MULTIPASS (SLAVE NODES)...')
            for i in range(0, workers ):
                worker_name = workers_k8s_name.format(worker_id=i+1)
                LOG.info('(SLAVE NODES)... %s', worker_name)
                mu.docker_command(worker_name, user_os)
                mu.k8s_command(worker_name, user_os)
        case 6:
            # CLUSTER CONFIG
            LOG.info('CLUSTER CONFIG WITH MULTIPASS... %s', master_k8s_name)
            mu.k8s_kubeadm_pull_command(master_k8s_name)
            ips_vms = mu.ips_vms_command()
            LOG.info('ips_vms: %s', ips_vms)
            # ADD AND VERIFICATION HOSTS VM
            LOG.info('hosts: %s', hosts)
            for host in hosts:
                LOG.info('CONFIG HOSTS WITH MULTIPASS... %s', host)
                mu.add_hosts_command(host, ips_vms);
                mu.verification_hosts_command(host, hosts)
                LOG.info('DISABLED SWAP WITH MULTIPASS... %s', host)
                mu.swap_command(host) 
        case 7:
            # NODES CONFIG
            LOG.info('NODES CONFIG...')
            ip_master = mu.ip_vm_command(master_k8s_name)
            LOG.info('ip_master: %s', ip_master)
            mu.k8s_impl_command(master_k8s_name, ip_master)
            join_cmd = 'sudo {0}'.format(mu.k8s_join_command(master_k8s_name)) 
            for node in nodes:
                LOG.info('JOIN NODE WITH MULTIPASS... %s', node)
                mu.exec_command_user(node, join_cmd, user_os)               

        case 8:
            # CLUSTER CORRECTION
            mu.regular_k8s_command(master_k8s_name, user_os)
            mu.k8s_red_node_command(master_k8s_name, user_os)
            mu.k8s_get_nodes_command(master_k8s_name, user_os)                                         
        case _:
            LOG.info('METHOD NOT SUPPORT')

def __main__():
    for i in tqdm(range(0, 8), ncols = 100, desc ="Create Clust k8s: master + {0} nodes".format(workers)):
        case_exec(i+1)