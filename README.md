<!-- TOC -->
* [Introduction and YouTube demo](#introduction-and-youtube-demo)
* [Pricing model](#pricing-model)
  * [Key Factors Affecting Option Pricing](#key-factors-affecting-option-pricing)
    * [Volatility:](#volatility)
    * [Interest Rate:](#interest-rate)
  * [Equation](#equation)
* [How to set up and run the app](#how-to-set-up-and-run-the-app)
  * [Python environment](#python-environment)
  * [Setting-up the database](#setting-up-the-database)
  * [Setting Environment Variables](#setting-environment-variables)
  * [Running the Project](#running-the-project)
* [Limitations of Streamlit](#limitations-of-streamlit)
* [How to use it](#how-to-use-it)
  * [Interface](#interface)
  * [User controls](#user-controls)
<!-- TOC -->


# Introduction and YouTube demo
This project provides a tool for traders to compute option prices using the Black-Scholes model.
To enhance the analysis of financial instruments, heatmaps visualize the impact of potential changes in volatility and 
underlying asset prices.  
The GUI is built with the [Streamlit](https://streamlit.io/) Python framework. 
To facilitate parallel analysis, the previous computations are stored in a MySQL database and are accessible through a 
navigation interface.

[YouTube demo](https://youtu.be/7kuec0jKjwM)

![Dashboard](images/main_screenshot.png)
# Pricing model
The value of an option reflects the expected profit from holding it. This is derived from the price distribution of the underlying asset and involves two key components:
- Average value of all stock prices above the exercise price[^1]: This represents the weighted average price at which the option would be executed.
- Average payout from exercising the option[^1]: Calculated based on the probability of the option being in the money.

The expected profit from owning the option is the difference between these two components.

## Key Factors Affecting Option Pricing
### Volatility:
**_Volatility_**, the standard deviation of the price distribution, measures the expected price fluctuations in the market. 
Higher volatility increases the likelihood of extreme underlying price movements, therefore raising the option’s value.
### Interest Rate:
**_Interest rates_** impact the present value of the exercise price, as the exercise price is effectively a forward price 
adjusted for the **_Time to Expiration_**.
- Call Options: A higher interest rate increases the price, as holding the stock becomes more costly.
- Put Options: A higher interest rate decreases the price, as holding cash becomes more beneficial due to greater 
interest earnings.

## Equation
By fixing the interest rate and volatility, the option value can be calculated. This project uses the 
original **_Black-Scholes model_** for options on a non-dividend-paying stock[^1]:

[^1]: Option volatility and pricing (2nd edition) - Sheldon Natenberg

$$\textbf{Call price} = S \thinspace N(d_1) - X \thinspace e^{-rt} \thinspace N(d_2) 
\quad \quad \quad 
\textbf{Put price} = X \thinspace  e^{-rt} \thinspace N(-d_2) - S \thinspace N(-d_1)$$

$$ \text{where} \quad\quad d_1 = \displaystyle\frac{ln\frac{S}{X}+\frac{\sigma ^2}{2}t}{\sigma \thinspace \sqrt{t}}   
\quad\quad\text{and}\quad\quad 
d_2 = d_1 - \sigma \thinspace \sqrt{t} $$


_S: underlying price  
X: exercise price
t: time to expirations in years  
r: domestic interest rate  
&sigma;: annualized volatility in percent_

_N_ is the standard cumulative normal distribution function
# How to set up and run the app

## Python environment
This project is built using Python 3.12. All required library versions are explicitly listed in the [requirements](requirements.txt) file.

## Setting-up the database

The application requires a locally hosted MySQL database named: **_option_pricer_db_**.
To create the database, execute the following command in your MySQL environment:

    CREATE DATABASE option_pricer_db;

## Setting Environment Variables

To access the database, store the username and password as environment variables.

    export DB_USERNAME_OPTION_PRICER='your_mysql_username'
    export DB_PASSWORD_OPTION_PRICER='your_mysql_password'

## Running the Project
To start the application, run the following command:

    streamlit run main.py

This will launch the model in your default web browser.

# Limitations of Streamlit
The Streamlit framework triggers a full rerun of the code with every interaction in the GUI, which interrupts any 
previously running code. As a result, it does not support atomicity for code execution. Locking mechanisms that would 
typically ensure the full execution of specific code segments can be aborted by new interactions with the GUI.

This limitation lead to bugs when users click buttons repeatedly or too quickly, causing corruption in 
system state variables. A practical workaround is to wait at least one second between consecutive button clicks to help 
maintain system stability.

# How to use it
## Interface
![Parts](images/parts_screenshots.png)
The GUI is divided in three parts:

**1 - Input and Navigation:** This section allows users to enter model inputs and navigate through the computed values.
If an invalid value is entered, a message invites the user to correct the input.

**2 - Results Display:** This section shows the computed results, including the prices of the put and call options.
It also features heatmaps that illustrate price variations for the options when volatility and underlying price 
fluctuate within a range of ±10.

**3 - Input summary:** This section displays the model inputs corresponding to the currently displayed prices and heatmaps, ensuring 
clarity and accuracy of the provided information.

## User controls
**Compute:** Runs the model computation, stores the results in the database, and displays them. If the inputs remain 
unchanged since the last computation, the values are not recomputed; instead, the previous results are retrieved from 
the database. This avoids redundant computations and prevents storing duplicate values.

**Next (Previous):** Loads and displays the next (or previous) model computation stored in the database.





