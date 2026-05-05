"use strict";

// --- CONFIGURAÇÃO INICIAL ---
const CAPACIDADE = 8;
let currentMode = 'binary_tree';

// Estruturas de Dados (Simulação da Memória do PDF)
const memory = {
    key: Array(CAPACIDADE).fill(null),
    p: Array(CAPACIDADE).fill(null),
    left: Array(CAPACIDADE).fill(null),
    right: Array(CAPACIDADE).fill(null),
    next: Array(CAPACIDADE).fill(null),
    prev: Array(CAPACIDADE).fill(null),
    free: 0,
    root: null,
    head: null
};

// Inicializar Free List (Slide 31)
function initMemory() {
    for (let i = 0; i < CAPACIDADE; i++) {
        memory.key[i] = null;
        memory.p[i] = null;
        memory.left[i] = null;
        memory.right[i] = i === CAPACIDADE - 1 ? null : i + 1;
        memory.next[i] = memory.right[i]; // Mesma lógica para listas
        memory.prev[i] = null;
    }
    memory.free = 0;
    memory.root = null;
    memory.head = null;
    updateUI();
}

// --- ALOCAÇÃO DE MEMÓRIA (Slide 32) ---
function allocateObject() {
    if (memory.free === null) {
        alert("Ero: Memória Exausta (Overflow)!");
        return null;
    }
    let x = memory.free;
    memory.free = memory.right[x];
    return x;
}

// --- LÓGICA DE ÁRVORE BINÁRIA (Slide 36) ---
function treeInsert(k) {
    let z = allocateObject();
    if (z === null) return;

    memory.key[z] = k;
    memory.left[z] = null;
    memory.right[z] = null;
    memory.p[z] = null;

    let y = null;
    let x = memory.root;

    while (x !== null) {
        y = x;
        if (k < memory.key[x]) {
            x = memory.left[x];
        } else {
            x = memory.right[x];
        }
    }

    memory.p[z] = y;
    if (y === null) {
        memory.root = z;
    } else if (k < memory.key[y]) {
        memory.left[y] = z;
    } else {
        memory.right[y] = z;
    }
    
    logStep(`Inserido ${k} no índice ${z}.`);
    updateUI();
}

// --- LGICA DE LISTA DUPLAMENTE LIGADA (Slides 18-21) ---
function listInsert(k) {
    let x = allocateObject();
    if (x === null) return;

    memory.key[x] = k;
    memory.next[x] = memory.head;
    
    if (memory.head !== null) {
        memory.prev[memory.head] = x;
    }
    
    memory.head = x;
    memory.prev[x] = null;
    
    logStep(`Lista: Inserido ${k} no incio (ndice ${x}).`);
    updateUI();
}

function listDelete(idx) {
    if (idx === null) return;
    
    if (memory.prev[idx] !== null) {
        memory.next[memory.prev[idx]] = memory.next[idx];
    } else {
        memory.head = memory.next[idx];
    }
    
    if (memory.next[idx] !== null) {
        memory.prev[memory.next[idx]] = memory.prev[idx];
    }
    
    // Devolver  Free List
    memory.key[idx] = null;
    memory.right[idx] = memory.free;
    memory.free = idx;
    
    logStep(`Lista: Removido elemento do ndice ${idx}.`);
    updateUI();
}

// --- INTERFACE E VISUALIZAO ---
function updateUI() {
    renderTable();
    renderVisualizer();
}

