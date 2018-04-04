
## <p align="center">tgflow
<p align="center">
<img  src="https://raw.githubusercontent.com/DaniloZZZ/tgflow/master/assets/fgflow.png " width="200"/>
</p>
<p align="center">A declarative-style <a href="https://core.telegram.org/bots/api">Telegram Bot</a> framework

_Here's how you declare a vanilia counter bot:_

```python
from tgflow import TgFlow,handles

TgFlow.configure(token='TOKEN',state='start') # display 'start' state by default
TgFlow.start({'start':{
	# t is for 'text'
    't':handles.st("Hello, i'm hooray bot. Hooray %i times!", 
                   'count',default=1), # pass 'count' value to '%i' in string
    # b is for 'buttons'
    'b':[{
        'Say hooray':lambda count=1:
        ('start',{'count':count+1}) # display 'start' state, increment 'count' value
    }]
}
})

```

* [Getting started.](#getting-started)
* [Writing your first bot](#writing-your-first-bot)
* [Architecture](#architecture)
* [Types](#types)
  * [Prepare](#prepare)
  * [Actions](#actions)
  * [Post processing](#post)
* [Usage](#usage)
  * [Prepare](#prepare)
  * [Actions](#actions)
  * [Post processing](#post-processing)
  * [Multiple files](#multiple-files)
* [CofeeUI](#coffeui)
* [What you should care of](#what-you-should-care-of)
* [More examples](#more-examples)

## Getting started.

There are two ways to install the library:


```
pip3 install tgflow
```
* Installation from source (requires git):

```
git clone https://github.com/DaniloZZZ
cd tgflow
python3 setup.py install
```

It is generally recommended to use the first option.


## Writing your first bot
Tgflow is a state-based framework Each user has a state and data, and each state corresponds to some text and buttons - generally speaking, UI.
It's a good way to imagine your bot as some shema like this:

![ a sample shema](https://raw.githubusercontent.com/DaniloZZZ/tgflow/master/assets/shema.png)

Here's how you to declare states for your bot:
```python
# States.py
from enum import Enum
class States(Enum):
	START=1
	SAY_HOORAY=2
	SET_FAV=3
	ERROR=9
```
Basically, you define state names in separate file and include it everywhere. You can use just strings instead on `Enum` class, but you can`s use some functionality then.

Then, for each state you create a dictionary that defines UI and some simple actions. To handle user input you define your functions and assign them to buttons in UI dict.  You store user-specific data in a dictionary which is passed to you by 'd' argument. Here is a brief example of usage:
```python
from tgflow import TgFlow
from tgflow import handles as h
from States import States # here you defined your states
import logic # some arbitrary code with buisness logic

def show_news(i,**d): # i is for input, s is for state, d is for data
# here i will be callback_query (https://core.telegram.org/bots/api#callbackquery)
	user_id = i.message.from.id
	news=logic.get_news(user_id)
	if news:
		new_state=States.NEWS
	else:
		new_state=States.NO_PERMISSION
	upd_data = {'news':news} # assign user's data to pass forward and store in dict
	return new_state,upd_data

# Unnececary parameters an be omitted.
# Tgflow will automatically determine what to pass.
def show_weather(i,location=None): # you can get user's data by key like this
	user_id = i.message.from.id
	new_data = {'weather': logic.get_weather(location)} # assign user's data to pass forward and store
	return States.WEATHER,new_data
	
UI={States.START:{
	't':"Hello, wanna see some news?",
	'b':[
		{'yes, show me news':h.a(show_news)}, # h.a is an alias for handles.action
		{'no, tell me the weather':h.a(show_weather)}
		]
	},
	States.NEWS:{
	't':h.st("here are your news:\n %s", 'news'),
	 #  h.st pastes value from user's data to string
	 'b':[{'Back':States.START}] # you can leave just state(Enum) without wrapping.
								 # this will forward user to this state.
							 # equivalent to h.a(lambda(s): States.START)
							 # or h.a(lambda(i,s,**d):(i,States.START,d))
	}
	States.WEATHER:{...},		
	States.NO_PERMISSION:{...},						 
				 
```
