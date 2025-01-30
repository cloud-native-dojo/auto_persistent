// script.js
document.addEventListener('DOMContentLoaded', () => {
    const progressBar = document.getElementById('downloadProgress');
    let downloadValue = 0;

    // ダウンロードのシミュレーション
    const downloadInterval = setInterval(() => {
        if (downloadValue <100 ) {
            downloadValue += 1; // 進行状況を更新
            progressBar.value = downloadValue;
        } else {
            clearInterval(downloadInterval); // ダウンロード完了
            alert('ダウンロード完了');
        }
    }, 100); // 100msごとに進行状況を1%増加
});

