# Digital Score Analysis Dashboard

This dashboard provides visualizations and insights on the average digital scores of websites across different countries. It includes a world map visualization, a bar chart for individual countries, and additional information on the websites of selected countries.

## Features

- Count of websites in different categories - Poor, Average, Good
- Slider to navigate between any ranges of digital scores and drill down to view specific features
- How websites digitisation changes over time
- Interactive world map showing the average digital score by country
- Bar chart displaying the digital score distribution for each country
- Clicking on a country in the world map updates the bar chart and displays the websites for that country
- Clicking on a bar in the bar chart updates the displayed websites

## Getting Started

### Clone the Repository


```shell
git clone https://github.com/kartikeysharma95UZH/digi_score.git
```

### Setting up the Environment

- Navigate to the project directory:
```shell
cd digi_score/visualisation_plotly_dash_code
```

### Create and activate a virtual environment (optional, but recommended):

```shell
python3 -m venv env      # Create a virtual environment
source env/bin/activate # Activate the virtual environment
```

### Install the required packages from the requirements.txt file:

```shell
pip install -r requirements.txt
```
This will install all the necessary packages and their specific versions for the project.

## Running the Application

To run the Dash application, use the following command:

```shell
python home.py
```
![Image Description](images/home.png)


```shell
python page1.py
```
![Image Description](images/page1.png)


```shell
python linechart.py
```
![Image Description](images/linechart.png)

```shell
python over_time.py
```
![Image Description](images/over_time.png)

```shell
python geography.py
```
![Image Description](images/geography.png)
![Image Description](images/geography_2.png)

## Dataset


The dataset used for this project is locations_100.csv, which contains information about website locations and their digital scores.

## Technologies Used


- Python
- Pandas
- Plotly
- Dash
- Dash Bootstrap Components

