# API Server Exercise

You are given a JSON formatted file containing primary election results by state, county,
party, and candidate. An example record is provided below:

```json
{
    "Pennsylvania": {
        "Chester": {
            "Democrats" :{
                "Humphrey ": 100,
                "McGovern": 50
            },
            "Republicans" :{
                "Nixon": 200,
                "Ashbrook": 2,
                "McCloskey": 1
            }
        }
    }
}
```

Without using a database, create an API that has the ability to do the following:

- Return the winning primary candidates in each state and overall

- Implement an interface that allows a user to choose the state to see the winner for
each, as well as the overall winner

The interface does not need to do anything more than what is listed above. This can be a
CLI (command line) interface, a frontend client, or instructions to leverage RESTful
endpoints. But please consider what you’d do next with more time and let us know!

---

My process: 
  - Set up Flask server. I tested this while developing by running the python file and then navigating here in a browser: 
    - http://127.0.0.1:3333/state_winner?state=...
    - http://127.0.0.1:3333/overall_winner
  - write the get_* functions, wrap them in the route functions, test until results work. 
  - Fuzz test data to iron out function logic. 
    - Discovered possible tie scenario here, added handling for that. (Without this, whichever tied canditate was first in the file would be the winner)
  - Generate a multistate version of the election results JSON for further testing.
  - Added multi-state winning endpoint - useful for my own visibility, might as well be a feature.
  - Added a taskfile out of habit.
  - Write this doc.

Some notes on what could be done from here: 

- No JSON sanitizing: I have not added in validations that the file is formatted correctly or that the types are appropriate, or that votes are positive integers, all that. I'd add a validator to this before deploying it, either built by hand or imported. 

- Assuming names will be unique between democract / republican lists. I believe this is already handled at the ballot level, so the names would come into this JSON as "Johnson (D)" and "Johnson (R)". If not handled upstream there, we can do here at the step of looping through the state winners.

- Popular votes all the day down: In this implementation, the popular vote wins states, and the popular vote wins the overall election. For an electoral college - like implementation, just store a dictionary of state weights, and modify the sum by multiplying where appropriate.

- Counties and parties are completely ignored here. I believe that's correct to the desired logic in the prompt. This tool could easily be extended to count other things factoring that data in, like which party won each state, which party got more votes at the state / federal level. Resisting the urge to scope creep those in here, but they would be quick to add. 

- The prompt says that "You are given a file" containing these things. This reads to me like reading the JSON in from the API request wasn't in the intended scope here, but if it was, this could be added. Each of the three get_* functions takes a "data" parameter for the JSON they parse. For now these are all hardcoded to the variable at the top of the file, but this could also point to the body of the request by modifying the endpoint function definitions. 

- A note on runtime: Feels obligatory to bring this up in a programming exercise. Parsing the JSONs is all linear time. Finding the maxes is also linear here. It could be brought down to constant time by tracking the currently wining candidate and updating it on each read-in of new votes, but I think that's overkill. 