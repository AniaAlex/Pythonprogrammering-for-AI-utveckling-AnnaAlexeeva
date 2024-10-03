
# Upgift: Projekt 1: Hangman

Skapa en version av det klassiska spelet Hangman.

Datorn väljer ett slumpmässigt ord från en fördefinierad lista av ord.

Spelet visar hur många bokstäver ordet består av, men inte vilka bokstäver som är rätt.

Spelaren ska gissa en bokstav i taget, och datorn ger feedback om bokstaven finns i ordet eller inte.

Spelet fortsätter tills spelaren har gissat hela ordet eller har gjort tillräckligt många felaktiga gissningar.

------------------

# Hur spelar man?:

Det finns en fil som heter "words-to-guess", den andra spelare kan använda det för att skapa en ny lista av ord.

Hitta "hangman.py" och starta spelet med `python3 hangman.py`

Datorn kommer att välja ett slumpmässigt ord och ge dig en ledtråd om hur mänga totala och unika bokstäver som finns 
i ordet.

Spelaren har rätt att göra tre misstag. 

Oavsett om spelaren vinner eller förlorar,kommer datorn att spara resultatet i filen "game_log.json".
