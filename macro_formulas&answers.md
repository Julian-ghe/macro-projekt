Inside Real GDP (Chained Prices$)
Outside Real GDP (Chained Prices$)
Population
Workforce
avg. annual hours per worker
Human Capital Index
Real Consuption (Current 2021 Prices$)
Domestic Absorbtion (Current 2021 Prices$)
Inside Real GDP (Current 2021 Prices$)
Outside Real GDP (Current 2021 Prices$)
Capital Stock (Current 2021 Prices$)
Capital Service level (Current 2021 Prices$)
TFP level (Current 2021 Prices$)
Welfare level (Current 2021 Prices$)Welfare level (Current 2021 Prices$)
Real GDP  (Constant 2021 Prices$)
Real Consuption (Constant 2021 Prices$)
Domestic Absorbtion (Constant 2021 Prices$)
Capital Stock (Constant 2021 Prices$)
Capital Service level (Constant 2021 Prices$)
TFP level (Constant 2021 Prices$)
Welfare level (Constant 2021 Prices$)

irr	Real internal rate of return	
delta	Average depreciation rate of the capital stock	
		
Exchange rates and GDP price levels		
xr	Exchange rate, national currency/USD (market+estimated)	
pl_con	Price level of CCON (PPP/XR), price level of USA GDPo in 2021=1	
pl_da	Price level of CDA (PPP/XR), price level of USA GDPo in 2021=1	
pl_gdpo	Price level of CGDPo (PPP/XR), price level of USA GDPo in 2021=1	
		
Data information variables		
i_cig	0/1/2/3/4: relative price data for consumption, investment and government is extrapolated (0), benchmark (1), interpolated (2), ICP PPP timeseries: benchmark or interpolated (3) or  ICP PPP timeseries: extrapolated (4)	
i_xm	0/1/2: relative price data for exports and imports is extrapolated (0), benchmark (1) or interpolated (2)	
i_xr	0/1: the exchange rate is market-based (0) or estimated (1)	
i_outlier	0/1: the observation on pl_gdpe or pl_gdpo is not an outlier (0) or an outlier (1)	
i_irr	0/1/2/3: the observation for irr is not an outlier (0), may be biased due to a low capital share (1), hit the lower bound of 1 percent (2), or is an outlier (3)	
cor_exp	Correlation between expenditure shares of the country and the US (benchmark observations only)	
		
Shares in CGDPo		
csh_c	Share of household consumption at current PPPs	
csh_i	Share of gross capital formation at current PPPs	
csh_g	Share of government consumption at current PPPs	
csh_x	Share of merchandise exports at current PPPs	
csh_m	Share of merchandise imports at current PPPs	
csh_r	Share of residual trade and GDP statistical discrepancy at current PPPs	
		
Price levels, expenditure categories and capital		
pl_c	Price level of household consumption,  price level of USA GDPo in 2021=1	
pl_i	Price level of capital formation,  price level of USA GDPo in 2021=1	
pl_g	Price level of government consumption,  price level of USA GDPo in 2021=1	
pl_x	Price level of exports, price level of USA GDPo in 2021=1	
pl_m	Price level of imports, price level of USA GDPo in 2021=1	
pl_n	Price level of the capital stock, price level of USA in 2021=1	
pl_k	Price level of the capital services, price level of USA=1	

Term defintions:
Production (GDP): 
    Nominal GDP($Y):  Total value with current prices of produced goods&services 
    Real GDP(Y): Total units at fixed price (accounts for inflation)                            
    Logarithmic Real GDP(ln(Y)): acounts for interest on intrest
    Real GDP per capita/worker: real measure standard of living?
Technological Progress (A): Advancements allowing increased GDP
Savings (s): % savings rate
Economic growth rate: % change in GDP
    Business cycle: reccuring expansion & contraction of economy 
Profit (Π): Total revenue - total costs per firm
Employment rate: % population engaged in production goods&services
    „Real“ wage (w)
    Total Labour input (N)

