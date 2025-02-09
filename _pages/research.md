---
permalink: /research/
title: "Research Areas"
author_profile: true
---

My research, in general, has an applied flavor.
Specifically, a principled solution will be customized to the underlying domain to
achieve both practical and (mostly) formal guarantees. 

## Embedded Systems Security
____
Internet of Things (IoT) devices or, in general, embedded devices are ubiquitous and are part of our everyday life. 
We have been moving into an ecosystem of having several small, low-powered microcontroller or microcontroller unit (MCU) based devices connected directly to the internet or through a proxy.
It is important to ensure that the RTOS and system software that runs as part of these systems
is secure, and we can rely on it to perform the required mission-critical operations.
Furthermore, security vulnerabilities in these systems are likely remotely triggerable.

In this area, we focus on various areas targeted towards improving the security of embedded systems.
Our research is along the following thrusts:

### Vulnerability Detection
In this thrust, we focus on enabling scalable and precise vulnerability detection on embedded systems.
Analysis techniques face unique challenges when dealing with embedded systems, such as asynchronous execution semantics and hardware dependence.
We explore techniques such as staged static analysis, systematic testing, rehosting-based dynamic analysis, and machine learning for effective vulnerability detection.

> Our work has identified over 100 security vulnerabilities in various embedded software, including network stacks.

#### Publications
* [An Empirical Study on the Use of Static Analysis Tools in Open Source Embedded Software (ISSTA '25)](../files/emsast.pdf)
* [Systematically Detecting Packet Validation Vulnerabilities in Embedded Network Stacks (ASE '23)](../files/emnest.pdf)
* [TEEzz: Fuzzing Trusted Applications on COTS Android Devices (S&P '23)](../files/teezz.pdf)
* [Towards Rehosting Embedded Applications as Linux Applications (DSN Disrupt '23)](../files/dsndisrupt.pdf)

### Developer Support
In this thrust, we are explore following questions related to developer perspectives on securing embedded systems.
What challenges do developers face in engineering secure embedded systems?
What mistakes do developers make in designing embedded systems?
Can we develop tools and techniques to assist developers?

> We identified several open-problems in using Rust for embedded systems.

#### Publications
* [Rust for embedded systems -- current state, challenges, and open-problems (CCS '24)](../files/rustembedccs.pdf).
* [Towards Automated Identification of Layering Violations in Embedded Applications (LCTES '23)](../files/ncmas.pdf)

### Language Based Security
In this thrust, we explore new language primitives that can enable the development of secure embedded systems.
Specifically, new programming languages, additions to existing programming languages, new type systems, etc.

The challenging aspect here is ensuring that our techniques align with embedded system constraints -- low overhead and backward compatibility (i.e., should work with existing codebase).

#### Publications
* **On-going**: Linear Types in Checked C.
* [C to Checked C by 3c (OOPSLA '22)](../files/3c.pdf)

### UEFI and Bootloaders Security
In this thrust, we focus on the security of UEFI/EDK-II components.
Specifically, vulnerability detection and prevention.
We are currently exploring dynamic analysis (fuzzing) based techniques to test DXE drivers and services holistically.
We are also exploring techniques for automatically adding Checked C annotations to the UEFI codebase to prevent spatial safety vulnerabilities.

> We found 20 security vulnerabilities in the latest version of EDK-2.

#### Publications
* [FuzzUEr: Enabling Fuzzing of UEFI Interfaces (NDSS '25)](../files/fuzzuerr.pdf).

### Supported By

![NSF](../images/nsf.jpeg) ![DARPA](../images/darpa.jpeg) ![Rolls Royce](../images/rr.png)

## Securing Continuous Integration Workflows
----
Continuous Integration (CI) has become essential to the modern software development cycle. Developers engineer CI scripts, commonly called workflows or pipelines, to automate most software maintenance tasks, such as testing and deployment.

Developers frequently misconfigure workflows resulting in severe security issues, which can have devastating effects resulting in supply-chain attacks.
The extreme diversity of CI platforms and the supported features further exacerbate the problem and make it challenging to specify and verify security properties across different CI platforms uniformly.
In this area, we aim to addresses the problem by defining the desired security properties of a workflow and developing platform-independent techniques to verify and enforce the security properties.

> We found thousands of security vulnerabilities in various open-source GitHub workflows. More details [here](https://secureci.org/).

### Publications
----
* [ARGUS: Framework for Staged Static Taint Analysis of GitHub Workflows and Actions (USENIX Security '23)](../files/argus.pdf)
* [Characterizing the Security of Github CI Workflows (USENIX Security '22)](https://machiry.github.io/files/gwchecker.pdf) 

### Supported By

![Amazon and NSF](../images/amazonnsf.png)

## Mutation for the Masses
----
Current tools, such as AFL++ and libafl, revolutionalized mutation testing, especially Fuzzing.
Traditionally, fuzzing has been mainly used for testing and bug finding.
However, in this thrust, we explore various other uses and applications of fuzzing (i.e., mutation testing or stochastic search).
We view fuzzing as a way to solve optimization problems intelligently. Provided we can precisely define the following: feedback on how close we are to the desired outcome, a way to map a stream of bytes to the solution space, and an oracle to identify the desired solution.

In addition, we also explore other (more traditional) uses of fuzzing and apply it to dynamic testing of complex systems, such as IoT devices, Kernel Drivers, Network Programs, etc.
We explore different techniques that will enable a security researcher to help the fuzzing techniques to test these complex programs effectively. We have exciting ideas in this direction. Get in touch to know more.

> We used fuzzing techniques to generate thousands of semantically equivalent binaries through existing compilers.

#### Publications
* [Feedback-Guided Software Fault Injection (AsiaCCS '24)](../files/fuzzerr.pdf)
* [Feedback Guided Generation of Binaries (FSE '22)](../files/cornucopia.pdf)

## Checked C and Friends
----
Checked C extends legacy C with checked pointer types that are restricted by the compiler to safe uses. Checked pointer types can coexist with legacy pointers, thus admitting incremental conversion of legacy C to Checked C, in the style of migratory typing. We are working on a technique to port an existing C program to Checked C by converting its pointers to have checked type.

I am also collaborating with David Taditi on this.

#### Publications
* [C to Checked C by 3c (OOPSLA '22)](../files/3c.pdf)

## Binary Analysis: Techniques and Applications
----
I am interested in binary analysis and have always been fascinated by the problems and possible applications.
The ability to analyze executables and identify various semantic information is interesting and challenging.
I use domain-specific techniques to solve common issues with binary analysis tasks.

#### Publications
* [Adaptive Verification of Binary Level Patches (NDSS '25)](../files/veribin.pdf)
* [Feedback Guided Generation of Binaries (FSE '22)](../files/cornucopia.pdf)

## Machine Learing + Security
----
Machine Learning (and Deep Learning) provides us very useful techniques to achieve best-effort solutions in the presence of a large corpus of data. Many problems in security are proven to be intractable; however, providing a best-effort solution is reasonable. On this front, we are exploring the use of various Machine Learning techniques to handle the problems of: Vulnerability Detecton, Prevention and Mobile Privacy.
 
#### Publications
* [Type Inference on Binaries (USENIX Security '24)](../files/tygrusenix2024.pdf)
* [ARBITRAR: User-Guided API Misuse Detection (S&P '21)](../files/arbitrar.pdf)

