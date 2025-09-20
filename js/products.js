let products = {};

async function loadProducts() {
  try {
    const res = await fetch("/productos_dict");
    products = await res.json();
    console.log("✅ Productos cargados desde la base:", products);
  } catch (err) {
    console.error("Error cargando productos:", err);
  }
}

loadProducts();
