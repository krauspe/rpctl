#!/usr/bin/ksh
#
# (c) Peter Krauspe 10/2015
#
# This script should run on an admin machine.
# It should start the remote reconfiguration of a single or all hosts of a list which assigns resource fqdns to remote fqdns
# ... under development....(24.11.2015)
# 
# Simulation
# TODO all !!
#
# <2step>
#. /etc/2step/2step.vars
#
echo "starting simulated reconfiguration ... (do nothing :-)"
exit
# TODO : create simulated status list


#dbg=echo
dbg=""
dev=eth0
# ggfs spaeter aus config file
basedir=/opt/dfs/tsctl2
bindir=${basedir}/binsim
confdir=${basedir}/config
vardir=${basedir}/var
typeset -A STATUS

typeset -A RESOURCE_MAC
typeset -A REMOTE_FQDN 
typeset -A TARGET_OPTION
typeset -A CURRENT_FQDN
typeset resource_fqdn
typeset current_fqdn
typeset status
typeset -i reconfigure_sucessful
typeset -i vlan_switch_sucessful
typeset -i invalid_entrys
typeset -i double_entrys

source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers
typeset AllDomainServers=$(echo $RemoteDomainServers $ResourceDomainServers | sed 's/\s+*/\n/g' |  sort -u )

resource_nsc_list_file=${vardir}/resource_nsc.list   # all nscs from all resource domains: <resource-nsc-fqdn> <resource-mac-address>
remote_nsc_list_file=${vardir}/remote_nsc.list       # all nscs from all remote domains <remote-fqdn>
nsc_status_list_file=${vardir}/nsc_status.list       # discovered : <resource-nsc-fqdn> <current-fqdn> <status>
target_config_list_file=${vardir}/target_config.list # wanted     : <resource-nsc-fqdn> <remote-fqdn>

# define functions

function ManageDomain
{
  typeset action=$1
  typeset resource_fqdn=$2
  typeset fqdn=$3
  typeset type=$4
  typeset domain_server=$5
  typeset add2line=""

  [[ $type == "rnsc" ]] &&  add2line="resource_fqdn=$resource_fqdn"
  case $action in

   REG)   echo "  REGISTER $remote_fqdn on $remote_domain_server as $type"
           cmd="ssh $domain_server nsc_adm add ${fqdn} $type:${RESOURCE_MAC[$resource_fqdn]} $add2line"
           ;;

   UNREG) echo "  UNREGISTER $fqdn from $domain_server as $type"
           cmd="ssh $domain_server nsc_adm del ${fqdn} $type"
           ;;
  
  esac 

  echo "  $cmd"
  $dbg $cmd > /dev/null
}

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

echo "\n<< Reconfigure Resource NSC's >>\n"

# ensure existence of target_config_list 

if [[ ! -f $target_config_list_file ]]; then
  echo "\n  $target_config_list_file doesn'reg_window exist. exiting !\n"
  exit 1
fi

# ensure existence of resource_nsc_list 

if [[ ! -f $resource_nsc_list_file ]]; then
  echo "  $resource_nsc_list_file not found, create it .."
  ${bindir}/admin_get_resource_nsc_list.sh
fi

