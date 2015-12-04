#!/bin/ksh
#
# (c) Peter Krauspe 10/2015
#
# This script should run on admin machine
#
# creates a status list (or a single entry) of resource_nsc / remote_nsc assignment and current status
#
# Simulation
# TODO all !!
#
# <2step>
#. /etc/2step/2step.vars
#
#dbg=echo
dbg=""
dev=eth0
# ggfs spaeter aus config file
basedir=/opt/dfs/tsctl2
bindir=${basedir}/binsim
confdir=${basedir}/config
vardir=${basedir}/var
typeset resource_fqdn
typeset resource_dn
typeset resource_hn
typeset -A RESOURCE_MACS
typeset -A CURRENT_FQDNS
typeset -A STATUS
typeset arg1=$1

source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers
typeset AllDomainServers=$(echo $RemoteDomainServers $ResourceDomainServers | sed 's/\s+*/\n/g' |  sort -u )

resource_nsc_list_file=${vardir}/resource_nsc.list
nsc_status_list_file=${vardir}/nsc_status.list


function get_domain_server_hn
{
  typeset domain=$1
  typeset hn 

  for fqdn in $AllDomainServers
  do
     if [[ $domain == ${fqdn#*.} ]] ; then
       hn=${fqdn%%.*}  
       echo $hn
       break
     fi
  done 
}

function check_nsc_status
{
  typeset fqdn=$1
  typeset -l ret
  #domain_server=nss.${fqdn#*.}
  domain_server=$(get_domain_server_hn ${fqdn#*.}).${fqdn#*.}
  ping -c 1 $domain_server > /dev/null 2>&1
  if (( $? != 0 )) ; then
    echo "nss_unreachable"
  else
    ssh $domain_server "ping -c 1 $fqdn"  > /dev/null 2>&1
    if (( $? > 0 )) ; then
      echo "unreachable"
    else
      ssh $domain_server "ssh $fqdn uptime"  > /dev/null 2>&1
      if (( $? > 0 )) ; then
        echo "alive"
      else
        echo "ssh-ok"
      fi
    fi
  fi
}

echo "\n<< Create Resource NSC Status (List) .. This may take a while, be patient !!  >>\n" >&2

if [[ ! -f $resource_nsc_list_file ]]; then
  echo "  $resource_nsc_list_file not found, create it .." >&2
  ${bindir}/admin_get_resource_nsc_list.sh --no-target-config-list
fi


# read MAC adresses from resource_nsc's

while read line
do
  [[ $line == \#* ]] && continue
  set -- $line
  fqdn=$1
  mac=$2
  RESOURCE_MACS[$fqdn]=$mac
  RESOURCE_FQDNS_ALL="$RESOURCE_FQDNS_ALL $fqdn"
done < $resource_nsc_list_file

# read nsc_status_list if available
if [[ -f $nsc_status_list_file ]] ; then
  while read line
  do
    [[ $line == \#* ]] && continue
    set -- $line
    resource_fqdn=$1
    current_fqdn=$2
    status=$3
    CURRENT_FQDNS[$resource_fqdn]=$current_fqdn
    STATUS[$resource_fqdn]=$status
  done < $nsc_status_list_file
fi

if [[ -n $arg1 ]]; then
  RESOURCE_FQDNS=$arg1
else
  RESOURCE_FQDNS=$RESOURCE_FQDNS_ALL
fi

[[ -f  $nsc_status_list_file ]] && mv $nsc_status_list_file ${nsc_status_list_file}.previous 

for resource_fqdn in $RESOURCE_FQDNS
do
  found=0
  resource_dn=${resource_fqdn#*.}
  resource_hn=${resource_fqdn%%.*}
  
  echo "ping $resource_fqdn in default domain ..."
  resource_status=$(check_nsc_status $resource_fqdn)
  current_fqdn=${CURRENT_FQDNS[$resource_fqdn]}

  if [[ $resource_status == "ssh-ok" ]]; then
    echo "$resource_fqdn $resource_fqdn available" | tee -a $nsc_status_list_file
    found=1
  elif [[ -n $current_fqdn && $current_fqdn != "unknown" ]] ; then
    echo "  try previuos domain for $resource_fqdn ..."  
    remote_status=$(check_nsc_status ${CURRENT_FQDNS[$resource_fqdn]} ) 
    if [[ $remote_status == "ssh-ok" ]]; then
      echo "$resource_fqdn $current_fqdn occupied" | tee -a $nsc_status_list_file
      found=1
    fi
  fi

  if (( $found == 0 )); then
    echo "found=$found : search for $resource_fqdn in all remote domains..."
    for remote_domain_server in $RemoteDomainServers
    do
      echo "LOOK ON $remote_domain_server"
      resource_status_in_remote_domain=$(ssh $remote_domain_server "${bindir}/nss_manage_remote_nsc.sh status $resource_fqdn --force_search")
      if [[ -n $resource_status_in_remote_domain ]]; then
        echo "$resource_fqdn $resource_status_in_remote_domain" | tee -a $nsc_status_list_file
        found=1
        break
      fi
    done
    (( $found==0 )) && echo "$resource_fqdn unknown unreachable" | tee -a  $nsc_status_list_file
  fi
  echo
done  

echo "Done."
