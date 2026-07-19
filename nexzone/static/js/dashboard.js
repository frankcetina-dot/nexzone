let contentData = [];
let usersData = [];
let currentEditId = null;
let currentEditUserId = null;
let currentFilter = 'all';
let currentPlayingId = null;

async function loadContentFromAPI() {
    try {
        const response = await fetch('/dashboard/api/content');
        contentData = await response.json();
        renderTable();
        updateTopPlays();
        updateStats();
    } catch (error) {
        console.error("Error cargando contenido:", error);
    }
}

function renderTable(filteredData = null) {
    const tbody = document.getElementById('content-table-body');
    if (!tbody) return;

    tbody.innerHTML = '';
    let dataToRender = filteredData || contentData;

    if (currentFilter !== 'all') {
        dataToRender = dataToRender.filter(item => item.type === currentFilter);
    }

    if (dataToRender.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="px-6 py-8 text-center text-zinc-500">No se encontraron resultados.</td></tr>`;
        return;
    }

    dataToRender.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'table-row border-b border-zinc-800';

        const statusColor = item.status === 'Publicado'
            ? 'bg-emerald-500/10 text-emerald-400'
            : item.status === 'Borrador'
                ? 'bg-amber-500/10 text-amber-400'
                : 'bg-red-500/10 text-red-400';

        tr.innerHTML = `
            <td class="py-3 pl-6">
                <div class="flex items-center gap-x-3">
                    <div class="w-16 h-9 bg-zinc-900 rounded-xl overflow-hidden border border-zinc-700 flex-shrink-0">
                        <img src="${item.thumb}" class="content-thumb w-full h-full object-cover" alt="${item.title}">
                    </div>
                    <div class="font-medium pr-4">${item.title}</div>
                </div>
            </td>
            <td class="py-3 text-zinc-300 tabular-nums">${item.duration || '—'}</td>
            <td class="py-3">
                <span class="inline-block px-3 py-0.5 text-xs rounded-full font-medium ${statusColor}">
                    ${item.status}
                </span>
            </td>
            <td class="py-3 text-right font-medium tabular-nums text-emerald-400 pr-6">${item.plays || 0}</td>
            <td class="py-3 text-center">
                <button onclick="playVideo(${item.id}, event)"
                        class="px-3 py-1 text-xs rounded-xl bg-[#e50914]/10 hover:bg-[#e50914]/20 text-[#e50914] transition-colors flex items-center gap-x-1 mx-auto">
                    <i class="fa-solid fa-play mr-1"></i>
                    <span>Reproducir</span>
                </button>
            </td>
            <td class="py-3 pr-6">
                <div class="flex items-center justify-center gap-x-1">
                    <button onclick="openEditModal(${item.id})"
                            class="px-3 py-1 text-xs rounded-xl hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors">
                        <i class="fa-solid fa-edit"></i>
                    </button>
                    <button onclick="deleteContent(${item.id}, event)"
                            class="px-3 py-1 text-xs rounded-xl hover:bg-zinc-800 text-red-400 hover:text-red-500 transition-colors">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterByType(type) {
    currentFilter = type;
    document.querySelectorAll('[id^="filter-"]').forEach(el => {
        el.classList.remove('active-filter', 'bg-white', 'text-black');
        el.classList.add('text-zinc-400');
    });
    const activeBtn = (type === 'all')
        ? document.getElementById('filter-all')
        : document.getElementById('filter-video');
    if (activeBtn) {
        activeBtn.classList.add('active-filter', 'bg-white', 'text-black');
        activeBtn.classList.remove('text-zinc-400');
    }
    renderTable();
}

function filterTable() {
    const searchTerm = document.getElementById('global-search').value.toLowerCase().trim();
    if (!searchTerm) {
        renderTable();
        return;
    }
    const filtered = contentData.filter(item =>
        item.title.toLowerCase().includes(searchTerm)
    );
    renderTable(filtered);
}

// ========== Usuarios ==========

async function loadUsersFromAPI() {
    try {
        const response = await fetch('/dashboard/api/users');
        usersData = await response.json();
        renderUsersTable();
    } catch (error) {
        console.error("Error cargando usuarios:", error);
    }
}

function renderUsersTable() {
    const tbody = document.getElementById('users-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (!usersData || usersData.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="px-6 py-8 text-center text-zinc-500">No hay usuarios registrados.</td></tr>`;
        return;
    }

    usersData.forEach(user => {
        const tr = document.createElement('tr');
        tr.className = 'table-row border-b border-zinc-800';
        tr.innerHTML = `
            <td class="py-3 pl-6 font-medium">${user.name}</td>
            <td class="py-3 text-zinc-300">${user.email}</td>
            <td class="py-3">
                <span class="px-3 py-0.5 text-xs rounded-full font-medium bg-zinc-800 text-zinc-300">${user.role}</span>
            </td>
            <td class="py-3 pr-6">
                <div class="flex items-center justify-center gap-x-1">
                    <button onclick="openEditUserModal(${user.id})"
                            class="px-3 py-1 text-xs rounded-xl hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors">
                        <i class="fa-solid fa-edit"></i>
                    </button>
                    <button onclick="deleteUser(${user.id}, event)"
                            class="px-3 py-1 text-xs rounded-xl hover:bg-zinc-800 text-red-400 hover:text-red-500 transition-colors">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function openNewUserModal() {
    const modal = document.getElementById('modal-new-user');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeNewUserModal() {
    const modal = document.getElementById('modal-new-user');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

async function createNewUser() {
    const name = document.getElementById('new-user-name').value || 'Sin nombre';
    const email = document.getElementById('new-user-email').value;
    const password = document.getElementById('new-user-pass').value || '123456';
    const role = document.getElementById('new-user-role').value;

    if (!email) {
        alert('El email es obligatorio');
        return;
    }

    try {
        const response = await fetch('/dashboard/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, role })
        });
        const result = await response.json();
        if (result.success) {
            closeNewUserModal();
            await loadUsersFromAPI();
            showToast('Usuario creado exitosamente');
        } else {
            showToast(result.message || 'Error al crear usuario', true);
        }
    } catch (e) {
        showToast('Error de conexión', true);
    }
}

async function openEditUserModal(id) {
    const user = usersData.find(u => u.id === id);
    if (!user) return;
    currentEditUserId = id;

    const newName = prompt('Nombre:', user.name);
    if (newName === null) return;
    const newEmail = prompt('Email:', user.email);
    if (newEmail === null) return;
    const newRole = prompt('Rol (Administradora / Editor / Visualizador):', user.role);
    if (newRole === null) return;

    try {
        const response = await fetch(`/dashboard/api/users/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName, email: newEmail, role: newRole })
        });
        const result = await response.json();
        if (result.success) {
            await loadUsersFromAPI();
            showToast('Usuario actualizado');
        }
    } catch (e) {
        showToast('Error al actualizar', true);
    }
}

