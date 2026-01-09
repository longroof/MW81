// 251027入力検証
// 検証ボタンがクリックされたら実行する処理
document.getElementById('validateButton').addEventListener('click', event => {
    event.preventDefault();
    // アラートメッセージを一つにまとめる: 配列にエラーメッセージを追加する
    const errorMessages = [];

    // すべてのinputタグに入力されたvalueを取り出して検証する
    const inputs = document.querySelectorAll('input');
    for (let input of inputs) {
        // 入力値が1文字以上ある場合は共通関数に渡す 
        if (input.value) {
            const error = validateInputValue(checkPattern[input.id].item, input.value, checkPattern[input.id].pattern);
            if (error) errorMessages.push(error);
        }
        //  入力値が0文字もしくはnullの場合のエラーメッセージ
        else {
            errorMessages.push(`${input.placeholder}`);
        }
    }

    if (errorMessages.length) alert(errorMessages.join('\n'));  // [].joinで文字列に結合
}, false);

// 入力値を検証する共通関数
function validateInputValue(name, value, patt) {
    if (value.match(patt)) console.log(`${name}が正しく入力されました。: (${value})`);
    // else return `${name}を正しく入力し直してください: (${value})`;
    else return name + 'を正しく入力し直してください: (' + value + ')';
}

// お名前とパターンの組合せオブジェクト
const checkPattern = {
    userName: { item: "お名前", pattern: /^[\u30a0-\u30ff\u3040-\u309f\u3005-\u3006\u30e0-\u9fcf 　]{1,25}$/ },
    userId: { item: "ユーザーID", pattern: /^[0-9a-z]{8,12}$/ },
    userMail: { item: "メールアドレス", pattern: /@/ },
    userZip: { item: "郵便番号", pattern: /^[0-9]{3}-?[0-9]{4}$/ },
    userTel: { item: "電話番号", pattern: /^0[0-9]0-?[0-9]{4}-?[0-9]{4}$/ },
}