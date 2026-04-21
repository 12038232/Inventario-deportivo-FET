const API = "http://127.0.0.1:5000/api/productos/";

// 🔄 Cargar productos
async function cargarProductos() {
    const res = await fetch(API);
    const data = await res.json();

    const tbody = document.querySelector("#tabla tbody");
    tbody.innerHTML = "";

    data.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.nombre_producto}</td>
                <td>${p.stock}</td>
                <td>${p.precio}</td>
            </tr>
        `;
    });
}

cargarProductos();