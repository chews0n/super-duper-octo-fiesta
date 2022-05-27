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

## Feature List
A rough draft of all of the inputs for the model
## Melanie
- Pressure (time dependant)
- Production rates divided on a 30 day basis (time dependant)
- Previous time period's production volumes (Oil/Gas) (time dependant)
- completions - this will probably be a bunch of different things like shot density, phasing, OH, etc.... (constant)

## Islam
- length of the well (constant)
- location of well (constant)
- Permeability (constantish)
- Porosity (constantish)

## Monica
- vertical/horizontal (flag for well) (constant)
- depth (constant)
- initial saturations (constant)
- Stimulation/water flooding/secondary or tertiary recovery methods - this is probably be a classification input meaning you have lots of different names that correspond to different values within the model. So what you would do here is convert them to discrete numbers (ie. 0, 1, 2, 3) and each of them corresponds to a separate type that you're referring to. (time dependant)

## Pre First Steps
- We will need to decide on what we're going to do. So that means what types of field(s) we're going to pull data for. For example, last year we looked at all wells in the last 10 years in the Montney. You guys might want to do something different though. Probably where ever Monica is working is best.
ANSWER: SO we're going to look at wells in the Montney, but what does that entail. We'll use BCOGC data, so we have functions to recycle from the last assignment. I would try to limit that to the last 10 ish years of data and do forecast horizons of 10 years max, although I guess we could try to push that and try to be more "predictive", but that's a little sketchy.
- Also, with this what are we going to predict? Probably oil/gas production, but on what timeline and are we going to do time dependant predictions, meaning that we would have to train separate models for each time horizon and then probably use that output as the new input for the next time horizon, so on and so forth. What you could do is monthly production values (you have monthlies from the data) over a 10-20 year time horizon and training the separate models at each month.
ANSWER: Are we going to look at oil volumes or gas volumes or condensate or some sort of BOE of the three? Do all 3, that might get interesting though with wells that have no oil, but you can guard against that in the inputs.
Time dependent horizons, so for that I would suggest no more resolution than monthly on a 10 year horizon.

## First Steps
1. We will need to grab data for this. Where to get this data and how to use it will be the important parts
2. Once we have the data, starting cleaning it, preferably something that takes in the raw data and uses scripting to clean out the data. This will be useful for using this on other sets of data, probably of the same type. What do I mean by that, I mean that if you're using for example GeoScout data, you should be able to use other GeoScout data with the cleaning software. Having said that, GeoScout data is usually fairly clean for modern wells/completions.
