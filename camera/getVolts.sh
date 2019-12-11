#!/bin/bash

export LC_ALL=en_GB.UTF-8

readonly I2C_MC_ADDRESS=0x69
readonly I2C_VOLTAGE_OUT_I=3
readonly I2C_VOLTAGE_OUT_D=4


calc()
{
  awk "BEGIN { print $*}";
}

get_output_voltage()
{
	local i=$(i2c_read 0x01 $I2C_MC_ADDRESS $I2C_VOLTAGE_OUT_I)
	local d=$(i2c_read 0x01 $I2C_MC_ADDRESS $I2C_VOLTAGE_OUT_D)
	echo "$i"
	echo "$d"
	calc $(($i))+$(($d))/100
}

i2c_read()
{
  local retry=0
  if [ $# -gt 3 ] ; then
    retry=$4
  fi
  local result=$(i2cget -y $1 $2 $3)
  if [[ $result =~ ^0x[0-9a-fA-F]{2}$ ]] ; then
    echo $result;
  else
    retry=$(( $retry + 1 ))
    if [ $retry -eq 4 ] ; then
      log "I2C read $1 $2 $3 failed (result=$result), and no more retry."
    else
      sleep 1
      log2file "I2C read $1 $2 $3 failed (result=$result), retrying $retry ..."
      i2c_read $1 $2 $3 $retry
    fi
  fi
}

vout=$(get_output_voltage)

voltages=">>> "
voltages+="Vout=$(printf %.02f $vout)V, "
echo "$voltages"
