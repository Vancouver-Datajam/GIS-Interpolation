# Visualization & Prediction of Geospatial BC Climates

## Project team members
- Team lead: Evie Lapalme
- Mentor: Sasha
- Documentation: Art, Ashley, Emilia
- Code Writing: Chloe, Caesar, Thomas, Art, Kelvin, Cecilia, Ashley, Melissa
- Code Review: Chloe, Caesar, Thomas, Art, Kelvin, Ashley, Melissa, Yiquan, Cecilia

## Project statement
The aim of this project is to harness the power of data analysis and geospatial techniques to provide accurate visualizations and predictions of climatic conditions across various regions of British Columbia (BC). By employing Kriging interpolation on a carefully curated point dataset, we seek to create a detailed representation of BC's climate patterns. Additionally, we will develop an interactive geospatial dashboard using Plotly, enabling users to explore and understand the climatic variations in an intuitive and informative manner.

## Presentation
<https://docs.google.com/presentation/d/1uANv49etGWTlsa_tTqWVVDsW2Qh0-beMJwqWW1JWYPg/edit#slide=id.g226d46bec69_0_27>

### Key Tasks
- **Kriging Interpolation**
- **Geospatial Dashboard Development**
- **Visualization and Interpretation**
- **Prediction and Analysis**

### Deliverables
- A well-documented Python codebase that encompasses the entire data analysis process, from data acquisition to dashboard development.
- An interactive geospatial dashboard powered by Plotly, providing easy access to climate information for different regions of BC.

### What we accomplished
Kriging Interpolation:
- Implement the Kriging interpolation method to estimate climate values at unobserved locations.

Model Evaluation:
- The range of our data is -16.8 to 5.5 Celsius. Given that  standard deviation is 5.33 and our errors are below this, this suggests that the model’s predictions are indeed closer to the actual values than the spread of the data!
- an R² score of 0.858 means that approximately 85.8% of the variability in the target variable (temperature in this case) can be explained by the model.

Interactive Dashboard:
- Present the interpolated climate data through visually appealing and informative plots and maps.
Provide insights and context for interpreting the climatic patterns observed.
- Incorporating visual elements like maps, charts, and filters for a user-friendly experience.
- Enable users to input coordinates or select locations on the dashboard to receive predicted climate values.
Offer insights into how the climate varies across different regions of British Columbia.

### Why is this significant
Risk management and mitigation planning
- Geospatial interpolation is more important now than ever with climate change events worsening. This year we saw events like the fires in Hawaii due to poor disaster prevention and management - Moody’s RMS (Risk Management Solutions company) estimated up to $6 billion in economic losses from the devastating wildfires in Hawaii, which killed at least 115 people and destroyed countless homes and businesses. Geospatial interpolation would play a huge role in risk management and mitigation planning: By providing detailed spatial information on climate variables such as temperature (and more) geospatial interpolation supports risk assessment for extreme weather events, sea-level rise, and other climate-related hazards. This information is vital for designing mitigation and adaptation strategies, infrastructure planning, and disaster management. It could save lives and save billions in economic losses. 


### Skills
- **Geospatial Data Analysis Techniques**: Participants will gain hands-on experience in working with geospatial data, including data preprocessing, Kriging interpolation, and mapping.
- **Interactive Dashboard Development**: Participants will learn how to create dynamic and interactive geospatial dashboards using Plotly, enhancing their data visualization skills.
- **Spatial Data Interpretation**: This project will provide insights into how to interpret and visualize spatial data, allowing participants to understand climatic patterns at a regional level.
- **Application of Geostatistical Methods**: Participants will learn how to apply Kriging interpolation, a powerful geostatistical technique widely used in spatial analysis and prediction.
- **Collaboration and Communication**: Working as a team, participants will develop their skills in collaboration, communication, and sharing knowledge in a group setting.
- **Project Documentation**: Participants will gain experience in documenting their code, methodology, and results, which is essential for reproducibility and sharing findings.

### Conclusion
This project presents an exciting opportunity to combine advanced data analysis techniques with geospatial visualization, offering a valuable resource for understanding and predicting climate patterns in British Columbia. Through this endeavor, we aim to contribute to a better-informed understanding of the climatic conditions in this diverse and ecologically significant region.

## Description of Dataset
The dataset from <https://climatebc.ca/> is a comprehensive collection of climate data specifically focused on the province of British Columbia (BC), Canada. It provides a wide range of climate information and analyses tailored to the unique geographical and environmental characteristics of BC. The dataset includes historical climate data, which can be crucial for understanding long-term climate trends, variability, and patterns in British Columbia. Additionally, it may contain model-based projections and forecasts, offering insights into future climate scenarios for the province.

### Scope
- Temperature
- Precipitation
- Decade Averages from 2011-2021

## Vancouver Datajam 2023 Schedule:
- Main page: <https://vancouverdatajam.ca/>

#### Important dates: 

| Date | Description |
| - | - |
| Sept 22 | Projects are released, team introductions, familiarize with the Git |
| Sept 23 | Main Hackathon Day |
| Sept 24 | Wrap-up, judging, awards, and networking event |

|Time| Action item|
| - | - |
| Sept 22, 7pm | Team Meet & Greet |
| Sept 23, 9am | Team Stand-up |
| Sept 24, 9am | Team Stand-up |
| Sept 24, 11am | Deadline for Git repository finalization |
