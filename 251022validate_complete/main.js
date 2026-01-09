// 251022入力検証
// 検証ボタンがクリックされたら実行する処理
document.getElementById('validateButton').addEventListener('click', event => {
    event.preventDefault();
    // アラートメッセージを配列に格納する
    const alertMessage = [];

    // すべてのinputタグを取得して、入力値を共通関数へ送り、戻り値を受け取る
    document.querySelectorAll('input').forEach(element => {
        if (element.value) {
            return alertMessage.push(checkUserInputValue(checkValueItem[element.id].item,element.value,checkValueItem[element.id].pattern));
        }
        else alertMessage.push(element.placeholder);
    })

    // alertMessageに1行でも出力があればアラートを出力(配列.join()で文字列に変換し、('\n')で項目ごと改行)
    if (alertMessage.length) alert(alertMessage.join('\n'));
}, false);

// 共通入力チェック、パターンチェック関数
function checkUserInputValue(item, value, pattern) {
    if (value.match(pattern)) console.log(`${item}が正しく入力されました。:(${value})`)
    else return `${item}を正しく入力し直してください。:(${value})`
}

// ID、項目名、パターンのオブジェクト
const checkValueItem = {
    userName: { item: "お名前", pattern: /^[\u30a0-\u30ff\u3040-\u309f\u3005-\u3006\u30e0-\u9fcf 　]{1,25}$/ },
    userId: { item: "ユーザーID", pattern: /^[a-z0-9]{8,12}$/ },
    userMail: { item: "メールアドレス", pattern: /^[a-zA-Z0-9_+-]+(.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/ },
    userZip: { item: "郵便番号", pattern: /^[0-9{3}]-?[0-9]{4}$/ },
    userTel: { item: "電話番号", pattern: /^[0-9]{3}-?[0-9]{4}-?[0-9]{4}||[0-9]{3}-?[0-9]{3}-?[0-9]{4}$/ },
}