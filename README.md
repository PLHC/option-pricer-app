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

$$\text{Call price} = S \thinspace N(d_1) - X \thinspace e^{-rt} \thinspace N(d_2) $$

$$\text{Put price} = X \thinspace  e^{-rt} \thinspace N(-d_2) - S \thinspace N(-d_1)$$

$$ d_1 = \frac{ln\frac{S}{X}+\frac{\sigma ^2}{2}t}{\sigma \thinspace \sqrt{t}} $$  

$$ d_2 = d_1 - \sigma \ thinspace \sqrt{t} $$



## Language, tools and limitations

## How to use it




