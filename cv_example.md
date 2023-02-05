# Tobias Burns - Curriculum Vitae

___

## Education

### 2017 - 2019 | Study in pursuit of a PhD before exiting the program | Department of Computer Science, Maynooth University, Ireland | Deep Slam: Utilising Deep Learning for Predictive 3D Mapping, Supervisors: Dr. John McDonald & Prof. Barak Pearlmutter
The past decade has seen a sea change in the capabilities of autonomous robotics. From self-driving cars to unmanned aerial vehicles, robots are moving out of the research lab and into our everyday lives. Central to these advances has been the development of visual sensing algorithms that allow robots to build 3D models of their environment from camera sensors. These models provide a foundation for higher level reasoning and interaction with the world, allowing robots to relate geometric, semantic and dynamic information about the environment. As such, the accuracy and completeness of these 3D models is critically important. In this project I am addressing two important problems with current visual mapping systems: their lack of semantic(object level) information, and their inability to model areas of the environment that they have not yet sensed. Although the latter seems like an impossible task, if we consider our own perception, we constantly deal with partial sensory information of the world, yet cognitively we are capable of bridging these gaps. The mechanism by which we recognise objects, and predict the unseen data to "fill in gaps," is to use past experience of the world. I will develop algorithms with similar capabilities using an approach to machine learning, known as deep learning, to predict the class of objects and complete their structure based on partial data by learning object geometries from online 3D object databases. An important element here will be our approach to understanding uncertainties associated with the algorithm's predictions. Firstly, this is important for processing itself, to know where more data is needed and to provide a confidence level in what the computer thinks it sees. Secondly, for humans using these systems, a representation of how reliable the system is, and how accurate the predicted regions of the map are, is extremely important.

### 2013 - 2017 | **Bachelor of Science (BSc)**, Computer Science and Software Engineering | Department of Computer Science, Maynooth University, Ireland
1st Class Honours 839/1000 Best in Class.

## Awards and Funding

### Sept 2017 | Intel Medal for Best Final Year Student in Computer Science | National University of Ireland Maynooth.

### Oct 2017 | John and Pat Hume Doctoral Scholarship | Awarded by Maynooth University 2017
This provided ~€60,000 over 4 years to pursue my PhD.

### May 2018 | SFI Research Grant | Funded by Valeo and Lero - the Irish Software Research Centre.

## Publications

### 2019 | MouldingNet: Deep-Learning for 3D Object Reconstruction | T. Burns, B. Pearlmutter, and J. McDonald | Irish Machine Vision and Image Processing 2019, Technological University Dublin, Dublin, Ireland | doi:10.21427/synp-mr39

---

## Work Experience

### Apr 2020 - Jul 2022 | **Software Engineer** | Susquehanna International Group, International Financial Services Centre, Co. Dublin, Ireland.

* Given complete ownership/control of a high volume desktop trading tool.
* Designed, developed and supported business critical code using C# and the .Net framework.
* Interviewed and mentored intern software engineers, helping them to develop their skills toward becoming full time hires.

### Feb 2017 - Dec 2019 | **Occasional Lecturer and Lab Demonstrator** | Maynooth University, National University of Ireland, Maynooth, Co. Kildare, Ireland.

* Demonstrated the modules "Introduction to Object Oriented Programming", "Algorithms and Data Structures" and "Software Design".
* Guest lecturer for "Software Design".

### Oct 2016 - Dec 2019 | **Robo Eireann Team Member** | Maynooth University, National University of Ireland, Maynooth, Co. Kildare, Ireland.

* Completed my final year project on visual robot detection.
* Awarded a research internship in June 2017 for the development of a new system for visually detecting lines on a pitch.
* Attended Robocup 2017, Nagoya, Japan and took the role Team-Captain at Robocup 2019, Sydney, Australia.

### Feb 2016 - Aug 2016 | **Intern Software Engineer** | Accenture, 1 Grand Canal Square, Grand Canal Quay, Dublin 2, Ireland.

* Wrote reliable, efficient and maintainable code in C# and VB. 
* Worked closely with the companies business analysts and customers, handling shared requirements to meet deadlines and produce high quality software.

## Project Abstracts

### Oct 2016 - May 2017 | Final Year Project | RoboCup -- Visual Robot Detection
Robocup Soccer is an annual competition where teams of autonomous robots play soccer. Robo Eireann, the Maynooth University Robocup team, compete in the Standard Platform League where all robots have uniform hardware and so teams compete on a software level. Localisation, the problem of identifying where one is in a particular space, and object avoidance are two major issues in Robocup soccer. This project focused on improving Robo Eireann's existing systems for performing these operations with the use of visual robot detection. Localisation currently relies on goal post detection which sometimes detects robots arms as false positives. This can have a significant negative impact on the robots behaviour and performance. By pre-filtering regions containing robots prior to goal detection the number of false positives would be greatly reduced. Object avoidance relies on sonar which has a very short range. Using a vision system to detect other robots is both longer range and more robust in terms of localisation. Previously the Robo Eireann robots had no system for visually detecting other robots. This project addressed this problem by applying the histogram of oriented gradients algorithm. This algorithm extracts a feature vector via the gradient orientation in local image regions. These features, along with a relevant classification label, are then fed into a support vector machine which is trained to perform robust robot detection. We found running a full histogram of oriented gradients on the images to be too slow due to the exhaustive nature of the search. To solve this problem a quick heuristic for finding candidate regions of an image had to be used. Discarded points from Robo Eireann's ball detector tended to cluster around a robots legs. Using these points to create a bounding box around candidate regions increased the overall efficiency of our system. Our detector was trained and tested using 3-fold cross-validation on 200 images with a precision of 95% and a recall of 80%. To ensure that the outputs of the project could be exploited by Robo Eireann, a major component of the work focused on integration within the existing code base. The net result of this is a robot detection system that works both with Robo Eireann's PC toolset and is deployable directly onto the Nao robot.

### Jun 2017 - Aug 2017 | Robocup -- Research Intern 2017 | Pitch Line Detection
Based on the success of my final year project described above I was offered a position on the Robo Eireann team as a research intern for 6 weeks. This internship allowed me to gain an understanding of advanced robotic software systems development and in particular the challenges of working with a team of researchers to create a unified real-time robotic software system. My main role was to develop systems for visually detecting lines on the pitch for use in localisation. As part of the internship I also travelled to Japan to participate in Robocup 2017 as a full team member for the competition. Since the internship I have continued as an active member of the team, staying involved in the platform development and a number of outreach activities over the current academic year.

---

## Programming Languages and Software

### Best: | C#

### Other: | Python, C++, Java, CUDA

### Software: | Blazor, Caffe, Tensorflow, Eclipse, Visual Studio, Git, LATEX, Linux, Windows

## Interests and Other Projects

* I have entered and organised several coding competitions including an internal SIG competition, IEEEXtreme, Google CodeJam, AIB Datathon and IrlCPC.
* Reading, gaming, technology and music.
* Volunteer work.