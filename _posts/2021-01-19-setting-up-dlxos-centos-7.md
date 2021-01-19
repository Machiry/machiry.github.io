---
title: "Setting up DLXOS (ECE 469) on Cent OS 7"
date: 2021-01-19
permalink: /posts/2021/01/dlxos-centos-7/
tags:
  - DLXOS
  - ECE 469
---

This post describes the steps to setup DLXOS needed for Purdue ECE 469 labs on Cent OS 7 VirtualBox VM.

There are three steps here: Setting up VM, Install dependencies, and Setting up DLXOS tools.

## VM Setup
1. Download the (Cent OS 7 Virtual Box Image)[https://sourceforge.net/projects/linuxvmimages/files/VirtualBox/C/7/CentOS_7.7.1908_VBG.zip/download]
2. Extract the above folder and (import the .ova VM)[https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html]
> You may need to change the network adapter to NAT
> Login into the VM with username: centos and password: centos


> The following steps have to be run inside the VM.
## Install Dependencies
```
sudo yum install glibc.i686
sudo yum install libstdc++.so.5
```

## Setting up DLXOS tools
```
mkdir ~/ee469
cd ~/ee469
scp [your-account]@ecegrid.ecn.purdue.edu:~ee469/labs/common/dlxos_new.tar.gz .
tar -xvzf dlxos_new.tar.gz
```
### Setting up the PATH
```
gedit ~/.bashrc
# at the end of the file append the following line
export PATH=~/ee469/dlxos_new/bin:$PATH
(save and clode gedit)
```

That's it. You are all set.

To test, open a terminal and run `dlxsim`, you should see some help message.