# read resource_nsc_list ################
while read line
do
  [[ $line == \#* ]] && continue
  set -- $line
  fqdn=$1
  mac=$2
  RESOURCE_MAC[$fqdn]=$mac  
  VALID_RESOURCE_FQDNS="$VALID_RESOURCE_FQDNS $fqdn"
done < $resource_nsc_list_file

# read remote_nsc_list ################
while read line
do
  [[ $line == \#* ]] && continue
  set -- $line
  fqdn=$1
  mac=$2
  VALID_REMOTE_FQDNS="$VALID_REMOTE_FQDNS $fqdn"
done < $remote_nsc_list_file

# create/update nsc_status_list ################
 echo "\nCREATE/UPDATE nsc_status_list\n" 
 echo "(this may take a while)\n" 
 ${bindir}/admin_get_status_list.sh


# read nsc_status_list ################
while read line
do
  set -- $line
  resource_fqdn=$1
  current_fqdn=$2
  status=$3
  CURRENT_FQDN[$resource_fqdn]=$current_fqdn  
  STATUS[$resource_fqdn]=$status  
done < $nsc_status_list_file

# read target_config_list ################

echo -n "\n<< Read $target_config_list_file and check entrys and integrity ..."

invalid_entrys=0

while read line
do
  [[ $line == \#* ]] && continue # skip comment lines
  set -- $line
  resource_fqdn=$1
  remote_fqdn=$2
  target_option=$3
  # --- check resource_fqdns ------
  echo $VALID_RESOURCE_FQDNS | grep $resource_fqdn >/dev/null 2>&1
  if (( $? > 0 )); then
   echo "  \n$resource_fqdn is NO VALID RESOURCE_FQDN, will be SKIPPED!"
   invalid_entrys=$((invalid_entrys+1))
   continue
  fi
  # --- check remote_fqdns ------
  if [[ $resource_fqdn != $remote_fqdn ]]; then
    [[ -z $remote_fqdn ]] && echo "\n$resource_fqdn: no remote_fqdn assignd , skipping" && continue  # skip entrys without remote_fqdn entry
    echo $VALID_REMOTE_FQDNS | grep $remote_fqdn >/dev/null 2>&1
    if (( $? > 0 )); then
     if [[ $remote_fqdn == "default" ]]; then
       remote_fqdn=$resource_fqdn 
     else
       echo "  \n$remote_fqdn is NO VALID REMOTE_FQDN, will be SKIPPED!"
       invalid_entrys=$((invalid_entrys+1))
       continue
     fi
    fi
  fi
  # --- check end

  REMOTE_FQDN[$resource_fqdn]=$remote_fqdn
  TARGET_OPTION[$resource_fqdn]=$target_option
  RESOURCE_FQDNS="$RESOURCE_FQDNS $resource_fqdn"
  REMOTE_FQDNS="$REMOTE_FQDNS  $remote_fqdn"
  #echo "READ: <$resource_fqdn> <$remote_fqdn> <$target_option>"
done < $target_config_list_file

if (( $invalid_entrys > 0 )); then
  echo "  \n$invalid_entrys INVALID ENTRYS found !! in $target_config_list_file >>"
else
  echo "done. >>"
fi

## (simple) check integrity of target_config_list (may be improved) ################

echo -n "\n<<   Checking multible entrys in $target_config_list_file..." 

echo $RESOURCE_FQDNS | sed 's/\s/\n/g' | sort > /tmp/sorted_list.tmp
cat /tmp/sorted_list.tmp | sort -u            > /tmp/uniq_list.tmp
DIFF_RESOURCE_FQDNS=$(diff --suppress-common-lines /tmp/sorted_list.tmp /tmp/uniq_list.tmp | grep \< | sed 's/<//g' )

echo $REMOTE_FQDNS | sed 's/\s/\n/g' | sort > /tmp/sorted_list.tmp
cat /tmp/sorted_list.tmp | sort -u            > /tmp/uniq_list.tmp
DIFF_REMOTE_FQDNS=$(diff --suppress-common-lines /tmp/sorted_list.tmp /tmp/uniq_list.tmp | grep \< | sed 's/<//g' )

double_entrys=0
for entry in $DIFF_RESOURCE_FQDNS $DIFF_REMOTE_FQDNS
do
  #echo "entry=<$entry>"
  if [[ -n $entry ]] ; then
    double_entrys=1
    echo "\n:ERROR: taget_list contains $entry more than once !! >>"
  fi
done

if (( double_entrys == 1 )); then
  echo "\n  EXITING, because of multible use of identical fqdns"
  echo "  PLEASE CHECK $target_config_list_file !!\n"
  exit
else
  echo ": ok >>\n"
fi

# MAIN
 
for resource_fqdn in $RESOURCE_FQDNS
do
  reconfigure_sucessful=0
  vlan_switch_sucessful=0
  ready_for_reconfiguration=0

  remote_fqdn=${REMOTE_FQDN[$resource_fqdn]}
  target_option=${TARGET_OPTION[$resource_fqdn]}
  current_fqdn=${CURRENT_FQDN[$resource_fqdn]}
  # nss. ersetzen durch Funktionsaufruf der nss oder nss-mgt findet !!
  #resource_domain_server=nss.${resource_fqdn#*.}
  #current_domain_server=nss.${current_fqdn#*.}
  #remote_domain_server=nss.${remote_fqdn#*.}

  resource_dn=${resource_fqdn#*.}
  current_dn=${current_fqdn#*.}
  remote_dn=${remote_fqdn#*.}

  resource_domain_server=$(get_domain_server_hn $resource_dn).$resource_dn
  current_domain_server=$(get_domain_server_hn $current_dn).$current_dn
  remote_domain_server=$(get_domain_server_hn $remote_dn).$remote_dn

  #echo "FOR: <$resource_fqdn> <$remote_fqdn> <$target_option>"


  [[ -z $remote_fqdn ]] && continue  # skip entrys without assignment 
                                     # ist eigentlich redundant !!

  echo "\n-----------------------------------------------------------------------------------------\n"

  echo "EXECUTING: $resource_fqdn => $remote_fqdn ($target_option)"
  if [[ $current_fqdn == $remote_fqdn && $target_option != "force_reconfigure" ]] ; then
    echo "current config of $resource_fqdn is already $remote_fqdn and no force option set. Nothing to do."
  elif [[ ${STATUS[$resource_fqdn]} == "unreachable" || $current == "unknown" ]] ; then
    echo "current status of $resource_fqdn is ${STATUS[$resource_fqdn]}. can not configure !!. Check host !!"
  elif [[ ${STATUS[$resource_fqdn]} == "occupied" ]] ; then
    if [[ $target_option == "force_reconfigure" ]] ; then
      echo "reconfigure $resource_fqdn (currently $current_fqdn) AGAIN as $remote_fqdn due to force option"
      ready_for_reconfiguration=1
    else
      echo "$resource_fqdn is occupied as $current_fqdn and no force option is set. Ignoring."
    fi
  else
    echo "  reconfigure $resource_fqdn (currently $current_fqdn) as $remote_fqdn through $current_domain_server"
    ready_for_reconfiguration=1
  fi

  if (( $ready_for_reconfiguration == 1 )); then

    # RECONFIGURE AND REBOOT
    echo "ssh $current_domain_server ssh $current_fqdn ${bindir}/nsc_reconfigure.sh $remote_fqdn reboot"
    $dbg ssh $current_domain_server "ssh $current_fqdn ${bindir}/nsc_reconfigure.sh $remote_fqdn reboot"

    if (( $? == 0 )); then 
      reconfigure_sucessful=1
    fi
    # SWITCH VLAN 

    if (( $reconfigure_sucessful == 1 )); then 
      echo "  switch vlan for $resource_fqdn into $remote_dn"
      cmd="$bindir/control_rem_pil_test_net.sh -c $remote_dn  $resource_fqdn"
      echo "  $cmd"
      $dbg $cmd >/dev/null 

      if (( $? == 0 )); then 
        vlan_switch_sucessful=1
      fi

    else
      echo "  nsc_reconfigure FAILED. vlan will NOT be switched !!"
    fi

    # UNREGISTER / REGISTER ON SUCCESSFUL VLAN SWITCH

    if (( $vlan_switch_sucessful == 1 )); then 

      # ManageDomain <REG|UNREG> <resource_fqdn> <fqdn> <type> <domain_server>

      if [[ $current_fqdn == $resource_fqdn ]]; then
        echo "    current_fqdn == resource_fqdn"
        if [[ $remote_fqdn == $resource_fqdn ]]; then
          #echo "      remote_fqdn == resource_fqdn"
          ManageDomain REG   $resource_fqdn $resource_fqdn nsc $resource_domain_server  # kann man auch weglassen
        else
          #echo "      remote_fqdn != resource_fqdn"
          ManageDomain UNREG $resource_fqdn $current_fqdn nsc $current_domain_server 
          ManageDomain REG   $resource_fqdn $remote_fqdn  nsc $remote_domain_server
          ManageDomain REG   $resource_fqdn $remote_fqdn rnsc $remote_domain_server
        fi
      else
        echo "    current_fqdn != resource_fqdn"
        if [[ $remote_fqdn == $resource_fqdn ]]; then
          #echo "      remote_fqdn == resource_fqdn"
          ManageDomain UNREG $resource_fqdn $current_fqdn  nsc $current_domain_server 
          ManageDomain UNREG $resource_fqdn $current_fqdn rnsc $current_domain_server 
          ManageDomain REG   $resource_fqdn $resource_fqdn nsc $resource_domain_server
        else
          #echo "      remote_fqdn != resource_fqdn"
          ManageDomain UNREG $resource_fqdn $current_fqdn  nsc $current_domain_server 
          ManageDomain UNREG $resource_fqdn $current_fqdn rnsc $current_domain_server 
          ManageDomain REG   $resource_fqdn $remote_fqdn   nsc $remote_domain_server
          ManageDomain REG   $resource_fqdn $remote_fqdn  rnsc $remote_domain_server
        fi
      fi
    else
      echo "  switch vlan FAILED. hostlists will NOT be changed !!"
    fi
  fi

  echo "-----------------------------------------------------------------------------------------\n"
done < $target_config_list_file
