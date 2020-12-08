---
title: "Making Kernel Drivers Great Again"
date: 2017-09-23
permalink: /posts/2017/09/kernel-drivers/
tags:
  - Linux Kernel
  - Vulnerability Detection
---

Project: MKDGA

Kernel drivers were once good. A few years ago (circa 2008), Security issues in the Linux kernel were mostly in the non-driver components. Most of us thought Linux kernel is getting better w.r.t security.

In the year 2010, Android came into popularity. Hundreds of vendors started quickly producing android compliant devices. Competition between the vendors became fierce and time to the market became an important factor to capture the growing market.
Android uses Linux kernel as its core. Vendors write drivers to support their Hardware. However, because of Factor 1, These drivers were not *properly* vetted, resulting in drivers becoming the bug-prone components of the Android kernel [1]. If you take a look at the CVEs [2] most of these bugs are embarrassing, it is incredible that such code even exists.

I want to solve this problem and make Linux kernel drivers great again. 
My grand plan:
1) Develop a precise static analysis technique that can find easy bugs.

Before actually developing yet another static bug finding tool, I wanted to check, how the existing tools perform on the android kernel drivers. The results are not good, a huge number of warnings and few times even the code as simple as below snippet raises multiple warnings. 
```
char buf[100];
strcpy(buf, "Hello");
```
Although, I understand that I should *never* use strcpy,  but still the above code is fine.
We need a tool that can spot easy bugs with low false positives (< 20%). By easy I mean, memory corruption vulnerabilities triggerable by the user data. In program analysis lingo, these are called Taint based vulnerabilities. 
Myself along with few amazing people from UC Santa Barbara developed this tool called **DR.CHECKER (published at USENIX Security 2017)** which tries to achieve exactly this in a completely automated way. Furthermore, it has amazing UI, where you can see exactly how user data could cause a reported vulnerability.

Refer:https://github.com/ucsb-seclab/dr_checker , for the usage guide.
2) Develop a smart fuzzer customized for the drivers. 

While looking up existing work on fuzzing Linux kernel fuzzers, I found syzkaller by Google, which truly is a masterpiece and gold standard for fuzzing Linux kernel syscalls. However, one problem with it is that it requires the specification of driver interface. Such as device name, possible ioctl cmd ids and corresponding structures.
Although this information could be easily specified by the driver developers, it is a non-trivial task for a security analyst to do this. We developed a technique called **DIFUZE (going to be published at CCS 2017)** which retrieves the driver interface in an automated way. These interfaces could be used in syzkaller (recommended) or use our simple fuzzer called MangoFuzz to fuzz the drivers.

3) Develop a website where people can submit their kernel.tar.gz and it gives a self-contained docker image customized to analyze the kernel sources both statically and dynamically with a single command run.py.

I registered the domain drchecker.io to integrate DR.CHECKER and DIFUZE into a self-contained docker image, for the analysts to use.

I will be working on this, whenever I find free time. Any additional help is greatly appreciated.
Please do not hesitate to contact me for any details.

References:

[1] https://events.linuxfoundation.org/sites/events/files/slides/Android-%20protecting%20the%20kernel.pdf

[2] https://source.android.com/security/bulletin/

[3] https://github.com/google/syzkaller
