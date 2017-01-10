# Urban mobility analysis for Turin

The project aims to track and analyse Turin's urban mobility with real-time and geo-referenced data.
A particular focus is given to Car Sharing companies and services.

The folder "Architecture" contains the skeleton of what will be the definitive software, while the other folders contain scripts which help us to build modules function by function.

Here's a list of the main conceptual blocks:

- Data Collection
  - Real Time Data Source metaclass
    - Enjoy RTDS
    - Car2Go RTDS
    - [TO]bike RTDS (stopped)
    - GTT RTDS
  
- DataBase Management
  - DataBaseProxy class
  
- Data Mining, Feature Selection and Feature Extraction
  - Provider metaclass
    - Enjoy
    - Car2Go
    - [TO]bike 
    - GTT

- Data Analysis

- Visualization
