// 251022入力検証
// 検証ボタンがクリックされたら実行する処理
document.getElementById('validateButton').addEventListener('click', event => {
    event.preventDefault();
    // アラートメッセージを一つにまとめる: 配列にエラーメッセージを追加する
    const errorMessages = [];

    // お名前欄の入力値を取得する
    const userNameValue = document.getElementById('userName').value;
    if (userNameValue) {
        if (validateName(userNameValue)) {
            errorMessages.push(validateName(userNameValue));
        }
    }
    // else alert('お名前欄が入力されていません。');
    else errorMessages.push('お名前欄が入力されていません。');

    // ユーザーID欄の入力値を取得する
    const userIdValue = document.getElementById('userId').value;
    if (userIdValue) {
        if (validateId(userIdValue)) {
            errorMessages.push(validateId(userIdValue));
        }
    }
    // else alert('ユーザーID欄が入力されていません。');
    else errorMessages.push('ユーザーID欄が入力されていません。');

    // メールアドレス欄の入力値を取得する
    const userMailValue = document.getElementById('userMail').value;
    if (userMailValue) {
        if (validateMail(userMailValue)) {
            errorMessages.push(validateMail(userMailValue));
        }
    }
    // else alert('メールアドレス欄が入力されていません。');
    else errorMessages.push('メールアドレス欄が入力されていません。');

    // エラーメッセージの確認
    if (errorMessages.length) console.log(errorMessages);   // 配列をコンソール出力
    if (errorMessages.length) console.log(errorMessages.join('\n'));  // [].joinで文字列に結合
    if (errorMessages.length) alert(errorMessages.join('\n'));  // [].joinで文字列に結合

    // 郵便番号欄の入力値を取得する
    const userZipValue = document.getElementById('userZip').value;
    // if (userZipValue) validateZip(userZipValue);
    // else alert('郵便番号欄が入力されていません。');

    // 電話番号欄の入力値を取得する
    const userTelValue = document.getElementById('userTel').value;
    // if (userTelValue) validateTel(userTelValue);
    // else alert('電話番号欄が入力されていません。');

}, false);

// お名前の入力値を検証する関数 /^[\u30a0-\u30ff\u3040-\u309f\u3005-\u3006\u30e0-\u9fcf 　]{1,25}$/
function validateName(name) {
    if (name.length && name.match(/^[\u30a0-\u30ff\u3040-\u309f\u3005-\u3006\u30e0-\u9fcf 　]{1,25}$/)) console.log('お名前欄が正しく入力されました。');
    // else alert(`お名前を正しく入力し直してください：${name}`);
    else {
        return `お名前を正しく入力し直してください：${name}`;
    };
}

// ユーザーID欄の入力値を検証する関数 /^[a-z0-9]{8,12}$/
function validateId(id) {
    if (id.length && id.match(/^[a-z0-9]{8,12}$/)) console.log('ユーザーID欄が正しく入力されました。');
    // else alert(`ユーザーID欄を正しく入力し直してください。：${id}`)  // [`(バックスラッシュShift + @)]
    else {
        return `ユーザーID欄を正しく入力し直してください。：${id}`;
    }
}

// メールアドレス欄の入力値を検証する関数 ^[a-zA-Z0-9_+-]+(.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$
function validateMail(mail) {
    if (mail.length && mail.match(/^[a-zA-Z0-9_+-]+(.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/)) console.log('メールアドレス欄が正しく入力されました。');
    // else alert(`メールアドレス欄を正しく入力し直してください。:${mail}`);
    else {
        return `メールアドレス欄を正しく入力し直してください。:${mail}`;
    }
}

// 郵便番号欄の入力値を検証する関数 ^[0-9]{3}-?[0-9]{4}$
function validateZip(zip) {
    if (zip.length && zip.match(/^[0-9]{3}-?[0-9]{4}$/)) console.log('郵便番号欄が正しく入力されました。');
    else alert(`郵便番号欄を正しく入力し直してください。:${zip}`);
}

// 電話番号欄の入力値を検証する関数 ^[0-9]{3}-?[0-9]{4}-?[0-9]{4}||[0-9]{3}-?[0-9]{3}-?[0-9]{4}$
function validateTel(tel) {
    if (tel.length && tel.match(/^(0[5-9]0[-(]?[0-9]{4}[-)]?[0-9]{4}|0120[-]?\d{1,3}[-]?\d{4}|050[-]?\d{4}[-]?\d{4}|0[1-9][-]?\d{1,4}[-]?\d{1,4}[-]?\d{4})*$/)) console.log('電話番号欄が正しく入力されました。');
    else alert(`電話番号欄を正しく入力し直してください。:${tel}`);
}
