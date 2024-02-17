
let setTimer = new Date();
function logTime(message = "") {
    let stopTimer = new Date();
    console.log(message + (stopTimer.getTime() - setTimer.getTime()) / 1000 + " SECONDS")
};
function deleteFirstArrItem(array, item) {
    if (!array.includes(item)) return array;
    let index = array.indexOf(item);
    return array.slice(0, index).concat(array.slice(index + 1));
};
function setInputFilter(textbox, inputFilter) {
    [ "input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop", "focusout" ].forEach(function(event) {
        textbox.addEventListener(event, function(e) {
            if (!inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = '';
            }
        });
    });
};

// let xorArr = []
// for (let word of wordFrequency) {
//     if (!wordList.includes(word)) {
//         xorArr.push(word)
//     }
// }
// console.log(xorArr)
// logTime()


const wordList = fullWordList

const playingMatInput = document.querySelector('#playing-mat-input')
const resourcesInput = document.querySelector('#resources-input')
const requiredInput = document.querySelector('#required-input')
const forbiddenInput = document.querySelector('#forbidden-input')
const lettersInput = document.querySelector('#letters-input')
const wildInput = document.querySelector('#wild-input')
const transferInput = document.querySelector('#transfer-input')
const transferFrom = transferInput.children[0]
const transferTo = transferInput.children[2]
const inputsArr1 = [
    playingMatInput, resourcesInput, requiredInput, forbiddenInput, wildInput
]
const inputsArr2 = [
    transferFrom, transferTo
]
for (const input of inputsArr1) {
    setInputFilter(input, (value) => /[^A-Za-z ,]/.test(value))
}
for (const input of inputsArr2) {
    setInputFilter(input, (value) => /[^A-Za-z]/.test(value))
}
setInputFilter(lettersInput, (value) => /[^0-9]/.test(value))
const doubleConsonantToggle = document.querySelector('#double-consonant .toggle');
const doubleVowelToggle = document.querySelector('#double-vowel .toggle');
doubleConsonantToggle.addEventListener('click', function() {
    this.classList.toggle('active')
})
doubleVowelToggle.addEventListener('click', function() {
    this.classList.toggle('active')
})
const submitButton = document.querySelector('#submit')
const answerContainer = document.querySelector('#answer-container')

submitButton.addEventListener('click', submitinput)

