
let cart = {};
let manualCounter = 1;

const formatCOP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
});

document.getElementById("barcode-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        const input = this.value.trim();
        this.value = "";

        let product = null;
        let matchedCode = null;

        if (/^\d/.test(input)) {
            // Barcode
            for (let key in products) {
                const p = products[key];

                if (Array.isArray(p.barcodes) && p.barcodes.includes(input)) {
                    product = p;
                    matchedCode = key;
                    break;
                } else if (p.barcode === input) {
                    product = p;
                    matchedCode = key;
                    break;
                }
            }
        } else {
           
            product = products[input];
            matchedCode = input;
        }

        if (product) {
            addItemToCart(product, matchedCode);
        } else {
            alert("Producto no encontrado");
        }
    }
});


function toggleManualForm() {
    const form = document.getElementById("manual-form");
    const isHidden = window.getComputedStyle(form).display === "none";
    form.style.display = isHidden ? "block" : "none";
}

function addManualItem() {
    const name = document.getElementById("manual-name").value.trim();
    const price = parseFloat(document.getElementById("manual-price").value);
    const ivaPercent = parseFloat(document.getElementById("manual-iva").value);

    if (!name || isNaN(price) || price <= 0 || isNaN(ivaPercent) || ivaPercent < 0) {
        alert("Ingrese un nombre, un precio y un IVA válido.");
        return;
    }

    const code = `m${manualCounter++}`;
    cart[code] = { name, price, iva: ivaPercent, quantity: 1 };
    updateCart();

    document.getElementById("manual-name").value = "";
    document.getElementById("manual-price").value = "";
    document.getElementById("manual-iva").value = "19";
    toggleManualForm();
}

function changeQuantity(code, delta) {
    if (!cart[code]) return;
    cart[code].quantity += delta;
    if (cart[code].quantity <= 0) {
        delete cart[code];
    }
    updateCart();
}

function removeItem(code) {
    delete cart[code];
    updateCart();
}

function updateCart() {
    const tbody = document.getElementById("cart-body");
    const totalSpan = document.getElementById("total");
    const countSpan = document.getElementById("item-count");

    tbody.innerHTML = "";
    let totalFinal = 0;
    let itemCount = 0;

    for (const code in cart) {
        const item = cart[code];
        const qty = item.quantity;
        const hasValidIVA = typeof item.iva === "number" && !isNaN(item.iva);
        const ivaRate = hasValidIVA ? item.iva : 0;


        const conIVAUnidad = item.price;
        const sinIVAUnidad = ivaRate > 0 ? conIVAUnidad / (1 + ivaRate / 100) : conIVAUnidad;


        const totalConIVA = conIVAUnidad * qty;

        itemCount += qty;
        totalFinal += totalConIVA;

        const row = document.createElement("tr");
        console.log(code);

        row.innerHTML = `
 <td class="product-cell">
  <button class="delete-btn" onclick="removeItem('${code}')">❌</button>
  <span>${" <b> " + code + " </b> <br>" + item.name}</span>
</td>

      <td>
        <div class="quantity-controls">
          <button class="arrow-btn" onclick="changeQuantity('${code}', 1)">🔼</button>
          <span>${qty}</span>
          <button class="arrow-btn" onclick="changeQuantity('${code}', -1)">🔽</button>
        </div>
      </td>
      <td>${formatCOP.format(sinIVAUnidad)}</td>
      <td>${formatCOP.format(conIVAUnidad)}</td>
      <td>${formatCOP.format(totalConIVA)}</td>
    `;

        tbody.appendChild(row);
    }

    totalSpan.innerText = `Suma Total: ${formatCOP.format(totalFinal)}`;
    countSpan.innerText = `${itemCount} artículo${itemCount !== 1 ? 's' : ''}`;
}


function calculateTotal() {
    let total = 0;
    const rows = document.querySelectorAll("#cart-body tr");

    rows.forEach(row => {
        const totalCell = row.querySelector("td:last-child");
        if (totalCell) {
            // Remove $ and dots, convert to number
            const value = parseFloat(totalCell.textContent.replace(/[^\d]/g, ""));
            if (!isNaN(value)) {
                total += value;
            }
        }
    });

    return total;
}

function checkout() {
    const total = calculateTotal(); 
    const data = encodeURIComponent(JSON.stringify({ total }));
    window.open(`r.html?data=${data}`, 'popup', 'width=500,height=600');
}


window.addEventListener("message", function (event) {
    if (event.data?.type === "finalizarCompra") {
        const confirmPrint = confirm("¿Desea imprimir el recibo?");

        if (confirmPrint) {
            document.body.querySelector("#btn-print").click()
            
        }

        
        location.reload();
    }
});

function clearCart() {
    location.reload();
}


function addItemToCart(product, inputCode = null) {

    let existingCode = null;


    for (const code in cart) {
        if (code === inputCode) {
            existingCode = code;
            break;
        }
    }

    if (existingCode) {
        cart[existingCode].quantity += 1;
    } else {

        const code = inputCode;

        cart[code] = {
            name: product.name,
            price: product.price,
            iva: product.iva,
            quantity: 1
        };
    }

    updateCart();

    const lastScanned = document.getElementById("last-scanned");


    const barcodeDisplay = product.barcodes ? ` | Códigos: ${product.barcodes.join(", ")}` :
        product.barcode ? ` | Código: ${product.barcode}` : "";

    lastScanned.textContent = `Último producto: ${inputCode}${barcodeDisplay} | ${product.name} | Precio: ${formatCOP.format(product.price)}`;
    lastScanned.className = lastScanned.className === "green" ? "red" : "green";

}
