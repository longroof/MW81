// 0秒後にも実行させる
getCurrentTime();

// 毎秒実行させるタイマーをセット
setInterval(getCurrentTime, 1 * 1000);

function getCurrentTime() {
    // Dateオブジェクトを代入
    const date = new Date();

    // Dateオブジェクトから年、月、日を取り出すメソッドを実行して代入
    const yearString = date.getFullYear();
    const monthString = date.getMonth() + 1;
    const dateString = date.getDate();

    // 時間、分、秒を取り出して代入
    const hourString = ('0' + date.getHours()).slice(-2);
    const minuteString = String(date.getMinutes()).padStart(2,0);
    const secondString = to2Digit(date.getSeconds());

    // 年月日（曜日）時分秒を結合して、1行でコンソールに出力する
    const dayList = ['(日)', '(月)', '(火)', '(水)', '(木)', '(金)', '(土)',];
    const dayString = dayList[date.getDay()];
    const dateTimeString = yearString + '年' + monthString + '月' + dateString + '日' +
        dayString + hourString + '時' + minuteString + '分' + secondString + '秒';

    // HTML上に表示させる
    document.getElementById('currentTime').textContent = dateTimeString;
}

function to2Digit(num) {
    if (num > 9) {
        return num;
    } else {
        return '0' + num;
    }
}

function messageToConsole(message) {
    console.log(message);
}

// clickBtn3を取得する
const clickBtn3 = document.getElementById('clickBtn3');

// clickBtnにクリックイベントを付与して、イベント発火時の処理をまとめる
clickBtn3.addEventListener('click', function() {
    console.log('クリック3ボタンがクリックされました！');
    clickBtn3.textContent = "クリックされたクリック3";
})