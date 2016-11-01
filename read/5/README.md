# READ5

### Citation

Nistor, A., Song, L., Marinov, D., & Lu, S. (2013, May). Toddler: Detecting performance problems via similar memory-access patterns. In Proceedings of the 2013 International Conference on Software Engineering (pp. 562-571). IEEE Press. [Paper link](http://dl.acm.org/citation.cfm?id=2486862).

### Summary

The authors provide a functional-bug based framework for studying performance-based bugs.

### Keywords

* ii1. Performance bug: Bugs responsible for significant performance degradation (e.g. feeling sluggish).
* ii2. Functional bugs: Bugs responsible for reduced functionality in a software project.
* ii3. Automated oracle: A program that detects if a test triggers a bug (e.g. an ``assertion`` in Python).
* ii4. Performance analysis: The study of a program's qualitative (e.g. responsiveness) and quantitative (e.g. actual speed) properties.

### Main Items

* iii1. Tutorial materials. The authors provide an overview of standard functional bug test creation:

> To test for functional bugs, developers usually follow three steps: (1) write as many and as diverse tests as allowed by the testing budget, (2) run these tests and use automated oracles (e.g., crashes or assertions) to find which tests fail, and (3) inspect _only_ the failing tests.

 After this very quick tutorial, they then refer to these steps later in the paper when describing their own model for performance bugs. I found this inclusion very useful because I could immediately connect their novel results to the existing models.

* iii2. Motivating statements. Tying in with their mini-tutorial, the authors note how historically performance bug analysis cannot follow the functional code framework, mostly due to a lack of quantitative metric. The authors' goal with this paper is to introduce a framework to bridge these two gaps, allowing the study of performance bugs in a functional-based framework.
* iii3. Visualizations. The authors include several pseudocodes that are well-written, including input and output, comments, and proper syntax highlighting. I felt these inclusions were very helpful because they mentally provided a clear view of the framework that could unify performance and functional bugs.

* iii4. The paper ends with a section on related work, outlining two major categories: Profiling, Visualization, and Computational Complexity; and Performance-Bug Detection. The first talks about how existing work has concentrated on the visualization of performance bugs, but has typically suffered from detection limitations (i.e. an oracle with poor solution quality). In previous detection work, the authors note how their nested-loop detection code lead to improvements that previous work couldn't identify. They suggest that TODDLER would work well complementing these techniques.  

# Improvements

* iv1. Ambiguous suggested use of TODDLER. The authors praise their tool for finding performance bugs that other tools could not, but then suggest that their tool is best used to complement existing techniques. I would have found it helpful for the authors to explicitly identify the limitations of TODDLER and when/where alternatives should be used.
* iv2. Missing future work. While the authors provide nice technical details and experiments, they fail to mention what future work could be made on TODDLER. In some sense this is the same problem as not outlining the faults: they are presenting a shiny new toy with little intuition on its faults and future improvements.
* iv3. No open source data or code. The authors spend a significant portion of the paper outlining data structure and implementation details, but do not provide a link for their code.
