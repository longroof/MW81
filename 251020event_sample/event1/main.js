// DOMの解析が完了してから実行する
document.addEventListener('DOMContentLoaded', () => {
  // ボタンの取得
  const btn = document.getElementById('machine_power');
  // マシン状態テキストの取得
  const txt = document.getElementById('machine_status');
  // マシン状態bool値の定義
  let machineStatusBool = false;

  /*
     「スタート」ボタンをクリックしたら、
     「マシーンは起動しています。」にテキストが変更し、
     ボタンの文字列は「ストップ」に変更してください。
     「ストップ」ボタンをクリックしたら、
     「マシーンは停止しています。」にテキストが変更し、
     ボタンの文字列は「スタート」に変更してください。
   */
  // コード追加ここから
  // btnがクリックされたら実行される処理
  btn.addEventListener('click', function () {
    if (!machineStatusBool) {
      // 「スタート」ボタンをクリックした時の処理
      txt.textContent = 'マシーンは起動しています。';
      btn.value = 'ストップ';
      machineStatusBool = true;
    } else {
      // 「ストップ」ボタンをクリックした時の処理
      txt.textContent = 'マシーンは停止しています。';
      btn.value = 'スタート';
      machineStatusBool = false;
    }

  })

})
