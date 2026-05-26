from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.excel import router as excel_router

app = FastAPI(title="ProyectoUno")

app.include_router(excel_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProyectoUno</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, sans-serif; background: #f5f7fa; padding: 2rem; color: #333; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { margin-bottom: 1.5rem; }
        .card { background: #fff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
        .card h2 { font-size: 1.1rem; margin-bottom: 1rem; }
        input[type=file] { display: block; margin-bottom: .75rem; }
        button { background: #2563eb; color: #fff; border: none; padding: .5rem 1rem; border-radius: 6px; cursor: pointer; }
        button:hover { background: #1d4ed8; }
        .msg { margin-top: .75rem; padding: .5rem; border-radius: 6px; display: none; }
        .msg.error { background: #fee2e2; color: #991b1b; display: block; }
        .msg.success { background: #dcfce7; color: #166534; display: block; }
        table { width: 100%; border-collapse: collapse; }
        th, td { text-align: left; padding: .5rem; border-bottom: 1px solid #e5e7eb; }
        th { background: #f9fafb; font-weight: 600; }
        tr:hover td { background: #f9fafb; }
        .empty { color: #9ca3af; text-align: center; padding: 2rem; }
        .loading { color: #6b7280; text-align: center; padding: 1rem; }
    </style>
</head>
<body>
<div class="container">
    <h1>ProyectoUno</h1>

    <div class="card">
        <h2>Subir archivo Excel</h2>
        <input type="file" id="fileInput" accept=".xlsx">
        <button onclick="uploadFile()">Subir</button>
        <div id="uploadMsg" class="msg"></div>
    </div>

    <div class="card">
        <h2>Datos cargados</h2>
        <div id="loadingState" class="loading">Cargando...</div>
        <div id="emptyState" class="empty" style="display:none;">No hay datos. Sube un archivo Excel.</div>
        <div id="tableWrapper" style="display:none;">
            <table>
                <thead><tr><th>Nombre</th><th>Correo</th><th>Nota</th></tr></thead>
                <tbody id="dataBody"></tbody>
            </table>
        </div>
    </div>
</div>

<script>
async function loadData() {
    try {
        const resp = await fetch('/uploads');
        const json = await resp.json();
        const tbody = document.getElementById('dataBody');
        tbody.innerHTML = '';
        document.getElementById('loadingState').style.display = 'none';
        if (json.data.length === 0) {
            document.getElementById('emptyState').style.display = 'block';
            document.getElementById('tableWrapper').style.display = 'none';
        } else {
            document.getElementById('emptyState').style.display = 'none';
            document.getElementById('tableWrapper').style.display = 'block';
            json.data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${row.nombre}</td><td>${row.correo}</td><td>${row.nota}</td>`;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        document.getElementById('loadingState').textContent = 'Error al cargar datos.';
    }
}

async function uploadFile() {
    const input = document.getElementById('fileInput');
    const msg = document.getElementById('uploadMsg');
    msg.className = 'msg';
    msg.style.display = 'none';
    if (!input.files.length) { msg.textContent = 'Selecciona un archivo.'; msg.className = 'msg error'; msg.style.display = 'block'; return; }
    const form = new FormData();
    form.append('file', input.files[0]);
    try {
        const resp = await fetch('/upload-excel', { method: 'POST', body: form });
        if (!resp.ok) {
            const err = await resp.json();
            msg.textContent = err.detail || 'Error al subir archivo.';
            msg.className = 'msg error';
        } else {
            msg.textContent = 'Archivo subido correctamente.';
            msg.className = 'msg success';
            input.value = '';
            loadData();
        }
    } catch (e) {
        msg.textContent = 'Error de conexión.';
        msg.className = 'msg error';
    }
    msg.style.display = 'block';
}

loadData();
</script>
</body>
</html>
    """
