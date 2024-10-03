import json
import random
from datetime import datetime, timezone, timedelta

def log_method(func):
    def wrapper(*args, **kwargs):
        print(f"Anropar metod: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


class Word:
    def __init__(self, word_to_guess: str):
        self.word_to_guess=word_to_guess
        #Sätt antalet unika bokstäver på detta sätt
        self.letters_to_guess=len(set(word_to_guess))
        self.letters_in_word=len(word_to_guess)

    def __str__(self):
        return f"{self.word_to_guess}, bokstäver att gissa: {self.letters_to_guess}, bokstäver att"

class Hangman:
    # Vi kan sätta antalet felaktiga försök varje spel
    # Nu kan vi komma åt count genom "self" och "cls"
    count: int = 0

    def __init__(self, words:list[Word]):
        self.words = words
        self.word_of_the_round: str = ""
        self.start_time: datetime = None
        self.duration: timedelta =timedelta()

    #När funktionen når sitt slut, returnerar den None
    def add_word(self, word) -> None:
        self.words.append(word)

    def select_random_word(self) -> Word:
       return random.choice(self.words)


    @staticmethod
    def letter_in_word(word, letter):
        if letter in word.word_to_guess:
            word.letters_to_guess-=word.word_to_guess.count(letter)
            return True, word
        else:
            return False, word

    @log_method
    def is_letter(self, letter):
        if len(letter)!=1:
            letter=input("Felaktigt format, prova igen")
            return self.is_letter(letter)
        return letter

    @log_method
    def roll_the_game(self):
        word = self.select_random_word()
        self.word_of_the_round=word.word_to_guess
        print(f"Ordet är valt, total bokstäver: {word.letters_in_word}; totalt unika bokstäver: {word.letters_to_guess}")
        while self.count>0:
            letter = input(f"Skriv in en bokstäv, ord att gissa {word.letters_to_guess}")
            letter=self.is_letter(letter)
            letter_exists, word =self.letter_in_word( word, letter)
            if word.letters_to_guess == 0:
                print ("Du har vunnit, kolla  på game log!")
                return
            if not letter_exists:
                self.count-=1
                print(f"Fell, du har {self.count} rundor kvar")
        print("Oh, du har förlorat, kolla på game_log om du vill veta mer!!")
        return

    @classmethod
    def load_the_game(cls, filename):
        words_to_guess_list=[]
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                for line in f:
                    word=line.strip().split('.')[1].lower()
                    words_to_guess_list.append(Word(word_to_guess=word))
            cls.count=3
            game_round=cls(words=words_to_guess_list)
            return game_round
        except FileNotFoundError:
            print("Filen hittas inte")
        except Exception as e:
            print(e)


    def save_the_file(self, filename):
        duration=datetime.now(timezone.utc)-self.start_time
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    data=[]
                    print(e)

        except FileNotFoundError:
            print("Files hittar inte")
        except Exception as e:
            print(e)

        data_to_save={'start_time': self.start_time.isoformat(),
                      'duration': str(duration),
                      "word_of_the_round": self.word_of_the_round}

        data.append(data_to_save)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)






def main():
    game_round=Hangman.load_the_game("words_to_guess.txt")
    start_the_game=input("Vill du börja spelet? Ja/Nej").strip().lower()
    if start_the_game == "ja":
        game_round.start_time=datetime.now(timezone.utc)
        game_round.roll_the_game()
        game_round.save_the_file("game_log.json")
        return main()
    elif start_the_game == "nej":
        print("ok, Bye")
        return
    else:
        print("Felaktig input!")
        return


if __name__=="__main__":
    main()

















