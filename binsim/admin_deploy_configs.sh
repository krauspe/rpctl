#!/usr/bin/ksh
#
# (c) Peter Krauspe 10/2015
# Simulation 
#
# funzt

# <2step>
. /etc/2step/2step.vars
#
dbg=echo
dbg=""
dev=eth0
# ggfs spaeter aus config file
basedir=/opt/dfs/rpctl  # simualation basdir
bindir=${basedir}/bin
confdir=${basedir}/config
vardir=${basedir}/var
remote_nsc_list_file=${vardir}/remote_nsc.list

source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers, simulation_mode

simulated_remote_nsc_count=6

arg1=$1

function check_host_alive
{
    echo 1
}

function create_remote_nsc_configs # create files on remote NSSes
{
  echo "fake: create_remote_nsc_configs :"
}

function get_remote_nsc_list  # returns the list. 
{
  #echo "simulate: get_remote_nsc_list :"
  typeset remote_nsc_list=""
  typeset -i n
  typeset remote_domain_server=$1
  typeset remote_dn=${remote_domain_server#*.}
  for i in $(seq 1 $simulated_remote_nsc_count)
  do
    n=$((100+i))
    remote_nsc_list="$remote_nsc_list psp${n}-s1.${remote_dn}"
  done
  echo $remote_nsc_list
}


function copy_remote_nsc_config # copys files
{
  echo "fake: copy_remote_nsc_config :"
}

echo "\n<< Create nsc list from all ResourceDomainServers >>\n"

${bindir}/admin_get_resource_nsc_list.sh --no-target-config-list

echo "\n<< Collect nsc configs from all RemoteDomainServers >>\n"

# get uniq list of ALL servers

AlleDomainServers=$(echo $ResourceDomainServers $RemoteDomainServers | sed 's/\s/\n/g' | sort -u)

echo "\n<< Fake: Deploy scripts and configs to all ResourceDomainServers and RemoteDomainServers >>\n"

for domain_server in $AlleDomainServers 
do
  if [[ $domain_server != $(dnsdomainname) ]]; then
    echo "  Deploy all scripts and configs to $domain_server"
  fi
done

[[ -f $remote_nsc_list_file ]] && rm $remote_nsc_list_file

for remote_domain_server in $RemoteDomainServers
do
   if [[ $(check_host_alive ${remote_domain_server}) == 0 ]]; then
     echo "$remote_domain_server NOT REACHED, skipping !!"
     continue
   fi
   remote_dn=${remote_domain_server#*.}

   [[ -d ${vardir}/$remote_dn ]] || mkdir -p ${vardir}/$remote_dn

   echo "  create remote nsc configs on $remote_domain_server"
   create_remote_nsc_configs $remote_domain_server
   echo "HIER !!"
   for remote_nsc in $(get_remote_nsc_list $remote_domain_server)
   do
     echo "  copy $remote_nsc config from $remote_domain_server"
     copy_remote_nsc_config $remote_domain_server $remote_nsc
     echo $remote_nsc >> $remote_nsc_list_file
   done
   
   echo "Fake  copy public key"


done

echo "\n<< Deploy all configs to all ResourceDomainServers and RemoteDomainServers >>\n"

for domain_server in $AlleDomainServers
do
  if [[ $domain_server != $(dnsdomainname) ]]; then
    echo "Fake: Deploy all configs to $domain_server"
  fi
done

echo "\n<< Fake: Deploy all configs to all Resource NSC's >>\n"

for resource_domain_server in $ResourceDomainServers
do
    # sync all configd to nsc's
    echo "  syncing $resource_domain_server clients"
    echo "    syncing tsctl2 stuff"

    if [[ $arg1 == *xinitrc*  || $arg1 == "all" ]] ; then
      echo "   Fake: syncing xinitrc"
    fi
    if [[ $arg1 == *wall_msg*  || $arg1 == "all" ]]; then
      echo "   Fake: syncing wall_msg script"
    fi

    if [[ $arg1 == *java*  || $arg1 == "all" ]] ; then
      echo "   Fake: syncing java ..."
    fi
done

echo "\nDone.\n"
