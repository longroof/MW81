// DOMの解析が完了してから実行する
document.addEventListener('DOMContentLoaded', () => {
    /*
      各色のボタンをクリックしたら、その色の背景色に変更してください。
      背景色の指定方法「document.body.style.backgroundColor = 'red'」
      各色idのボタンを使用する方法が成功したら、
      ボタン要素を集合体として取得して、value値の色の名前で処理を切り替えてみましょう。
    */
    // 各色ボタンの取得
    // const btn_red = document.getElementById('red');
    // const btn_blue = document.getElementById('blue');
    // const btn_yellow = document.getElementById('yellow');
    // const btn_green = document.getElementById('green');

    // ボタンにクリックイベントを追加して背景色を変える
    // 赤ボタンクリック時の処理
    // btn_red.addEventListener('click', () => document.body.style.backgroundColor = 'red');
    // コード追加ここから
    // btn_blue.addEventListener('click', () => document.body.style.backgroundColor = 'red');
    // btn_yellow.addEventListener('click', () => document.body.style.backgroundColor = 'yellow');
    // btn_green.addEventListener('click', () => document.body.style.backgroundColor = 'green');

    // inputタグの集合体を取得、クリックされたボタンidで背景色変更
    const btns = document.querySelectorAll('input');
    for (let btn of btns) {
      btn.addEventListener('click', () => document.body.style.backgroundColor = btn.id);
    }
})
