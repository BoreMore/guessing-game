# tkinter tutorial from https://www.youtube.com/watch?v=psKTroKLYfs and reference from https://effbot.org/tkinterbook/grid.htm


# package used to generate random number
# credit for random: https://codereview.stackexchange.com/questions/23694/guessing-game-computer-generated-number-between-1-and-100-guessed-by-user
import random
from tkinter import *

# initiates tkinter window
window = Tk()
window.title("Python Guessing Game")
window.geometry("800x640+0+0")
window.resizable(False, False)


# function giving instructions, generating random number, initiating variables and elements of the GUI, and initiating function that asks for the user's first guess
def init(wins, losses):
  # initiates variables
  Label(window, text = "Try to guess the integer between 1 and 100 I'm thinking of!", font = ("arial", 20, "bold"), fg = "black").place(relx=0.5, rely=0.03, anchor=CENTER)
  randomNum = random.randint(1, 100)
  guessesLeft = 10
  print(randomNum)
  alreadyGuessed = []
  prevDifference = 1000

  # sets GUI for stats
  statsLabel = Label(window, text = "Stats", font = ("arial", 15, "bold"), fg = "black")
  statsLabel.place(relx=0.5, rely=0.6, anchor=CENTER)
  winsLabel = Label(window, text="Wins \n" + str(wins), font = ("arial", 15, "bold"), fg = "lime green", borderwidth=2, relief="solid", width=10, height=3)
  winsLabel.place(relx=0.4, rely=0.7, anchor=CENTER)
  lossesLabel = Label(window, text="Losses \n" + str(losses), font = ("arial", 15, "bold"), fg = "tomato", borderwidth=2, relief="solid", width=10, height=3)
  lossesLabel.place(relx=0.6, rely=0.7, anchor=CENTER)

  # sets GUI that displays already guessed numbers
  alreadyGuessedGUI = Label(window, text = "Numbers guessed: ", font = ("arial", 15, "bold"), fg = "dodger blue", borderwidth=2, relief="solid", width=32, height=5)
  alreadyGuessedGUI.place(relx=0.25, rely=0.4, anchor=CENTER)

  # sets GUI for responses
  responseGUI = Label(window, text = "See how close you are here!", font = ("arial", 15, "bold"), fg = "dodger blue", borderwidth=2, relief="solid", width=32, height=5)
  responseGUI.place(relx=0.75, rely=0.4, anchor=CENTER)

  # sets GUIs for guessing areas
  guessInstructions = Label(window, text= "Guess a number", font = ("arial", 17, "bold"), fg = "royal blue")
  guessInstructions.place(relx=0.5, rely=0.15, anchor=CENTER)
  entry = Entry(window, width=25)
  entry.place(relx=0.45, rely=0.20, anchor=CENTER)
  #lambda credit from https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
  enterButton = Button(window, text = "Enter")
  enterButton.place(relx=0.60, rely=0.20, anchor=CENTER)

  # initiates function to ask for first guess passing in all variables defined before as parameters to avoid global variables
  handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)
  

# updates the display based on which action is requested
def handleDisplay(alreadyGuessed, action, response, guessesLeft, alreadyGuessedGUI, responseGUI):
  # if the update already guessed action is requested...
  if action == "updateGuessed":
    # set a new string
    NumbersGuessedString = ""
    # loop through the already guessed numbers 
    for x in alreadyGuessed:
      # if there are 4 in a line create a line break
      if alreadyGuessed.index(x) % 4 == 0 and not alreadyGuessed.index(x) == 0:
        NumbersGuessedString += ", \n" + str(x)
      # dont add a comma for the first number
      elif alreadyGuessed.index(x) == 0:
        NumbersGuessedString += str(x)
      # adds comma and number to string for all other numbers
      else:
        NumbersGuessedString += ", " + str(x)

    # update the GUI to display the already guessed numbers
    alreadyGuessedGUI.config(text="Numbers guessed: " + NumbersGuessedString)

    
  # updates the response box with the new response
  elif action == "updateResponse":
    responseGUI.config(text=response)

  # updates the window
  window.update()



# function that handles the input from the entry box
def handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel):
  # set the guess variable to tkinter string variable
  guess = StringVar()
  # credit for binding: https://stackoverflow.com/questions/50596574/use-enter-key-in-tkinter-python
  # execute conditionals functions with the parameters with enter is pressed
  enterKeyBind = window.bind("<Return>", lambda e: conditionals(guessesLeft, randomNum, alreadyGuessed, prevDifference, int(guess.get()), alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel))
  # set the guess variable to be the input from the entry box
  entry.config(textvariable=guess)
  # updates enterButton to run conditionals function with the new guess
  enterButton.config(command= lambda: conditionals(guessesLeft, randomNum, alreadyGuessed, prevDifference, int(guess.get()), alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel))
  # set focus to the entry box
  entry.focus_set()


