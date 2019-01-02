# Tucar
## An intelligent tutor that uses the socratic method of teaching.

### The tutor is made up of three components:

1. Tutor <br />
  > The tutor will ingest unstructured text and generate a core idea and support ideas of the digested text. The tutor will also generate questions and answers for the digested text. The text should be thought of as a learning objective (like a chapter in a text book) for the students.
2. Conversation Engine <br />
  > The conversation engine interacts with the digested data of the tutor. Its a way to access the structured data of the digested text. If you wanted to create your own bot, you could interact with this API and the Tutor API
3. Chat-Bot <br />
  > Finally the chat bot interacts with the Conversation Engine. There is some logic here for asking the right question at the right time
  
  ```
  CHAT BOT COMMANDS:
  
  help - Show a list of commands
  topics - show a list of learning objectives. These are items that you can be quized on. Its a list of topics seperated by spaces. Its best to copy a topic into your clipboard for a topic you want to be quized on.
  ask [topic] - be asked a random question from the topic.
  !exit - will end any questioning.
  
  ```

  ### An example of how to interact with the chat bot:
  to display all the topics to learn just type `topics`. <br />
  ```
  you: topics
  Tucar: 
  KEPLER_01_ASTRONOMY_BEFORE_KEPLER
  NPR_FACEBOOK_BREACH
  SCHOOL_PYSCH_RTI
  HISTORY_BEHIND_DEMOCRACY
  Quantum_Computing
  GLOCK_19_DEVELOPMENT
  TELE_COM_INTRO
  AI_BASIC_INFO
  ```
  Lets say I want to study `HISTORY_BEHIND_DEMOCRACY` more. I will use the `ask` command.

  ```
  you: ask HISTORY_BEHIND_DEMOCRACY
  Tucar: What came into particular general favor in post-industrial revolution nation states where large numbers of citizens evinced interest in politics?
  ```

  At this point, Tucar is expecting an answer, so give one!

  ```
  you: Representative democracy
  ```

  Tucar will not give feedback based on if you are correct or not. You will most likely get another question.
  
 If you want to digest your own data...
 
 1. access the tutor swagger here: http://localhost:5001/
 2. select POST/tutor/idea/
 3. Enter in your unstrctured text to `learning-material`. It has to be more than 5 setences :) Use an NPR article or a wikipedia section of an article
 4. Enter a name for `file-of-origin`. This should be unique and clearly represent the learning objective of the text. I do not check for name collision at this point. So if you generate a name that is already taken. The bot will just use the first document it finds.
 5. ???
 6. Execute!
 
 This could take about 3-5 mins to process. After it is done, you will see your topic through the chat bot when you type `topics`
 
 ### local execution
 0. install [docker](https://docs.docker.com/v17.12/install/)
 0. install [docker-compose](https://docs.docker.com/compose/install/)
 0. `$ git clone` or download the zip of the code
 0. `$ cd` into the directory 
 0. `$ docker-compose build`
 0. `$ docker-compose up`
 0. navigate to [http://localhost:8080](http://localhost:8080) for the chat bot
 0. navigate to [http://localhost:5000](http://localhost:5000) for the conversation engine API
 0. navigate to [http://localhost:5001](http://localhost:5001) for the tutor API
 
  
