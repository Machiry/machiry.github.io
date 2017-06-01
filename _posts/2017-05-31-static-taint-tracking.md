---
layout: post
title: "The need for Extensible anmd configurable Static Taint Tracking for C/C++"
date: 2017-05-31
---

Taint Tracking, as the name implies is a technique to tracks the “taint” of the data throughout the program. The taint of the data is usually a binary attribute, as such can have Boolean values true/false or 1/0. There are other possible representations of the taint, which we ignore for simplicity. Most often taint is used to indicate whether the data is “controlled” by the user or not. Refer [1] for a comprehensive treatment of taint tracking.

One of the most common use case of taint tracking is input validation vulnerability detection. i.e., checking whether the tainted data can reach a program point (or sensitive function) that expects untainted or non-tainted data. For ex: using tainted string as the source string in a strcpy call,  this can lead to overflow of the destination buffer. 

Depending on the method of tracking, Taint Tracking techniques are classified as dynamic or static.

In the case of Dynamic taint tracking, the program is instrumented with taint propagation instructions along with checks to make sure that tainted data does not reach sensitive functions. Dynamic taint tracking is the popular choice for taint tracking. As such there are many tools available to perform dynamic taint tracking on Binaries[3, 4], C/C++ using LLVM [5], Java[6], etc. But, Dynamic Taint Tracking suffers from same disadvantages as any dynamic analysis techniques like Input generation, Speed, etc. Refer [2] for more details about the disadvantages of Dynamic analysis techniques. 

However, In the case of Static taint tracking, standard data-flow techniques are used to propagate taint and warnings are raised when a tainted data may reach a sensitive function. Static taint tracking is not popular. There are only a few tools available for Java, Binaries, Web, etc. 

One interesting thing to note here is that there is No usable static taint tracking tool available for C/C++. Few works try to achieve this, but they are either discontinued [7, 8] or not extensible [7]. 
One work that comes close to achieving this is by Marcelo [9], where they modify the clang static analyzer to perform taint tracking. But clang has disadvantages as in it cannot analyze more than one source file, and it does not have access to the LLVM analyses which are helpful to do interesting stuff. 

The need of the hour is to **have a static taint tracking as LLVM pass**. It is sad to see that a multi-decade technique is not available for the languages for which it is most applicable.

Lack of an extensible and configurable static taint tracking is an open opportunity ignored by the academia. Anyone willing to take up Static taint tracking for C/C++ using LLVM as their project? I am with you and can help you in all stages of the project. 

Good to know: The compilation flag -gsrc to clang produces a bitcode file with accurate source lines information. 

Cheers. 

[1] All You Ever Wanted to know about Dynamic Taint Tracking: https://users.ece.cmu.edu/~aavgerin/papers/Oakland10.pdf 

[2] Table 1 of the pdf: https://link.springer.com/chapter/10.1007/978-3-319-11933-5_13 

[3] libdft: http://www.cs.columbia.edu/~vpk/research/libdft/ 

[4] Google: “Dynamic Taint Tracking for binaries.” 

[5] DataFlowSanitizer: http://clang.llvm.org/docs/DataFlowSanitizer.html 

[6] Google: “dynamic taint tracking for java” 

[7] Context sensitive static taint tracking: https://ece.uwaterloo.ca/~xnoumbis/noumbissi-thesis.pdf

[8] https://github.com/dceara/tanalysis/tree/master/tanalysis

[9] https://www.researchgate.net/publication/312938554_An_User_Configurable_Clang_Static_Analyzer_Taint_Checker 
