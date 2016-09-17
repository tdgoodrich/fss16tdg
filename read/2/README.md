# READ2

### Citation

Cataldo, M., Mockus, A., Roberts, J. A., & Herbsleb, J. D. (2009). Software dependencies, work dependencies, and their impact on failures. IEEE Transactions on Software Engineering, 35(6), 864-878. [Paper link](http://ieeexplore.ieee.org/document/5166450/).

### Summary

Incorrectly met dependencies cause a large number of customer-reported software failures. The authors study different types of dependencies and their affect on a dataset of eight years' of software development. The primary results gauge the relative impact of syntactic, logical, and work dependencies.


### Keywords

* ii1. Syntactic dependency: the dependency of one piece of software on correctly calling another piece, such as an API.
* ii2. Logical dependency: the inferred (non-explicit, non-syntactic) dependency between source files and their interactions. For example, a change spread over several files is likely to introduce a bug.
* ii3. Workflow dependency: The temporal aspects of software development.
* ii4. Coordination requirements: The intradeveloper coodination requirements.

### Main Items

* iii1. Motivating statements. The authors start by outlining three different types of dependencies -- syntactic, logical, and work. They note that each dependency is rather distinct from the others, creating the need for a study of each dependency and their _relative importance_. They note that unlike in defect prediction, they are not building predictive models, but rather looking back and evaluating past data to understand exactly what dependencies really mattered and which ones didn't.
* iii2. Related work. Section 2 begins with an overview of the existing literature in software dependencies, syntactic and logical, and Section 3 covers work dependencies. They note that the classic syntactic dependency literature started in compiler optimization, where dependencies could be automatically generated as abstract syntax trees, and noted previous work such as the notions of coupling and cohesion from Stevens et al. (citation 43), functional relationships by Hutchens and Basili (citation 29), and clustered methods for evaluating modularization from Selby and Basili (citation 40), among several other techniques. Contrastingly, they note how logical dependencies were developed in the different field of software evolution (again with several cited techniques) and how work dependencies have recently become popular in failure proneness literature.
* iii3. Checklists. The authors explicitly outline their questions of interest in the first two sections:
  * **RQ 1**. _What is the relative impact of syntactic and logical dependencies om the failure proneness of a software system?_
  * **RQ 2**. _Do higher levels of work dependencies lead to higher levels of failure proneness of a software system?_

* iii4. Data set. The authors note that they use two large software projects for their analysis. The first project was a distributed computer storage system, with three years development and four releases. The project has 114 developers in eight teams and three locations, where they produced 5 million lines of code in 7,737 source files in C and 117 in C++. The second project was from embedded systems, and consisted of forty developers nearly all working in one location over five years and six releases. The project consisted of 1.2 million lines, with 1,224 C files and 427 C++ files.

# Improvements

* iv1. More diverse data. The two datasets the authors examined were relatively the same: C and C++-based projects with O(1 million) lines of code and around 4 years of development. Do the conclusions hold true for different languages? For smaller projects? For projects with sporadic development or longer/shorter development times? More data would have helped answer these questions. The authors do note this weakness in their threats to validity.
* iv2. Some figures. The paper only contains tables of results and no plots. As a visual-based person, I would have gotten intuition faster with some nice plots.
* iv3. More motivation for the definition of coordination requirements. The work requirements are split into two measures, workflow dependency and coordination requirements. While workflow dependencies are given a fair amount of citations and discussions, the authors simply cite a framework by Cataldo et al. (citation 6) for coordination requirements. Is this the only framework? How and where has it been evaluated? I thought this was ill-defined. 
