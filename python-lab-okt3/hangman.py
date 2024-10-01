import random

class Word:
    def __init__(self, text: str):
        self.text=text
        #sätt antalet unika bokstäver på detta sätt
        self.letters_to_guess=len(set(text))
        self.letters_in_word=len(text)

    def __str__(self):
        return f"{self.text}, letters_to_guess {self.letters_to_guess} "

class Hangman:
    def __init__(self, count: int):
        self.words: list[str]=[]
        #vi kan sätta antalet felaktiga försök varje spel
        self.count: int=count

    def add_word(self, word) -> None:
        self.words.append(word)

    def select_random_word(self) -> Word:
       return random.choice(self.words)

    @staticmethod
    def letter_in_word(word, letter):
        if letter in word.text:
            word.letters_to_guess-=1
            return True, word
        else:
            return False, word

    def is_letter(self, letter):
        if len(letter)>1:
            letter=input("Felaktigt format, prova igen")
            self.is_letter(letter)
        return letter

    def roll_the_game(self):
        word = self.select_random_word()
        print(f"Ordet är valt, total bokstäver: {word.letters_in_word}; total uniqka bokstäver:{word.letters_to_guess}")
        while self.count>0:
            letter = input(f"Skriv in en bokstav, ord att gissa {word.letters_to_guess}")
            letter=self.is_letter(letter)
            letter_exists, word =self.letter_in_word( word, letter)
            if word.letters_to_guess == 0:
                print ("Du har vunnit!")
                return
            if not letter_exists:
                self.count-=1
                print(f"Fell, men du har {self.count} rundor kvar")
        print("Oh, du har förlorat!")
        return

def main():
    word_1=Word(text="apple")
    word_2=Word(text="rose")
    game=Hangman(count=10)
    game.add_word(word_1)
    game.add_word(word_2)
    start_the_game=input("Vill du börja spellet? Ja/Nej").strip().lower()
    if start_the_game == "ja":
        game.roll_the_game()
        main()
    elif start_the_game == "nej":
        print("ok, Bye")
        return
    else:
        print("Felaktig input!")


if __name__=="__main__":
    main()

















