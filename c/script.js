
let cart = {};
let manualCounter = 1;

const formatCOP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
});

document.getElementById("barcode-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        const code = this.value.trim();
        if (products[code]) {
            const product = products[code];
            if (cart[code]) {
                cart[code].quantity += 1;
            } else {
                cart[code] = { ...product, quantity: 1 };
            }
            updateCart();
        } else {
            alert("Producto no encontrado.");
        }
        this.value = "";
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

    const code = `manual-${manualCounter++}`;
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
        row.innerHTML = `
 <td class="product-cell">
  <button class="delete-btn" onclick="removeItem('${code}')">❌</button>
  <span>${item.name}</span>
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

    totalSpan.innerText = `Total: ${formatCOP.format(totalFinal)}`;
    countSpan.innerText = `${itemCount} artículo${itemCount !== 1 ? 's' : ''}`;
}


function checkout() {
    if (Object.keys(cart).length === 0) {
        alert("No hay productos ingresados");
        return;
    }
    alert("Compra realizada");
    cart = {};
    updateCart();
}
