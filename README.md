# Black-Scholes Option Pricer

![Dashboard](images/main_screenshot.png)


## Introduction 
This project provides a tool for traders to compute option prices using the Black-Scholes model.
To support the analysis of the financial instrument it includes heatmaps displaying the effect of 
potential volatility and underlying price variations. Finally, to facilitate parallel analysis,
the different computations are stored in a MySQL database and are accessible through a navigation 
interface.

## Model
The model used for this project is the original Black-Scholes model for options on a non-dividend-paying 
stock[^1]:

[^1]: Option volatility and pricing (2nd edition) - Sheldon Natenberg

$$\text{Call price} = SN(d_1) - XN(d_2)exp(-rt)$$
$$Put price = XN(-d_2)exp(-rt) - SN(-d_1)$$




## Language, tools and limitations

## How to use it




