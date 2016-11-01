# READ7

### Citation

Shen, D., Luo, Q., Poshyvanyk, D., & Grechanik, M. (2015, July). Automating performance bottleneck detection using search-based application profiling. In Proceedings of the 2015 International Symposium on Software Testing and Analysis (pp. 270-281). ACM. [Paper link](http://dl.acm.org/citation.cfm?id=2771816).

### Summary

The authors formulate the problem of performance-testing large websites in terms of search-based software engineering.

### Keywords

* ii1. Application profiling: Quantitatively profiling a program (i.e. benchmarking).
* ii2. Performance analysis: Studying the practical performance (e.g. responsiveness) of a program.
* ii3. Dynamic analysis: Studying the execution properties (e.g. space and time complexities) of a program.
* ii4. Search-Based Software Engineering: The subfield of converting software engineering problems into an optimization problem, and then using search algorithms (e.g. genetic algorithms) on this model.

### Main Items

* iii1. Motivating statements: The authors begin with an introduction that motivates the study of performance maintenance, including bugs. They mention a survey of 148 enterprises, of whom 92% reported that improving application performance was a top priority. Combined with the large scale of certain applications, such as web applications, the problem is both computationally difficult and of high interest to the community.
* iii2. Hypothesis: The authors named Section 2 simply "Problem Statement", emphasizing the formulation of a specific problem. This step is significant because a well-defined problem needs to be established before applying search heuristics. The stated problem is to _increase the efftiveness of input-sensitive profiling efficiently_. This problem has two parts. First, fast algorithms are needed, the space of all inputs is exponential and cannot be explored arbitrarily. Second, effective and meaningful queries need to come out of this testing.
* iii3. Visualizations: The authors provide a few short-but-sweet pseudocodes to illuminate specific points. An early one is a mere three lines, yet pops up throughout the text as a recurring example. I thought this was a really good use of a figure, it provided the medium for extended discussion from multiple angles.
* iii4. Related work: Near the end of the paper, the authors include a fairly large related work section outlining Profiling, Genetic Algorithms, and Performance Testing. They relate these distinct areas by noting that profiling is a largely manual job for performance bugs, thus the creation of an automated environment (exploring with genetic algorithms) is very welcome.

# Improvements

* iv1. No future work. The authors introduce a concrete problem and provide a baseline result with genetic algorithms. Where should the next research explore? What alternative algorithms are attractive? The answers to these questions would have been appreciated.
* iv2. Plots are too small. Several of the later plots are too small to be read. The captions could also use some work, as they do not stand alone.  
* iv3. More comparisons to previous work. TODDLER in particular is a tool that explored performance bugs using a functional-based approach, similar to phrasing the problem as a search. While the authors do compare to FOREPOST, including TODDLER would have been interesting.
