# READ3

### Citation

Bertram, D., Voida, A., Greenberg, S., & Walker, R. (2010, February). Communication, collaboration, and bugs: the social nature of issue tracking in small, collocated teams. In Proceedings of the 2010 ACM conference on Computer supported cooperative work (pp. 291-300). ACM. [Paper link](http://dl.acm.org/citation.cfm?id=1718972).

### Summary

The authors claim that issue tracking is fundamentally a social, not software-exclusive, process. They study issue tracking systems used by small and collocated software development teams. The authors note real-world practices and offer suggestions for future systems.

### Keywords

* ii1. Shared knowledge: A body of knowledge shared and maintained -- a "centralized brain".
* ii2. Issue tracking: Software used by numerous stakeholders for managing issue reports, assignments, tracking, resolution, and archiving.  
* ii3. Collocated development teams: Software development teams from a single institute and geographical location.
* ii4. Quality assurance: Teams that find and verify defects and their associated fixes.

### Main Items

* iii1. Related work. The authors start with a related work section about computer-supported cooperative work. One example is Perry et al.'s work on the perceived and actual time allocations for various tasks (citation 15), who found that half a developer's time is spent interacting with co-workers. Ye (citation 21) found that software is both knowledge-intensive and collaboration-based. Several other works in computed-based cooperative work are also provided.
* iii2. Study instruments/sampling procedures. In the Design and Participants sections, the authors detail how the participants were selected and data collected. Specifically, 15 participants were chosen from four North American software teams, and given a questionnaire and interview. The questionnaire included questions like how long the participant worked with an issue tracking system, their primary uses for it, and the frequency with which they used the communication channels. The interview included questions about various aspects of issue tracking systems, specifically about users' workflow, coordination, issue lifecycle, and information seeking habits.
* iii3. Tutorial. After defining how their data was collected, the authors spend a good amount of space outlining issue trackers in a historical context. They start with the conventional definition (an issue tracker as a software tool "that enables the [development] team to record and track the status of all outstanding issues associate with each configuration object"). They then look at the issue tracker as a knowledge repository, as a boundary object, as a communication and coordination hub, and as a communication channel. I found this explicit enumeration of the various facets very useful -- as a software engineer I know what an issue tracker is, but I also took many of these facets for granted and didn't initially consider them.
* iii4. Patterns/baseline results. After the tutorial, the authors examine contrasting perspectives on issue tracking. For example, in a subsection titled "A Bug List, A Task List, or a To-do List?" As a boundary object, an issue tracker can be interpreted as any of these three lists depending on the stakeholders. Various points are discussed in this section, based on the conducted interviews, which ultimately concludes with a well-formulated design consideration:

 **Design consideration #1:** _The issue tracker often represents different things to different people. These small but insignificant distinctions should be acknowledged and exposed in the issue tracker through features catering to each of the stakeholder's individual needs. Customizable, role-oriented interfaces that emphasize certain aspects of the tracker's data while abstracting away others may provide a better fit for the multitude of stakeholders that make up the issue tracking system's audience_

 I appreciated this intuitive format of (a) pattern, (b) result, and (c) recommendation.

# Improvements

* iv1. Size of dataset. The dataset consisted of interviews with 15 programmers from four different groups. This dataset become very small in certain parts, such as one of these groups only had two people, and three of the groups only having one female. The study would be better by either (a) splitting the data they have on different facets, or (b) collecting enough data where these groups are not so tiny.

* iv2. Comparison with results from non-collocated teams. The authors note that the issue tracker was still a central communication hub even though the teams were collocated. A direct comparison of the results to a non-collocated team study, or suggestions for forming such a study, would have improved the context of these particular results.

* iv3. Figures. The paper had no figures except for a single table outlining the participant population demographics. Some visualization of what forms of issue tracking were used, or how people tended to interact with them, would help give intuition to some of the results hidden in discussion text.
