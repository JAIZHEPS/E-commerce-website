
function copyBill() {
    const bill = document.getElementById('bill-summary');
    if (bill) {
        const range = document.createRange();
        range.selectNode(bill);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        try {
            document.execCommand('copy');
            alert('Bill copied to clipboard!');
        } catch (err) {
            alert('Failed to copy bill.');
        }
        window.getSelection().removeAllRanges();
    }
}

function screenshotBill() {
    if (typeof html2canvas === 'undefined') {
        alert('Screenshot feature requires html2canvas. Please include it.');
        return;
    }
    const bill = document.getElementById('bill-summary');
    html2canvas(bill).then(canvas => {
        const link = document.createElement('a');
        link.download = 'bill.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}