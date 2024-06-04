# Black-Scholes Option Pricer

![Dashboard](images/main_screenshot.png)


# Introduction 
This project provides a tool for traders to compute option prices using the Black-Scholes model.
To support the analysis of the financial instrument, heatmaps display the effect of 
potential volatility and underlying price variations. The GUI uses the [Streamlit](https://streamlit.io/) 
Python framework. Finally, to facilitate parallel analysis, the different computations are stored in a MySQL 
database and are accessible through a navigation interface.

# Model
The model used for this project is the original Black-Scholes model for options on a non-dividend-paying 
stock[^1]:

[^1]: Option volatility and pricing (2nd edition) - Sheldon Natenberg

$$\textbf{Call price} = S \thinspace N(d_1) - X \thinspace e^{-rt} \thinspace N(d_2) 
\quad \quad \quad 
\textbf{Put price} = X \thinspace  e^{-rt} \thinspace N(-d_2) - S \thinspace N(-d_1)$$

$$ \text{where} \quad\quad d_1 = \displaystyle\frac{ln\frac{S}{X}+\frac{\sigma ^2}{2}t}{\sigma \thinspace \sqrt{t}}   
\quad\quad\text{and}\quad\quad 
d_2 = d_1 - \sigma \thinspace \sqrt{t} $$


S: underlying price  
X: exercise price  
t: time to expirations in years  
r: domestic interest rate  
&sigma;: annualized volatility in percent

# How to set up and run the app

## Python
The project was developed using Python 3.12 and the versions of the different 
installed libraries are specified in the [requirements](requirements.txt) file.

## Setting-up the database

The application requires a locally hosted MySQL database named: Option_Pricer_DB.
Run the following command in MySQL to create the database.

    CREATE DATABASE Option_Pricer_DB;

## Setting Environment Variables

To access the database, the username and password needs to be recorded in environment variables. 

    export DB_USERNAME_OPTION_PRICER='your_mysql_username'
    export DB_PASSWORD_OPTION_PRICER='your_mysql_password'

## Running the Project

    streamlit run main.py


# Limitations of Streamlit
Streamlit framework triggers a complete run of the code for every interaction with the GUI and interrupts any 
previously running code. There is therefore no way to implement atomicity for every code execution. Locking mechanisms
which normally guarantee full execution of a portion of the code can in this framework be aborted at any moment 
by any new interaction with the GUI. Bugs have been observed when clicking repeatedly fast on the buttons,
resulting in variables maintaining the current state of the system to be corrupted. An acceptable practice is to wait 
a second between two button clicks not to corrupt the system.

# How to use it
## Interface
![Parts](images/parts_screenshots.png)
The GUI is divided in three parts. The first one is used to enter model inputs and to navigate through the
computed values. Any forbidden value triggers a message inviting the user to correct the given input. 
The second part displays the results of the model: prices of the put and call options and heatmaps
displaying the price variations of the options if volatility and underlying price deviate in the ranges +/-10.
The third part shows the inputs to the model corresponding to the displayed prices and heatmaps guaranteeing 
certainty in the provided information.

## User controls
**_Compute_** button runs the model computation, stores the values in the database and display them. In case 
the inputs have not been changed since the last computation, the values are not computed and the last computation
is loaded from the database. This prevents storing unnecessarily the same values.

**_Next_** and **_Previous_** load and display the next or previous model computation stored in the database.





