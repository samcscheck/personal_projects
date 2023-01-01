/*                                                                     
** Description: This program allows the user to play hangman against the computer.
**              This file contains the main driver as well as all of the functions
**              required to run the program. 
*/

#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <cstdlib>
using namespace std;

const int NUM_WRONG = 6;  // specified number of wrong guesses before game ends
const int ASCII_VAL = 97;  // this ASCII value will be used to indicate lower case letters
const char YES = 'y';  // indicates the user input to continue the game
const char NO = 'n';  // indicates the user input to end the game
const char NULL_TERMINATOR = '\0';  // used to identify empty array spaces
const char UNDERSCORE = '_';  // used to indicate letters the user has not guessed yet
const string FILE_NAME = "words.txt";  // specified file name for the list of words used
const string SPACE = " ";  // used for formatting letters throughout the game

int readFile(string fileName);
void loadWords(string fileName, string wordArr[], int arrSize);
char playGame(string keyWord);
void displayPuzzle(char solvedChars[], int arrSize);
char guessChar();
bool updatePuzzle(char guess, string keyWord, char solvedChars[], int arrSize);
bool usedChar(char usedChars[], int arrSize, char guess);
int numLettersLeft(char solvedChars[], int arrSize);

int main() {
    srand(time(NULL));

    cout << "Welcome to UMBC Word Guess" << endl;
    // arrSize contains the int returned from readFile, the number of words 
    // contained in the file FILE_NAME
    int arrSize = readFile(FILE_NAME);
    cout << arrSize << " words were imported." << endl;

    string wordArr[arrSize];
    // loadWords loads each word read in FILE_NAME into wordArr
    loadWords(FILE_NAME, wordArr, arrSize);

    char yesOrNo;
    string keyWord;  // variable to hold the random word
    // this do while loop continues playing the game until the user input indicates otherwise
    do{
        keyWord = wordArr[rand() % arrSize];
        yesOrNo = playGame(keyWord);
    }while(yesOrNo == YES);
    cout << "Thanks for playing UMBC Word Guess!" << endl;
  return 0;
}

/*
** Name: readFile
** PreCondition: none
** PostCondition: returns the number of words listed in the file and 
**                and confirms that the file exists
*/
int readFile(string fileName){
    string word;  // used to read through each word in the file
    int arrSize = 0;  // count in order to create an array of correct size
    ifstream myFile (fileName);

    if(myFile.is_open()){
        cout << "Your file was imported!" << endl;
        while(myFile >> word){
            ++ arrSize;
        }
    }else{
        cout << "Your file failed to open." << endl;
    }

    myFile.close();
    return arrSize;
}

/*
** Name: loadWords
** PreCondition: fileName exists as a file, arrSize is large enough to hold each word
**               read in from the file fileName
** PostCondition: wordArr will contain strings of each word contained in the file fileName
*/
void loadWords(string fileName, string wordArr[], int arrSize){
    ifstream myFile (fileName);
    string word;  // used to read in each word in the file

    int i = 0;
    while(myFile >> word){
        wordArr[i] = word;
        ++ i;
    }
    myFile.close();
}