async function deleteUser(id, e) {
    e.stopImmediatePropagation();
    if (!confirm('¿Eliminar este usuario?')) return;

    try {
        const response = await fetch(`/dashboard/api/users/${id}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
            await loadUsersFromAPI();
            showToast('Usuario eliminado', true);
        } else {
            alert(result.message || 'No se pudo eliminar');
        }
    } catch (error) {
        showToast('Error al eliminar', true);
    }
}

// ========== Token ==========

async function refreshCurrentToken() {
    try {
        const response = await fetch('/dashboard/api/refresh_token', { method: 'POST' });
        const result = await response.json();
        if (result.success) {
            showToast('Sesión renovada correctamente');
        } else {
            showToast(result.message || 'No se pudo renovar el token', true);
        }
    } catch (e) {
        showToast('Error al renovar token', true);
    }
}

function startTokenVerification() {
    setInterval(async () => {
        try {
            const response = await fetch('/dashboard/api/verify_token');
            const data = await response.json();
            if (!data.valid) {
                alert('Tu sesión ha expirado o el token ya no es válido. Serás redirigido al login.');
                window.location.href = '/logout';
            }
        } catch (e) {
            // silencioso
        }
    }, 5 * 60 * 1000);
}

async function loadTokenConfig() {
    try {
        const response = await fetch('/dashboard/api/parametros');
        const data = await response.json();
        if (data.success && data.parametros.length > 0) {
            const tokenParam = data.parametros.find(p => p.clave === 'token_expiration_minutes');
            if (tokenParam) {
                const input = document.getElementById('token-minutes');
                if (input) input.value = tokenParam.valor;
            }
        }
    } catch (e) {}
}

async function saveTokenConfig() {
    const input = document.getElementById('token-minutes');
    const value = input.value;

    try {
        const response = await fetch('/dashboard/api/parametros', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ clave: 'token_expiration_minutes', valor: value })
        });
        const result = await response.json();
        if (result.success) {
            showToast('Configuración guardada. Los nuevos logins usarán ' + value + ' minutos.');
        } else {
            showToast(result.message || 'Error al guardar', true);
        }
    } catch (e) {
        showToast('Error de conexión', true);
    }
}

// ========== Contenido ==========

function openNewContentModal() {
    const modal = document.getElementById('modal-new');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeNewContentModal() {
    const modal = document.getElementById('modal-new');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

async function createNewContent() {
    const title = document.getElementById('new-title').value || 'Sin título';
    const youtubeUrl = document.getElementById('new-youtube').value;
    const duration = document.getElementById('new-duration').value || '—';
    const status = document.getElementById('new-status').value;

    let youtubeId = '';
    if (youtubeUrl.includes('youtube.com/watch?v=')) {
        youtubeId = youtubeUrl.split('v=')[1].split('&')[0];
    } else if (youtubeUrl.includes('youtu.be/')) {
        youtubeId = youtubeUrl.split('youtu.be/')[1].split('?')[0];
    }

    const newItem = {
        title: title,
        type: 'video',
        status: status,
        duration: duration,
        youtube_id: youtubeId,
        thumb: youtubeId
            ? `https://img.youtube.com/vi/${youtubeId}/hqdefault.jpg`
            : 'https://picsum.photos/id/160/300/170'
    };

    try {
        const response = await fetch('/dashboard/api/content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newItem)
        });
        const result = await response.json();
        if (result.success) {
            closeNewContentModal();
            await loadContentFromAPI();
            showToast('Video agregado exitosamente');
        }
    } catch (error) {
        showToast('Error al agregar contenido', true);
    }
}