Aggregate Income/Input:
    Taxes (T): Transfer payment made to state
    Consumption(C): Good&Services purchase by households
    Purchasing Power Parity: (PPPs) How much people are willing to spend
    Investment(I): Money spent by businesses
        Stock of Capital(K): Amount of money owned in a country
        Rental Rate(r): Percentage of Capital invested in the economy
    Goverment Expendature(G): Money spendt by goverment
Prices (P): Cost of goods
    Inflation rate(): % Increase in Price of daily goods
    GDP Deflator(Pt):  Increase in good produced per state
    Consumer price index (CPI): Price Increase „regular“ goods
    Interest rate: % paid for borrowed mony 
Trade:
    Exports (X): goods&services sold to other countries
    Imports(IM): goods&services provided by other countries
    Net exports(NX) = X - IM

Correlations:
    Population 
    Workforce 
    avg. annual hours per worker
    TFP Level (B)

    Real GDP (Y) = Real GDP (Constant 2021 Prices$)
    Nominal GDP ($Y1) = Inside Real GDP (Current 2021 Prices$)
    Nominal GDP ($Y2) = Outside Real GDP (Current 2021 Prices$)
    ln(Y) = ln(Y)
    Real GDP per capita = Y / Population
    Real GDP per worker = Y / Workforce

    Technological Progress (A) = TFP level
    Total Labour Input (N) = Workforce × avg. annual hours per worker
    Stock of Capital (K) = Capital Stock (Constant 2021 Prices$)
    Rental Rate (r) = (Real internal rate of return) -> Not there for Iran
    Capital-output ratio = K / Y

    # For Solov Model:
    Domestic Absorption (C+I+G) = Domestic Absorption
    
    # For expenditure decomposition & cross-country comparison:
    C = csh_c × $Y2
    I = csh_i × $Y2
    G = csh_g × $Y2
    X = csh_x × $Y2
    IM = csh_m × $Y2

