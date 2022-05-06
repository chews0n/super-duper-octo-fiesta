# Assignment Ideas 

## PDP Evaluations
Output: production forecast -> 5 year production forecast, 10 year, 20 year
NOTE: this is a time dependant variable, so that's something to consider.
What would you use to predict PDP? (Inputs)
- Perm
- OOIP
- Poro
- Historical Prod
- Pressure

TIP: try to keep features/inputs to around 10 max

On what scale should predictably be?
- Formation level
- Reservoir level
- Well level
- Perforation Level

Should we have multiple models based on which formation/reservoir we are in?

So I guess from that, you can also do development optimization. So your model will be able to give you predictions and then you can do another regression to maximize Production or NPV or whatever