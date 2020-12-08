---
title: "Kernel Debugging Ubuntu 16.04"
date: 2020-08-24
permalink: /posts/2020/08/ubuntu-kernel-debug/
tags:
  - Kernel Debugging Setup
  - Ubuntu 16.04
---

> All the following steps are tested on Ubuntu 16.04

There are 3 steps here: Building qemu image, building and installing kernel, debugging

## Building qemu image
### Install qemu
```
sudo apt-get install qemu-kvm qemu virt-manager virt-viewer libvirt-bin
```
### Create a qcow disk
Here, we will create a virtual disk on which ubuntu will be installed.
> Why qcow2? not regular image? 
Because we can increase the size of qcow later, but increasing the size of regular image is tricky.

```
qemu-img create -f qcow2 ubuntu16.04.qcow 40G
```

### Download ubuntu image
```
wget https://releases.ubuntu.com/16.04/ubuntu-16.04.7-desktop-amd64.iso
```
### Installing Ubuntu 16.04 on the disk
```
qemu-system-x86_64 -hda ubuntu16.04.qcow -boot d -cdrom ./ubuntu-16.04.7-desktop-amd64.iso -device virtio-net,netdev=vmnic -netdev user,id=vmnic -m 4G
```
This will open a window on which you follow the instructions to complete the installation.

## Build and install kernel
> Follow these instructions on the host machine
### Clone the kernel sources
```
git clone git://kernel.ubuntu.com/ubuntu/ubuntu-xenial.git
cd ubuntu-xenial
# check out the required kernel
git checkout tags/ubuntu-hwe-4.15.0-112.113_16.04.1
```
### Configure
#### get the default config
Copy the config from the QEMU vm, you can find the config at the following path on the __vm__.
```
/boot/config-`uname -r`
```
Lets say you got the config out from the VM into the host as `ubuntu16.04config`

Now copy the config as `.config` in the `ubuntu-xenial` (i.e., folder where we checked out our kernel sources) i.e.,
```
cp ubuntu16.04config <path to ubuntu-xenial>/.config
```
#### Modify the config (Optional)
```
make menuconfig
```
This will open a window where you can enable or disable additional kernel configuration options.

### Building kernel
```
	chmod a+x debian/scripts/*
	chmod a+x debian/scripts/misc/*
	cp debian/scripts/retpoline-extract-one scripts/ubuntu-retpoline-extract-one
	make deb-pkg
```
### Installing kernel on to the guest
Copy all `*.deb` from host to guest and install the built kernel into the __vm__.
> You should run the following command in guest VM
```
sudo dpkg -i linux-image-<..>.deb
sudo dpkg -i linux-headers-<..>.deb
```

## Debugging Guest VM
First, run the QEMU vm and make qemu wait for the debugger using the following command:
```
qemu-system-x86_64 -s -S -hda ubuntu16.04.qcow -device virtio-net,netdev=vmnic -netdev user,id=vmnic -m 4G -enable-kvm -append "console=ttyS0"
```
This will cause the qemu wait untill the debugger gets attached.

Now in an other terminal window
```
# Go to the folder where we built the kernel
cd <path to ubuntu-xenial>
# gdb
> file vmlinux
> target remote:1234
# You are inside debugger and see that the break point is being hit.
```
Thats it!! You can use the regular gdb commands from now on.

## References
[1] https://wiki.gentoo.org/wiki/QEMU/Options
[2] https://help.ubuntu.com/community/Kernel/Compile#Alternate_Build_Method_.28B.29:_The_Old-Fashioned_Debian_Way
