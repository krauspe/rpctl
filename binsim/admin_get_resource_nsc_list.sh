#!/bin/ksh
#
# (c) Peter Krauspe 10/2015
#
# This script should run on admin machine
# creates a list of all resource NSC's (resource_nsc.list) from each resource domain including  MAC adresses
#
# Simulation
# funzt
#

# <2step>
#. /etc/2step/2step.vars
#
#dbg=echo
dbg=""
dev=eth0
# ggfs spaeter aus config file
basedir=/opt/dfs/rpctl
bindir=${basedir}/binsim
confdir=${basedir}/config
vardir=${basedir}/var
arg1=$1

source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers

resource_nsc_list_file=${vardir}/resource_nsc.list
target_config_list_file=${vardir}/target_config.list
remote_nsc_list_file=${vardir}/remote_nsc.list

typeset -i n
simulated_resource_nsc_count=10

[[ -f $resource_nsc_list_file ]] && rm $resource_nsc_list_file

# create faked mac addresses

for i in $(seq -w 1 $simulated_resource_nsc_count)
do
  MAC[$i]="ab:cd:01:c2:d3:$i"
done

for resource_domain_server in $ResourceDomainServers
do
   resource_dn=${resource_domain_server#*.}
   [[ -d ${vardir}/$resource_dn ]] || mkdir -p ${vardir}/$resource_dn

   for i in $(seq 1 $simulated_resource_nsc_count)
   do
     resource_nsc_mac=${MAC[$i]}
     resource_fqdn=psp${i}-s1.${resource_dn}
     #echo "$resource_fqdn $resource_nsc_mac" 
     echo "$resource_fqdn $resource_nsc_mac" >> $resource_nsc_list_file     
   done
   echo "----------------------------------"
done

# DEBUG EXIT
exit

if [[ ! -f $target_config_list_file && $arg1 != "--no-target-config-list" ]]; then
  echo "No $target_config_list_file. "
  echo "Creating new without assignments"
  echo "# place "force_reconfigure" at end of line to reconfigure when occpied" >  $target_config_list_file
  if [[ -f $remote_nsc_list_file ]] ; then
   echo "#"                           >> $target_config_list_file
   echo "# Possible remote nsc fqdns" >> $target_config_list_file
   echo "#"                           >> $target_config_list_file
   awk '{print "#", $1}' $remote_nsc_list_file >> $target_config_list_file
   echo "#"                           >> $target_config_list_file
   echo "# Assign just by adding a remote nsc after the resource nsc" >> $target_config_list_file
   echo "#"                           >> $target_config_list_file
   echo "# RESOURCE-NSC (the physical machine)\tREMOTE-NSC (the hostname in the remote system)" >> $target_config_list_file
   echo "#"                           >> $target_config_list_file
  fi
  awk '{print $1}' $resource_nsc_list_file >> $target_config_list_file
fi
