document.addEventListener('DOMContentLoaded', () => {
    // let randomNumber = Math.floor(Math.random() * 100) + 1;
    let randomNumber = returnRandomNumber();
    const guesses = document.querySelector('.guesses');
    const lastResult = document.querySelector('.lastResult');
    const lowOrHi = document.querySelector('.lowOrHi');
    const guessSubmit = document.querySelector('.guessSubmit');
    const guessField = document.querySelector('.guessField');

    let guessCount = 1;
    let resetButton;

    function checkGuess() {

        const userGuess = Number(guessField.value);
        if (guessCount === 1) {
            guesses.textContent = 'これまでの数字: ';
        }
        guesses.textContent += userGuess + ' ';

        if (userGuess === randomNumber) {
            lastResult.textContent = 'おめでとう！正解です！！';
            lastResult.style.backgroundColor = 'green';
            lowOrHi.textContent = '';
            setGameOver();
        } else if (guessCount === 10) {
            lastResult.textContent = '!!!ゲームオーバー!!!';
            setGameOver();
        } else {
            lastResult.textContent = 'はずれ！';
            lastResult.style.backgroundColor = 'red';
            if (userGuess < randomNumber) {
                lowOrHi.textContent = '小さいねぇ';
            } else if (userGuess > randomNumber) {
                lowOrHi.textContent = '大きいよ！';
            }
        }

        guessCount++;
        guessField.value = '';
        guessField.focus();
    }
    // guessSubmit.addeventListener('click', checkGuess);
    guessSubmit.addEventListener('click', checkGuess);

    function setGameOver() {
        guessField.disabled = true;
        guessSubmit.disabled = true;
        resetButton = document.createElement('button');
        resetButton.textContent = 'ゲームリセット';
        document.body.appendChild(resetButton);
        resetButton.addEventListener('click', resetGame);
    }

    function resetGame() {
        guessCount = 1;

        const resetParas = document.querySelectorAll('.resultParas p');
        for (const resetPara of resetParas) {
            resetPara.textContent = '';
        }
        resetButton.parentNode.removeChild(resetButton);

        guessField.disabled = false;
        guessSubmit.disabled = false;
        guessField.value = '';
        guessField.focus();

        lastResult.style.backgroundColor = 'white';

        // randomNumber = Math.floor(Math.random()) + 1;
        randomNumber = returnRandomNumber();
    }
})

function returnRandomNumber() {
    const num = Math.floor(Math.random() * 100) + 1;
    console.log(num);
    return num;
}