function printReceipt() {
    if (Object.keys(cart).length === 0) {
        alert("No hay productos para imprimir.");
        return;
    }

    const productList = [];

    for (const code in cart) {
        const item = cart[code];
        const quantity = item.quantity || 1;
        const price = item.price || 0;

        productList.push({
            name: item.name,
            quantity: quantity,
            price: price
        });
    }

    const encodedData = encodeURIComponent(JSON.stringify(productList));
    window.open(`print/showPDF.html?productsList=${encodedData}`, "_blank");
}
