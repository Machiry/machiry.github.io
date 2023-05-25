---
permalink: /research/
title: "Research Areas"
author_profile: true
---

My research, in general, has an applied flavor.
Specifically, a principled solution is customized to the underlying domain to
achieve both practical and (mostly) formal guarantees. 

## Embedded Systems Security
____
Internet of Things (IoT) devices or, in general, embedded devices are ubiquitous and are part of our everyday life. 
We have been moving into an ecosystem of having several small, low-powered microcontroller or microcontroller unit (MCU) based devices connected directly to the internet or through a proxy.
The adoption of these small MCU-based devices is growing rapidly and extensively, with an estimated more 
than 50 billion devices.
It is important to ensure that the RTOS and system software that runs as part of these systems
is secure, and we can rely on it to perform the required mission-critical operations.
Furthermore, security vulnerabilities in these systems are likely remotely triggerable.
Similar to other system software, these are developed in unsafe languages, especially C and C++.
Research shows developers using these unsafe languages are prone to introduce security bugs.

In this area, we focus on various areas targeted towards improving the security of embedded systems.
Our research is along the following thrusts:

### Vulnerability Detection
In this thrust, we focus on enabling scalable and precise vulnerability detection on embedded systems.
Analysis techniques face unique challenges when dealing with embedded systems, such as asynchronous execution semantics and hardware dependence.
We explore techniques such as staged static analysis, systematic testing, rehosting-based dynamic analysis, and machine learning for effective vulnerability detection.

Our work has identified over 100 security vulnerabilities in various embedded software, including network stacks.

#### Publications
* **On-going**: Simple, yet effective technique to find security bugs at scale.
* **On-going**: Systematically Detecting Packet Validation Vulnerabilities in Embedded Network Stacks
* [Towards Rehosting Embedded Applications as Linux Applications (DSN Disrupt '23)](../files/dsndisrupt.pdf)

### Developer Support
What challenges do developers face in engineering secure embedded systems?
What mistakes do developers make in designing embedded systems?
Can we develop tools and techniques to assist developers?

These are a few questions we are exploring as part of this thrust.

#### Publications
* **On-going**: Rust for embedded systems -- current state, challenges, and open-problems.
* [Towards Automated Identification of Layering Violations in Embedded Applications](../files/ncmas.pdf)

### Language Based Security
In this thrust, we explore new language primitives that can enable the development of secure embedded systems.
Specifically, new programming languages, additions to existing programming languages, new type systems, etc.

The challenging aspect here is ensuring that our techniques align with embedded system constraints -- low overhead and backward compatibility (i.e., should work with existing codebase).

#### Publications
* **On-going**: Linear Types in Checked C.
* [C to Checked C by 3c](../files/3c.pdf)

### UEFI and Bootloaders Security
In this thrust, we focus on the security of UEFI/EDK-II components.
Specifically, vulnerability detection and prevention.
We are currently exploring dynamic analysis (fuzzing) based techniques to test DXE drivers and services holistically.
We are also exploring techniques for automatically adding Checked C annotations to the UEFI codebase to prevent spatial safety vulnerabilities.
### Supported By

![DARPA](../images/darpa.jpeg) ![Rolls Royce](../images/rr.png)

## Securing Continuous Integration Workflows
----
Continuous Integration (CI) has become essential to the modern software development cycle. Developers engineer CI scripts, commonly called workflows or pipelines, to automate most software maintenance tasks, such as testing and deployment.

Developers frequently misconfigure workflows resulting in severe security issues, which can have devastating effects resulting in supply-chain attacks.
The extreme diversity of CI platforms and the supported features further exacerbate the problem and make it challenging to specify and verify security properties across different CI platforms uniformly.
In this area, we aim to addresses the problem by defining the desired security properties of a workflow and developing platform-independent techniques to verify and enforce the security properties.

### Publications
----
* **On-going**: Framework for Staged Static Taint Analysis of GitHub Workflows and Actions
* [Characterizing the Security of Github CI Workflows (USENIX Security 2022)](https://machiry.github.io/files/gwchecker.pdf) 

### Supported By

![Amazon and NSF](../images/amazonnsf.png)

## Mutation for the Masses
----