1. 
    (b) Construct the series for real output per capita. Plot the series and discuss its evolution over
    time. Construct and plot the growth of real output per capita. What is the average growth
    rate over the whole sample? What can be inferred about the country’s business cycles?

    Formulas:
        - Real GDP per capita (t) = Y (t) / Population (t-1)
        - Growth rate of real GDP per capita (t) = ln(Real GDP per capita(​t)) - ln(Real GDP per capita(​t-1))
        - Average growth rate over the whole sample (t) = (ln(Real GDP per capita(​t=T)) − ln(Real GDP per capita(t=​0)​​)) / T

    Results (Iran):
        - plots_task1/1b_real_gdp_per_capita.png
        - Average Growth Rate: 0.96%
        - Inferrence on Business Cycle: (TODO Joseph) 
    
    Results (Qatar):
        - plots_task1/1b_real_gdp_per_capita.png
        - Average Growth Rate: -0.69%
        - Inferrence on Business Cycle (TODO Joseph) 


    (c) Plot and discuss the evolution of the unemployment rate over the whole sample. What is
    the average unemployment rate? What are the largest and the smallest values, and when
    were they reached? Are there any particularities of the labor market in this country?

    Formulas: 
        - Unemployment-Rate(t) = 1 - Workforce(t) / Population(t)
    
    Results (Iran):
        - plots_task1/1c_unemployment.png
        - Smallest Value for Unemployment Rate (Including date): 68.52 %  (in 2019)
        - Average Unemployment Rate: 72.53 %
        - Largest Value for Unemployment Rate (Including date): 77.48 %  (in 1986)
        - Evolution of Unemployment Rate: (TODO Joseph) 
        - Standouts in Labour Market?: (TODO Joseph) 

    Results (Qatar):
        - plots_task1/1c_unemployment.png
        - Smallest Value for Unemployment Rate (Including date): 20.09 %  (in 2015)
        - Average Unemployment Rate: 43.97 %
        - Largest Value for Unemployment Rate (Including date): 59.13 %  (in 1971)
        - Evolution of Unemployment Rate: (TODO Joseph) 
        - Standouts in Labour Market?: (TODO Joseph) 

    (d) Construct and plot the inflation rate. Discuss the evolution of the inflation rate in this
    economy. Is monetary policy inflation targeting? If so, since when and how successful has
    the monetary authority been at ensuring price stability?

    Formulas:
        - GDP Deflator (t) = $Y1 (t) / Y (t)
        - Inflaition Rate =  (GDP Deflator (t) /  GDP Deflator (t - 1)) - 1 = (pl_con (t) /  pl_con (t - 1)) - 1

    Results (Iran):
        - plots_task1/1d_inflation_methods_per_country.png
        - plots_task1/1d_inflation.png
        - Evolution of Inflation Rate: (TODO Joseph) 
        - Is monetary policy inflation targeting?: (TODO Joseph) 
        - If so, since when and how successful has it been at ensuring price stability? (TODO Joseph) 

    Results (Qatar):
        - plots_task1/1d_inflation_methods_per_country.png
        - plots_task1/1d_inflation.png
        - Evolution of Inflation Rate: (TODO Joseph) 
        - Is monetary policy inflation targeting?: (TODO Joseph) 
        - If so, since when and how successful has it been at ensuring price stability? (TODO Joseph) 

    (e) Using the stylized facts discussed in Lecture 3 as a benchmark, create similar stylized facts
    for your chosen country and discuss them. For example, some questions to be answered are:

    Formulas:
        - Real GDP per worker = Y / Workforce
        - Logarithm Real GDP per worker = ln(Real GDP per worker)
        - Real GDP per capita = Y / Population
        - Logarithm Real GDP per capita = ln(Real GDP per capita)
        - Laborshare = Real Wages * N / Y
        - Capitalshare = 1 - Laborshare

    Results:
        - plots_task1/1e_stylized_facts.png

        (i) Real GDP per Capita
        - Discussion: (TODO Joseph) 
        - Is the country among the rich or the poor countries?: (TODO Joseph)
        
        (ii) Logarithm Real GDP per Capita
        - Discussion: (TODO Joseph)
        - Does grow at relativly constant rate (typical for advanced economies): (TODO Joseph)

        (iii) Growth Real GDP per Capita
        - Discussion: (TODO Joseph)
        - Has it experienced high or low growth over the past decades?: (TODO Joseph)

        (vi) Real GDP per Worker
        - Discussion: (TODO Joseph)
        - Is this a strong per worker economy?: (TODO Joseph)
        
        (v) Logarithm Real GDP per Worker
        - Discussion: (TODO Joseph)
        - Does it converege with towards the other economies?: (TODO Joseph)

        (vi) Growth Real GDP per Worker
        - Discussion: (TODO Joseph)
        - Has it experienced high or low growth over the past decades?: (TODO Joseph)

        (vii) Labour Share / Capital Share
         - Discussion: (TODO Joseph)
         - Does it stay relatively constant (typical for advanced economies): (TODO Joseph)
         - Is this a worker driven economy?: (TODO Joseph)

2. Basic Solov Model
    (1)	Yt = B(Kt)α(Nt)1−α (Cobb-Douglas production function: F(Kt ,Nt))
    (2)	Kt+1 = St + (1 − δ)*Kt (Future Capital accumilation function)
    (3)	wt = (1 − α)B(Kt)αN−α (Firm first order condition: F‘N)
    (4)	rt = αB(Kt)α−1(Nt)1−α (Firm first order condition: F‘N)
    (5)	Ct + St = Yt (Perfect Competition)
    (6)	St = sYt (Savings rate to output)
    (7)	Nt+1 = (1 + n)Nt (Household biology)