# function that controls comparisons between guesses to see if it is correct
def conditionals(guessesLeft, randomNum, alreadyGuessed, prevDifference, guess, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel):
  # function that asks if user wants to play again
  def playAgainFunction(alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel):
    # update wins and losses
    winsLabel.config(text="Wins \n" + str(wins))
    lossesLabel.config(text="Losses \n" + str(losses))
    # removes guess instructions, entry, and enter button to prevent spam
    enterButton.destroy()
    entry.destroy()
    guessInstructions.destroy()
    # function controls reponse to play again
    def response(playAgain, ask, yesButton, noButton):
      # if user wants to play again
      if playAgain == "yes":
        # destroy these elements of the GUI since they will be reinitiated
        statsLabel.destroy()
        winsLabel.destroy()
        lossesLabel.destroy()
        ask.destroy()
        yesButton.destroy()
        noButton.destroy()
        alreadyGuessedGUI.destroy()
        responseGUI.destroy()
        # reinitiate game
        init(wins, losses)
      # if user doesnt want to play again
      else:
        # close window and exit
        raise SystemExit
        window.destroy()

    # GUI asking to play again
    ask = Label(window, text= "Want to play again?", font = ("arial", 15, "bold"), fg = "tomato")
    ask.place(relx=0.5, rely=0.85, anchor=CENTER)
    yesButton = Button(window, text = "Yes", command = lambda: response("yes", ask, yesButton, noButton), width=20)
    yesButton.place(relx=0.40, rely=0.9, anchor=CENTER)
    noButton = Button(window, text = "No", command = lambda: response("no", ask, yesButton, noButton), width=20)
    noButton.place(relx=0.60, rely=0.9, anchor=CENTER)
    
  
  # if the guess is correct update the response and display the number of tries. call playAgainFunction
  if guess == randomNum:
    alreadyGuessed.append(guess)
    handleDisplay(alreadyGuessed, "updateResponse", "You guessed the correct number in \n" + str(len(alreadyGuessed)) + " guesses! \n The number was " + str(randomNum), guessesLeft, alreadyGuessedGUI, responseGUI)
    # adds a win
    wins += 1
    playAgainFunction(alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)

  # checks if a number has already been guessed and displays error if it has been
  elif guess in alreadyGuessed:
    handleDisplay(alreadyGuessed, "updateResponse", "You already guessed this number! \n Try again", guessesLeft, alreadyGuessedGUI, responseGUI)
    handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)
  
  # displays error is guess is more than 100
  elif guess > 100:
    handleDisplay(alreadyGuessed, "updateResponse", "Guess too high! \n Try a number between 1 and 100", guessesLeft, alreadyGuessedGUI, responseGUI)
    handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)
  
  # displays error if guess is less than 1
  elif guess < 1:
    handleDisplay(alreadyGuessed, "updateResponse", "Guess too low! \n Try a number between 1 and 100", guessesLeft, alreadyGuessedGUI, responseGUI)
    handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)

  # if the guess is not the correct number add the number guessed to array of already guessed numbers and decrease the guesses left. then compare the guess to the previous guess. then tell the user the guess was incorrect and if they're getting closer or not
  elif guess != randomNum:
    alreadyGuessed.append(guess)
    guessesLeft -= 1

    # gets absolute value between the random number and guess
    difference = abs(randomNum - guess)
    if difference < prevDifference:
      howClose = "getting warmer"
    elif difference == prevDifference:
      howClose = "the same \n distance as your last guess"
    elif difference > prevDifference:
      howClose = "getting colder"
  
    # response
    handleDisplay(alreadyGuessed, "updateResponse", "Incorrect! \n " + str(guessesLeft) + " guesses left. You're " + howClose, guessesLeft, alreadyGuessedGUI, responseGUI)
    # set prevDifference variable to be the difference for future comparison
    prevDifference = difference
    # call handleInput to listen to user input
    handleInput(guessesLeft, randomNum, alreadyGuessed, prevDifference, alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)
  
    

  # if there are no guesses left update the response and call playAgainFunction
  if guessesLeft == 0:
    handleDisplay(alreadyGuessed, "updateResponse", "Game over! \n You lose. The number was " + str(randomNum), guessesLeft, alreadyGuessedGUI, responseGUI)
    # adds a loss
    losses += 1
    playAgainFunction(alreadyGuessedGUI, responseGUI, enterButton, entry, guessInstructions, wins, losses, statsLabel, winsLabel, lossesLabel)


  # updates the already guessed display every time the conditionals function is run
  handleDisplay(alreadyGuessed, "updateGuessed", None, guessesLeft, alreadyGuessedGUI, responseGUI)

# initiate
init(0, 0)

window.mainloop()