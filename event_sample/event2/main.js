// DOMの解析が完了してから実行する
document.addEventListener('DOMContentLoaded', () => {
    // canvasの取得とcanvas内描画準備
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    // 黒丸描画関数
    function drawCircle(x, y, size) {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.beginPath();
        ctx.fillStyle = 'black';
        ctx.arc(x, y, size, 0, 2 * Math.PI);
        ctx.fill();
    }

    // x座標，y座標，直径で黒丸を描画
    let x = 50;
    let y = 50;
    let size = 30;
    drawCircle(x, y, size);

    /*
    キーダウンイベントを取得して、Wキーの場合上へ、Sキーの場合下へ、
    Aキーの場合左へ、Dキーの場合右へ黒丸を移動させてください。
    */
    document.addEventListener('keydown', e => {
        // canvasを超えない
        // if (e.key == "w" && y > 30) y -= 10; 
        // コード追加ここから
        // if (e.key == "s" && y < 290) y += 10;
        // if (e.key == "a" && x > 30) x -= 10;
        // if (e.key == "d" && x < 450) x += 10;

        // canvasから消えたら反対から出現
        if (e.key == "w") {
            if (y <= -30) y = 350;
            y -= 10;
        }
        if (e.key == "s") {
            if (y >= 350) y = -30;
            y += 10;
        }
        if (e.key == "a") {
            if (x <= -30) x = 510;
            x -= 10;
        }
        if (e.key == "d") {
            if (x >= 510) x = -30;
            x += 10;
        }

        drawCircle(x, y, size);
        console.log(`x: ${x}, y: ${y}, size: ${size}`);
    })

})