function renderTable() {
    const tableHeaders = document.getElementById('table-headers');
    const tableBody = document.getElementById('table-body');
    
    // Headers dependem do modo
    let headers = ['Índice', 'Key'];
    if (currentMode === 'binary_tree') {
        headers.push('P (Parent)', 'Left', 'Right');
    } else {
        headers.push('Prev', 'Next');
    }
    
    tableHeaders.innerHTML = headers.map(h => `<th>${h}</th>`).join('');
    
    // Linhas
    tableBody.innerHTML = '';
    for (let i = 0; i < CAPACIDADE; i++) {
        const tr = document.createElement('tr');
        if (i === memory.root || i === memory.head) tr.className = 'active-row';
        
        let cols = [`<td class="idx-col">${i} ${i === memory.free ? ' (F)' : ''}</td>`];
        cols.push(`<td class="key-col">${memory.key[i] ?? '.'}</td>`);
        
        if (currentMode === 'binary_tree') {
            cols.push(`<td class="p-col">${memory.p[i] ?? '/'}</td>`);
            cols.push(`<td class="next-col">${memory.left[i] ?? '/'}</td>`);
            cols.push(`<td class="next-col">${memory.right[i] ?? '/'}</td>`);
        } else {
            cols.push(`<td class="prev-col">${memory.prev[i] ?? '/'}</td>`);
            cols.push(`<td class="next-col">${memory.next[i] ?? '/'}</td>`);
        }
        
        tr.innerHTML = cols.join('');
        tableBody.appendChild(tr);
    }
}

function renderVisualizer() {
    const area = document.getElementById('visualizer');
    area.innerHTML = '';
    
    if (currentMode === 'binary_tree') {
        if (memory.root === null) {
            area.innerHTML = '<div class="placeholder-text">rvore Vazia</div>';
            return;
        }
        drawTreeNode(memory.root, 400, 50, 200);
    } else {
        if (memory.head === null) {
            area.innerHTML = '<div class="placeholder-text">Lista Vazia</div>';
            return;
        }
        drawList();
    }
}

function drawList() {
    const area = document.getElementById('visualizer');
    let curr = memory.head;
    let x = 50;
    const y = 200;
    
    while (curr !== null) {
        // N da lista
        const div = document.createElement('div');
        div.className = 'tree-node'; // Reaproveitar estilo circular ou mudar para quadrado
        div.style.borderRadius = '8px';
        div.style.left = `${x}px`;
        div.style.top = `${y}px`;
        div.innerHTML = `<span style="font-size:10px; color:var(--text-secondary)">[${memory.prev[curr] ?? '/'}|</span>${memory.key[curr]}<span style="font-size:10px; color:var(--text-secondary)">|${memory.next[curr] ?? '/'}]</span>`;
        area.appendChild(div);
        
        // Seta para o prximo
        if (memory.next[curr] !== null) {
            drawEdge(x + 50, y + 25, x + 100, y + 25);
            // Seta de volta
            drawEdge(x + 100, y + 15, x + 50, y + 15);
        }
        
        curr = memory.next[curr];
        x += 100;
        if (x > 700) break; // Evitar overflow visual
    }
}

function drawTreeNode(idx, x, y, offset) {
    if (idx === null) return;
    
    const area = document.getElementById('visualizer');
    
    // Desenhar ligações primeiro (atrás)
    if (memory.left[idx] !== null) {
        drawEdge(x, y, x - offset, y + 80);
        drawTreeNode(memory.left[idx], x - offset, y + 80, offset / 1.5);
    }
    if (memory.right[idx] !== null) {
        drawEdge(x, y, x + offset, y + 80);
        drawTreeNode(memory.right[idx], x + offset, y + 80, offset / 1.5);
    }
    
    // Desenhar nó
    const div = document.createElement('div');
    div.className = 'tree-node';
    div.style.left = `${x - 25}px`;
    div.style.top = `${y - 25}px`;
    div.innerText = memory.key[idx];
    area.appendChild(div);
}

function drawEdge(x1, y1, x2, y2) {
    const area = document.getElementById('visualizer');
    const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
    
    const edge = document.createElement('div');
    edge.className = 'tree-edge';
    edge.style.width = `${length}px`;
    edge.style.left = `${x1}px`;
    edge.style.top = `${y1}px`;
    edge.style.transform = `rotate(${angle}deg)`;
    area.appendChild(edge);
}

// --- HANDLERS ---
function handleAdd() {
    const val = parseInt(document.getElementById('node-value').value);
    if (isNaN(val)) return;
    
    if (currentMode === 'binary_tree') {
        treeInsert(val);
    } else {
        listInsert(val);
    }
}

function handleClear() {
    initMemory();
}

function switchMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    initMemory();
}

function logStep(msg) {
    document.getElementById('step-desc').innerText = `[AÇÃO] ${msg}`;
}

// Inicializar
window.onload = initMemory;