function openEditModal(id) {
    const item = contentData.find(c => c.id === id);
    if (!item) return;

    currentEditId = id;
    document.getElementById('edit-id').value = item.id;
    document.getElementById('edit-title').value = item.title;
    document.getElementById('edit-status').value = item.status;
    document.getElementById('edit-views').value = item.plays || 0;
    document.getElementById('edit-duration').value = item.duration || '';

    const modal = document.getElementById('modal-edit');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeEditModal() {
    const modal = document.getElementById('modal-edit');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    currentEditId = null;
}

async function saveEditedContent() {
    if (!currentEditId) return;

    const updatedData = {
        title: document.getElementById('edit-title').value,
        status: document.getElementById('edit-status').value,
        plays: parseInt(document.getElementById('edit-views').value) || 0,
        duration: document.getElementById('edit-duration').value
    };

    try {
        const response = await fetch(`/dashboard/api/content/${currentEditId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        });
        const result = await response.json();
        if (result.success) {
            closeEditModal();
            await loadContentFromAPI();
            showToast('Cambios guardados');
        }
    } catch (error) {
        showToast('Error al guardar cambios', true);
    }
}

async function deleteContent(id, e) {
    e.stopImmediatePropagation();
    if (!confirm('¿Eliminar este contenido?')) return;

    try {
        const response = await fetch(`/dashboard/api/content/${id}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
            await loadContentFromAPI();
            showToast('Contenido eliminado', true);
        }
    } catch (error) {
        showToast('Error al eliminar', true);
    }
}

async function deleteCurrentContent() {
    if (!currentEditId) return;
    if (!confirm('¿Estás seguro de eliminar este contenido?')) return;

    try {
        await fetch(`/dashboard/api/content/${currentEditId}`, { method: 'DELETE' });
        closeEditModal();
        await loadContentFromAPI();
        showToast('Contenido eliminado', true);
    } catch (error) {
        showToast('Error al eliminar', true);
    }
}

async function playVideo(id, e) {
    e.stopImmediatePropagation();
    const item = contentData.find(c => c.id === id);
    if (!item || !item.youtube_id) return;

    try {
        await fetch(`/dashboard/api/content/${id}/play`, { method: 'POST' });
        await loadContentFromAPI();
    } catch (error) {}

    currentPlayingId = id;
    document.getElementById('player-title').textContent = item.title;
    document.getElementById('player-meta').innerHTML =
        `${item.duration || '—'} • <span class="text-emerald-400">${(item.plays || 0) + 1} reproducciones</span>`;

    const iframe = document.getElementById('youtube-player');
    iframe.src = `https://www.youtube.com/embed/${item.youtube_id}?rel=0&modestbranding=1`;

    const modal = document.getElementById('modal-player');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closePlayerModal() {
    const modal = document.getElementById('modal-player');
    const iframe = document.getElementById('youtube-player');
    iframe.src = '';
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    currentPlayingId = null;
}

function updateTopPlays() {
    const sorted = [...contentData].sort((a, b) => (b.plays || 0) - (a.plays || 0));
    const top1 = document.getElementById('top1-plays');
    const top2 = document.getElementById('top2-plays');
    if (top1) top1.textContent = sorted[0] ? (sorted[0].plays || 0) : 0;
    if (top2) top2.textContent = sorted[1] ? (sorted[1].plays || 0) : 0;
}

function updateStats() {
    const videosEl = document.getElementById('stat-videos');
    if (videosEl) videosEl.textContent = contentData.length;
}

function openVideoOnYoutube() {
    const item = contentData.find(c => c.id === currentPlayingId);
    if (item && item.youtube_id) {
        window.open(`https://www.youtube.com/watch?v=${item.youtube_id}`, '_blank');
    }
}

function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-5 right-5 px-5 py-3 rounded-2xl shadow-xl text-sm flex items-center gap-x-2 z-[9999] ${
        isError ? 'bg-red-600' : 'bg-zinc-800 border border-zinc-700'
    }`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'all 0.3s ease';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 200);
    }, 2600);
}

function showNotifications() {
    showToast('Tienes 7 notificaciones pendientes');
}

function navigateToSection(section) {
    document.querySelectorAll('[id^="section-"]').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    const navItem = document.querySelector(`.nav-item[data-section="${section}"]`);
    if (navItem) navItem.classList.add('active');

    const pageTitle = document.getElementById('page-title');

    if (section === 'contenido') {
        pageTitle.textContent = 'Biblioteca de Contenido';
        document.getElementById('section-contenido').classList.remove('hidden');
        loadContentFromAPI();
    } else if (section === 'usuarios') {
        pageTitle.textContent = 'Catálogo de Usuarios';
        document.getElementById('section-usuarios').classList.remove('hidden');
        loadUsersFromAPI();
    } else if (section === 'config') {
        pageTitle.textContent = 'Configuración';
        document.getElementById('section-config').classList.remove('hidden');
        loadTokenConfig();
    } else {
        pageTitle.textContent = 'Dashboard';
        document.getElementById('section-dashboard').classList.remove('hidden');
    }
}

function initializeDashboard() {
    loadContentFromAPI();

    const allFilter = document.getElementById('filter-all');
    if (allFilter) {
        allFilter.classList.add('bg-white', 'text-black', 'active-filter');
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === '/' && document.activeElement.tagName === 'BODY') {
            e.preventDefault();
            const search = document.getElementById('global-search');
            if (search) search.focus();
        }
        if (e.key === 'Escape') {
            document.querySelectorAll('.fixed.inset-0.flex').forEach(modal => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            });
        }
    });

    let inactivityTimer;
    function resetInactivityTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(() => {
            alert("Tu sesión ha expirado por inactividad (20 minutos).");
            window.location.href = "/logout";
        }, 20 * 60 * 1000);
    }
    const activityEvents = ['mousemove', 'keydown', 'click', 'scroll', 'touchstart'];
    activityEvents.forEach(event => {
        document.addEventListener(event, resetInactivityTimer, true);
    });
    resetInactivityTimer();

    startTokenVerification();
}

window.filterByType = filterByType;
window.openNewContentModal = openNewContentModal;
window.createNewContent = createNewContent;
window.openEditModal = openEditModal;
window.saveEditedContent = saveEditedContent;
window.deleteContent = deleteContent;
window.deleteCurrentContent = deleteCurrentContent;
window.playVideo = playVideo;
window.closePlayerModal = closePlayerModal;
window.navigateToSection = navigateToSection;
window.showNotifications = showNotifications;
window.openNewUserModal = openNewUserModal;
window.createNewUser = createNewUser;
window.refreshCurrentToken = refreshCurrentToken;
window.saveTokenConfig = saveTokenConfig;
window.closeNewContentModal = closeNewContentModal;
window.closeEditModal = closeEditModal;
window.closeNewUserModal = closeNewUserModal;
window.openVideoOnYoutube = openVideoOnYoutube;

window.onload = initializeDashboard;