Part 2 - Model Simulation:
    Annahmen explizit:
        (i) N = Workforce (ohne Stundenkorrektur): avh nur 2005+ für MENA, deshalb nutze ich konsistent für alle Länder N = "Workforce" (= emp). Effekt: ich vergleiche "pro-Worker"-Größen statt "pro-Stunde". Strenger nach macro_formeln.md wäre N = Workforce × hours, aber nur USA/VEN hätten dann lange Reihen.

        (ii) TFP-Reihen enden 2019: für 2(c) und 2(e) breche ich die TFP-basierten Plots bei 2019 ab. Reale Mengen (K, Y, N) gehen weiter bis 2023.

        (iii) α zeitlich variabel: α_t = 1 − labsh_t (wie PWT es selbst macht). Für die zeitliche Variation in Cobb-Douglas ist das sauberer als ein konstanter Wert.

        (iv) ARE und DZA: in 2(c)/(d)/(e) ausgeschlossen, weil labsh fehlt. Sie bleiben in 2(a)/(b) drin.

        (v) Steady-State-Approximation in 2(d): K/Y* = s/(n+δ) ohne TFP-Wachstum (g=0) — die einfache Solow-Version aus den 7 Modellgleichungen. Wenn du g≠0 willst, ist das eine 1-Zeilen-Anpassung.

        (vi) Sparquote s ≈ csh_i (Investitionsanteil an PPP-GDP). Das ist die Standard-Solow-Approximation; theoretisch sauberer wäre s = (Y−C)/Y, aber für PPP-Daten ist csh_i konsistenter.


    Take the general Solow model studied in Lecture 4 to perform a model simulation for the
    chosen economy. 

    (b) Calibrate the model parameters - the capital share of income α, the population growth rate n, the depre-
    ciation rate of capital δ, the output per capita growth rate g, and the investment share of
    GDP s. Assume that A is initially equal to one, i.e. A0 = 1.

    Results:
        - plots_task2/2b_calibration.png
    
    (c) Assume that the country is in a steady state, i.e., that the per capita variables grow at a
    constant rate (balanced growth) from t = 0. Compute steady-state values for the variables.

    Results:
    (Steady state values per variable)

        Iran:
            - k̃* (capital per effective worker):   17.4109
            - ỹ* (output per effective worker):    5.4598
            - c̃* (consumption per effective worker): 4.0681

        Qatar:
            - k̃* (capital per effective worker):   30.2064
            - ỹ* (output per effective worker):    12.2885
            - c̃* (consumption per effective worker): 8.9758


    (d) Consider that in period 20 there is an exogenous shock that permanently changes one of
    the parameters of your choice, e.g., s, n, etc.. Motivate the parameter choice for the policy
    exercise and the magnitude of the change.

    Results:
        - Paramtere Choice: 
            - Iran: s (delta −0.05) 
            - Qatar: n (delta −0.04)
        
        - Motivation: 
            - Iran: Savings rate drops by 5 pp (1986 oil price crash + tightened US sanctions reduce investment capacity; directly visible in the actual csh_i data for 1986–90 and 2012+)
            - Qatar: Population growth falls from ~6 % to ~2 % (normalization after LNG construction phase, lower migration inflows; observable in PWT data from 2016 onwards)

    (e) By what percentage do the steady state values change after the permanent shock?

    Results:
     (% Change Steady state values per variable)

        Iran:
            - k_tilde: -41.606% (shock pre: 17.411, shock post: 10.167)
            - c_tilde: -27.356% (shock pre: 5.460, shock post: 3.966)
            - y_tilde: -22.482% (shock pre: 4.068, shock post: 3.154)

        Qatar:
            - k_tilde: 439.662% (shock pre: 30.206, shock post: 163.012)
            - c_tilde: 245.871% (shock pre: 12.289, shock post: 42.502)
            - y_tilde: 245.871% (shock pre: 8.976, shock post: 31.045)

    (f) Create time series for ˜kt, ˜yt, ˜ct, At, kt, yt, ct, ln(yt), ln(ct), and gy
    t = ln(yt) − ln(yt−1).
    Simulate 100 periods.

    Results:
        - plots_task2/2fg_simulation_Iran.png
        - plots_task2/2fg_simulation_Qatar.png

    (g) Create a set of diagrams showing the evolution over time of the above-mentioned variables
    and discuss your results.

    Results:
        - plots_task2/2fg_simulation_Iran.png
        - plots_task2/2fg_simulation_Qatar.png
        - Discussion: (TODO Joseph)

    3. Perform a comparison of the three countries. Discuss similarities and differences and possible
    factors, in particular government policies, that may explain them.

    (TODO Joseph: Choose interesting Comparisons from existing Data)
    (TODO Joseph: Important use 2 i, j, k graphics)

     Results:
    - Discussion: (TODO Joseph)