function submitinput() {

    answerContainer.innerHTML = ''

    function filterWordList({
        wordList,
        letters,
        requiredLetters = [],
        excludedLetters = [],
        doubleConsonant = false,
        doubleVowel = false,
        requiredLength = NaN
    }) {
    
        const isVowel = char => 'aeiou'.includes(char.toLowerCase());
        const hasDouble = (word, condition) => {
            for (let i = 0; i < word.length - 1; i++) {
                if (word[i] === word[i + 1] && condition(word[i])) {
                    return true;
                }
            }
            return false;
        };
        
        const letterCounts = letters.reduce((acc, letter) => {
            acc[letter] = (acc[letter] || 0) + 1;
            return acc;
        }, {});

        const wildcardCount = letterCounts['*'] || 0;
        delete letterCounts['*']; // Remove wildcard entry for letter checks

        return wordList.filter(word => {
            // Check for required and excluded letters
            if (!isNaN(requiredLength) && word.length !== requiredLength) return false;
            if (requiredLetters.some(letter => !word.includes(letter)) || excludedLetters.some(letter => word.includes(letter))) {
                return false;
            }
    
            // Check for double consonant and/or double vowel
            if (doubleConsonant && !hasDouble(word, char => !isVowel(char))) return false;
            if (doubleVowel && !hasDouble(word, isVowel)) return false;
            if (doubleConsonant && doubleVowel && !(hasDouble(word, char => !isVowel(char)) && hasDouble(word, isVowel))) return false;
    
            let tempWildcardCount = wildcardCount;
            const wordLetterCounts = [...word].reduce((acc, char) => {
                acc[char] = (acc[char] || 0) + 1;
                return acc;
            }, {});
  
            for (let char of Object.keys(wordLetterCounts)) {
                const required = wordLetterCounts[char];
                const available = letterCounts[char] || 0;
                
                if (required > available) {
                    tempWildcardCount -= required - available;
                    if (tempWildcardCount < 0) return false; // Not enough wildcards to cover the deficit
                }
            }
            return true;
        });
    }
    function calcRequiredDelta(words, subsetLetters) {
        // Initialize a map to store words by their additional letters needed
        const wordsByAdditionalLettersNeeded = new Map();
    
        words.forEach(word => {
        // Calculate the additional letters needed for each word
        const additionalLettersNeeded = calcAdditionalLetters(word, subsetLetters);
    
        // If the key does not exist in the map, initialize it with an empty array
        if (!wordsByAdditionalLettersNeeded.has(additionalLettersNeeded)) {
            wordsByAdditionalLettersNeeded.set(additionalLettersNeeded, []);
        }

        // Add the word to the appropriate array in the map
        wordsByAdditionalLettersNeeded.get(additionalLettersNeeded).push(word);
        });
    
        return wordsByAdditionalLettersNeeded;
    }
    function calcAdditionalLetters(word, subsetLetters) {
    
        const subsetCounts = subsetLetters.reduce((acc, letter) => {
            acc[letter] = (acc[letter] || 0) + 1;
            return acc;
        }, {});
    
        const wordCounts = [...word].reduce((acc, char) => {
            acc[char] = (acc[char] || 0) + 1;
            return acc;
        }, {});
    
        let additionalLettersNeeded = 0;
        let availableWildcards = subsetCounts['*'] || 0;
    
        for (let [char, required] of Object.entries(wordCounts)) {
            const available = subsetCounts[char] || 0;
            const deficit = required - available;
            
            if (deficit > 0) {
                if (availableWildcards >= deficit) {
                    availableWildcards -= deficit;
                } else {
                    additionalLettersNeeded += deficit - availableWildcards;
                    availableWildcards = 0;
                }
            }
        }
    
        return additionalLettersNeeded;
    }
    function inputToArr(input) {
        return input.value.toLowerCase().split('').filter(value => /[a-z]/.test(value))
    }
    let playingMat = inputToArr(playingMatInput)
    let resources = inputToArr(resourcesInput).concat(playingMat)
    let required = inputToArr(requiredInput)
    let forbidden = inputToArr(forbiddenInput)
    // Number of Letters
    let letters = parseInt(lettersInput.value)
    console.log(letters)
    // Wild
    let wild = inputToArr(wildInput)
    for (let letter of wild) {
        if (playingMat.includes(letter)) {
            deleteFirstArrItem(playingMat, letter)
            playingMat.push('*')
        }
        if (resources.includes(letter)) {
            deleteFirstArrItem(resources, letter)
            resources.push('*')
        }
    }
    // Letter transfer
    if (transferFrom.value) {
        for (let container of [playingMat, resources, required, forbidden]) {
            for (let i = 0; i < container.length; i++) {
                if (container[i] === transferFrom.value) {
                    container[i] = transferTo.value
                }
            }
        }
        forbidden.push(transferFrom.value)
    }
    let doubleConsonantActive = doubleConsonantToggle.classList.contains('active')
    let doubleVowelActive = doubleVowelToggle.classList.contains('active')

    console.log("Playing Mat: ", playingMat)
    console.log("Resources: ", resources)
    console.log("Required: ", required)
    console.log("Forbidden: ", forbidden)
    console.log("Number of Letters: ", letters)
    console.log("Wild: ", wild)
    console.log(`Transfer ${transferFrom.value} to ${transferTo.value}`)
    console.log("Double Consonant: ", doubleConsonantActive)
    console.log("Double Vowel", doubleVowelActive)

    const filteredWords = filterWordList({
        wordList: wordList,
        letters: resources,
        requiredLetters: required,
        excludedLetters: forbidden,
        doubleConsonant: doubleConsonantActive,
        doubleVowel: doubleVowelActive,
        requiredLength: letters
    });

    console.log(filteredWords);
    const additionalLettersMap = calcRequiredDelta(filteredWords, playingMat);
    const additionalLettersMapObj = Object.fromEntries(additionalLettersMap);
    console.log(additionalLettersMapObj);

    for (let letter in additionalLettersMapObj) {
        console.log(letter)
        let words = additionalLettersMapObj[letter]
        const newHeader = document.createElement('p')
        newHeader.classList.add('header')
        newHeader.innerText = `Letters from Resources: ${letter}`
        answerContainer.append(newHeader)
        for (let word of words) {
            const newWord = document.createElement('p')
            newWord.innerText = word
            answerContainer.append(newWord)
        }
    }

    let fadeDelay = 1
    setTimeout(() => {fadeMethod()}, 150 * fadeDelay)
    function fadeMethod() {
        const element = document.querySelector('#answer-container > p:not(.show)')
        if (!element) return;
        setTimeout(function(){
            element.classList.add('show')
            fadeMethod()
        }, 40 * fadeDelay)
    }  
}