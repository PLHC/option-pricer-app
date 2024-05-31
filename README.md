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

$$\textbf{Call price} = S \thinspace N(d_1) - X \thinspace e^{-rt} \thinspace N(d_2) 
\quad \quad \quad 
\textbf{Put price} = X \thinspace  e^{-rt} \thinspace N(-d_2) - S \thinspace N(-d_1)$$

$$ \text{where} \quad\quad d_1 = \frac{ln\frac{S}{X}+\frac{\sigma ^2}{2}t}{\sigma \thinspace \sqrt{t}}   
\quad\quad\text{and}\quad\quad 
d_2 = d_1 - \sigma \thinspace \sqrt{t} $$

<<<<<<< Updated upstream
=======
S: underlying price
<<<<<<< Updated upstream
=======

X: exercise price

t: time to expirations in years

r: domestic interest rate

&sigma;: annualized volatility in percent
>>>>>>> Stashed changes

X: exercise price

t: time to expirations in years

r: domestic interest rate

&sigma; : annualized volatility in percent

>>>>>>> Stashed changes


## Language, tools and limitations

## How to use it