/*
** Name: playGame
** PreCondition: keyWord contains a string of letters and no symbols
** PostCondition: returns char YES or NO to indicate if the user would like to 
**                continue playing
*/
char playGame(string keyWord){
    int numWrong = 0;  // counter for when the user guesses wrong
    int wordLen = keyWord.length();  // stores the length of keyWord to use as length of solvedChars

    char solvedChars[wordLen];  // array which holds the puzzle
    // fills solvedChars with underscores
    for(int j = 0; j < wordLen; j++){
        solvedChars[j] = UNDERSCORE;
    }
    char usedChars[NUM_WRONG];  // array which holds wrong guesses
    // fills userChars with null terminators
    for(int j = 0; j < NUM_WRONG; j++){
        usedChars[j] = NULL_TERMINATOR;
    }

    cout << "Ok. I am thinking of a word with " << wordLen << " letters." << endl;
    // while loop continues as long as the user has not guessed the word and 
    // has not used all guesses
    while (numWrong != NUM_WRONG && numLettersLeft(solvedChars, wordLen) != 0){
        // the next two lines display the status of the game to the user
        cout << numLettersLeft(solvedChars, wordLen) << " letters remain." << endl;
        displayPuzzle(solvedChars, wordLen);

        char guess = guessChar();  // this char holds user input
        bool usedGuess = usedChar(usedChars, NUM_WRONG, guess);
        bool correctGuess = updatePuzzle(guess, keyWord, solvedChars, wordLen);

        // accounts for a correct guess that has not been guessed before
        if(correctGuess && !usedGuess){
            usedChars[numWrong] = guess;
        }
        // accounts for a wrong guess that has not been guessed before
        else if(!usedGuess){
            cout << "There are no letters " << guess << " in the puzzle" << endl;
            usedChars[numWrong] = guess;
            ++numWrong;
            cout << "You have " << (NUM_WRONG - numWrong) << " bad guesses left." << endl;
        }
        // accounts for a guess which has already been guessed
        else{
            ++numWrong;
            cout << "The letter " << guess << " has already been guessed." << endl;
            cout << "You have " << (NUM_WRONG - numWrong) << " bad guesses left." << endl;
        }
    }

    // displays message if the word was not guessed before chances ran out
    if(numWrong == NUM_WRONG){
        cout << "Sorry, you lost." << endl << "The correct word was: " << keyWord << endl;
    }
    // displays message if the word was guessed
    else{
        cout << "Congrats, you won!" << endl << "The correct word was: " << keyWord << endl;
    }
    
    char newGame;  // holds the YES or NO char from the user
    do{
        cout << "Another game? y/n" << endl;
        cin >> newGame;
    }while(newGame != YES && newGame != NO);
    return newGame;
}

/*
** Name: displayPuzzle
** PreCondition: none
** PostCondition: prints the puzzle so far, with spaces in between letters/underscores
*/
void displayPuzzle(char solvedChars[], int arrSize){
    // the for loop iterates through the entire solvedChars array and prints each char
    for(int i = 0; i < arrSize; i++){
        cout << solvedChars[i] << SPACE;
    }
    cout << endl;
}

/*
** Name: guessChar
** PreCondition: none
** PostCondition: returns the user input as a char
*/
char guessChar(){
    char guess;
    // this do while loop ensures that the user input is a lowercase letter
    do{
        cout << "What letter would you like to guess?" << endl;
        cin >> guess;
    }while(guess < ASCII_VAL);
    return guess;
}

/*
** Name: updatePuzzle
** PreCondition: none
** PostCondition: changes any letters in solvedChars that correspond with the user's guess
**                and returns whether there was any change made to the solvedChars array
**                
*/
bool updatePuzzle(char guess, string keyWord, char solvedChars[], int arrSize){
    bool correctGuess = false;  // this bool will only change to true if a letter in keyWord 
    // equals the guess made by the user
    for(int i = 0; i < keyWord.length(); i++){
        if(keyWord[i] == guess){
            // switches the solvedChars empty value to the guessed char
            solvedChars[i] = guess;
            correctGuess = true;
        }
    }
    return correctGuess;
}

/*
** Name: usedChar
** PreCondition: none
** PostCondition: returns whether the guess existed in the userChars array
*/
bool usedChar(char usedChars[], int arrSize, char guess){
    for(int i = 0; i < arrSize; i++){
        // if statement to check if the guess exists in the usedChars array
        if(usedChars[i] == guess){
            return true;
        }
    }
    return false;
}

/*
** Name: numLettersLeft
** PreCondition: arrSize is greater than 0
** PostCondition: returns the number of letters left for the user to guess
*/
int numLettersLeft(char solvedChars[], int arrSize){
    int lettersLeft = 0;

    // loop to count the number of spaces left
    for(int i = 0; i < arrSize; i++){
        if(solvedChars[i] == UNDERSCORE){
            ++lettersLeft;
        }
    }
    return lettersLeft;
}
