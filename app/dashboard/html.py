DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Telegram Stremio V2 - Control Center</title>

<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%236366f1'/%3E%3Cpath d='M12.5 9.5l10 6.5-10 6.5z' fill='white'/%3E%3C/svg%3E">
<meta name="theme-color" content="#6366f1">

<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    color-scheme: dark;
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    --bg: #090d16;
    --card: #111827;
    --border: rgba(255, 255, 255, 0.08);
    --text: #f8fafc;
    --text-sec: #94a3b8;

    --surface: color-mix(in srgb, var(--text) 5%, transparent);
    --surface-2: color-mix(in srgb, var(--text) 9%, transparent);
    --surface-3: color-mix(in srgb, var(--text) 14%, transparent);
    --hairline: color-mix(in srgb, var(--text) 12%, transparent);
    --hairline-strong: color-mix(in srgb, var(--text) 20%, transparent);
    --muted: color-mix(in srgb, var(--text) 42%, transparent);
    --ring: color-mix(in srgb, var(--primary) 35%, transparent);
    --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.35);
    --shadow-strong: 0 24px 60px rgba(0, 0, 0, 0.45);
}

html { scroll-behavior: smooth; }

body {
    font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-image:
        radial-gradient(circle at 15% 10%, color-mix(in srgb, var(--primary) 12%, transparent), transparent 45%),
        radial-gradient(circle at 85% 80%, color-mix(in srgb, var(--accent) 12%, transparent), transparent 45%),
        radial-gradient(circle at 50% 50%, color-mix(in srgb, var(--card) 40%, transparent), transparent 60%);
}

.glass-panel {
    background: color-mix(in srgb, var(--card) 90%, var(--bg));
    border: 1px solid var(--hairline);
    box-shadow: var(--shadow-soft);
    border-radius: 1.5rem;
}

.glass-nav {
    background: color-mix(in srgb, var(--card) 82%, transparent);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.glass-pill { border-radius: 9999px; }

.surface-card {
    background: color-mix(in srgb, var(--card) 92%, var(--bg));
    border: 1px solid var(--hairline);
    border-radius: 1.5rem;
}

.btn-primary {
    background: var(--primary);
    color: #ffffff;
    font-weight: 700;
    border-radius: 1rem;
    transition: filter .2s ease, transform .12s ease, box-shadow .2s ease;
    box-shadow: 0 8px 22px color-mix(in srgb, var(--primary) 35%, transparent);
}
.btn-primary:hover { filter: brightness(1.1); transform: translateY(-1px); }
.btn-primary:active { transform: scale(.97); }

.btn-ghost {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--hairline);
    border-radius: 1rem;
    font-weight: 700;
    transition: background .2s ease, border-color .2s ease;
}
.btn-ghost:hover { background: var(--surface-2); border-color: var(--hairline-strong); }

.badge {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    font-size: .65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .12em;
    padding: .25rem .6rem;
    border-radius: 9999px;
    background: color-mix(in srgb, var(--primary) 14%, transparent);
    color: var(--primary);
}

.field, .s-input {
    width: 100%;
    background: color-mix(in srgb, var(--card) 88%, var(--bg));
    color: var(--text);
    border: 1px solid var(--hairline);
    border-radius: 0.9rem;
    padding: 0.65rem 1rem;
    font-size: 0.88rem;
    transition: border-color .2s ease, box-shadow .2s ease;
}
.field:focus, .s-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--ring);
}

.s-label {
    display: block;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-sec);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.4rem;
}

.settings-card, .tool-card {
    background: color-mix(in srgb, var(--card) 94%, var(--bg));
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.settings-card h2, .tool-card h2 {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--primary);
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.divider { border: none; border-top: 1px solid var(--border); margin: 1.25rem 0; }
.hint { font-size: 0.8rem; color: var(--text-sec); }

/* Toggle switch */
.toggle-wrap { display: flex; align-items: center; gap: 0.75rem; cursor: pointer; }
.toggle-input { position: absolute; opacity: 0; width: 0; height: 0; }
.toggle-track {
    display: inline-block; width: 3rem; height: 1.625rem;
    border-radius: 9999px; background: var(--border);
    position: relative; transition: background 0.2s ease; flex-shrink: 0;
}
.toggle-track::after {
    content: ''; position: absolute;
    top: 3px; left: 3px;
    width: 20px; height: 20px;
    border-radius: 50%; background: white;
    transition: transform 0.2s ease;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
.toggle-input:checked + .toggle-track { background: var(--primary); }
.toggle-input:checked + .toggle-track::after { transform: translateX(1.375rem); }
.toggle-label { font-size: 0.88rem; color: var(--text); user-select: none; }

/* Status pill */
.status-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.25rem 0.8rem; border-radius: 9999px;
    font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;
}
.status-idle      { background: color-mix(in srgb,var(--text-sec) 15%,transparent); color: var(--text-sec); }
.status-running   { background: rgba(34,197,94,0.15);  color: #22c55e; }
.status-paused    { background: rgba(245,158,11,0.15); color: #f59e0b; }
.status-cancelled { background: rgba(245,158,11,0.15); color: #f59e0b; }
.status-completed { background: rgba(34,197,94,0.15);  color: #22c55e; }
.status-error     { background: rgba(239,68,68,0.15);  color: #ef4444; }

/* Progress track */
.progress-track {
    width: 100%; height: 0.65rem; border-radius: 9999px;
    background: color-mix(in srgb, var(--text-sec) 18%, transparent);
    overflow: hidden;
}
.progress-fill {
    height: 100%; border-radius: 9999px; background: var(--primary);
    width: 0%; transition: width 0.4s ease;
}

.shadow-glow {
    filter: drop-shadow(0 0 8px color-mix(in srgb, var(--primary) 45%, transparent));
}

.stream-card {
    background: color-mix(in srgb, var(--card) 55%, transparent);
    border: 1px solid var(--border);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
    border-radius: 1.5rem;
}

.stream-badge-live {
    background: color-mix(in srgb, var(--primary) 18%, transparent);
    color: var(--primary);
}

.nav-link {
    color: var(--text-sec);
    border-radius: 9999px;
    padding: 0.45rem clamp(0.55rem, 0.8vw, 1.1rem);
    transition: color 0.25s ease, background 0.25s ease;
    position: relative;
    z-index: 1;
    white-space: nowrap;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.nav-link:hover { color: var(--text); }

.nav-link.pill-active {
    color: #ffffff !important;
    background: var(--primary);
    box-shadow: 0 0 15px color-mix(in srgb, var(--primary) 45%, transparent);
}

#toast-container {
    position: fixed;
    top: 1.25rem;
    right: 1.25rem;
    z-index: 99999;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    pointer-events: none;
}

.toast {
    pointer-events: auto;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1.25rem;
    border-radius: 1rem;
    background: color-mix(in srgb, var(--card) 95%, var(--bg));
    border: 1px solid var(--hairline-strong);
    box-shadow: var(--shadow-strong);
    color: var(--text);
    font-size: 0.88rem;
    min-width: 260px;
    max-width: 380px;
    animation: toast-in 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.toast.success { border-color: rgba(34, 197, 94, 0.4); }
.toast.success i { color: #22c55e; }
.toast.error { border-color: rgba(239, 68, 68, 0.4); }
.toast.error i { color: #ef4444; }
.toast.info { border-color: color-mix(in srgb, var(--primary) 40%, transparent); }
.toast.info i { color: var(--primary); }

@keyframes toast-in {
    from { opacity: 0; transform: translateY(-8px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes toast-out {
    from { opacity: 1; transform: translateY(0) scale(1); }
    to { opacity: 0; transform: translateY(-8px) scale(0.96); }
}

* { scrollbar-width: thin; scrollbar-color: var(--hairline-strong) transparent; }
*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-thumb { background: var(--hairline-strong); border-radius: 9999px; }

/* Multi-channel chips */
.multi-list-items { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 0.6rem; }
.multi-item { display: flex; align-items: center; gap: 0.5rem; }
.channel-chip {
    flex: 1; min-width: 0;
    padding: 0.55rem 0.85rem;
    background: color-mix(in srgb, var(--primary) 10%, transparent);
    border: 1px solid color-mix(in srgb, var(--primary) 28%, transparent);
    border-radius: 0.75rem;
    font-size: 0.875rem; font-weight: 600;
    color: var(--text);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.remove-btn {
    width: 2rem; height: 2rem; flex-shrink: 0;
    background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.25);
    color: #ef4444; border-radius: 0.5rem;
    font-size: 1rem; line-height: 1;
    cursor: pointer; transition: background 0.15s;
    display: flex; align-items: center; justify-content: center;
}
.remove-btn:hover { background: rgba(239,68,68,0.25); }

/* Grid helpers */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 640px) { .grid-2 { grid-template-columns: 1fr; } }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(115px,1fr)); gap: 0.75rem; }
.stat-box {
    background: color-mix(in srgb, var(--bg) 55%, transparent);
    border: 1px solid var(--border); border-radius: 0.9rem;
    padding: 0.75rem 0.9rem;
}
.stat-box .v { font-size: 1.25rem; font-weight: 800; }
.stat-box .l { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--text-sec); }
</style>
</head>

<body class="pt-24 pb-12 antialiased">

<!-- Floating Top Glass Navbar -->
<nav id="navbar"
  class="fixed top-5 left-1/2 -translate-x-1/2 w-[95%] max-w-6xl z-50
  glass-panel glass-nav glass-pill px-4 sm:px-5 py-2.5
  flex items-center justify-between gap-2 sm:gap-4
  transition-all duration-300">
    <div class="flex items-center gap-3 shrink-0 cursor-pointer" onclick="switchTab('overview')">
        <div class="w-8 h-8 rounded-xl bg-primary flex items-center justify-center shadow-[0_0_15px_var(--primary)]">
            <i class="fa-solid fa-play text-white text-xs"></i>
        </div>
        <div class="flex items-center gap-2">
            <span class="text-base sm:text-lg font-extrabold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                TG Stremio
            </span>
            <span class="hidden sm:inline-flex px-2 py-0.5 rounded-full text-[10px] font-bold bg-primary/15 text-primary border border-primary/25">
                v2.0 Turbo
            </span>
        </div>
    </div>

    <!-- Desktop Nav Links -->
    <div id="nav-container" class="hidden lg:flex relative items-center gap-1 p-1 bg-black/20 rounded-full border border-hairline">
        <button onclick="switchTab('overview')" class="nav-link pill-active" data-tab="overview">
            <i class="fa-solid fa-gauge-high text-xs"></i> Overview
        </button>
        <button onclick="switchTab('media')" class="nav-link" data-tab="media">
            <i class="fa-solid fa-clapperboard text-xs"></i> Media
        </button>
        <button onclick="switchTab('unmatched')" class="nav-link" data-tab="unmatched">
            <i class="fa-solid fa-list-check text-xs"></i> Queue
            <span id="nav-unmatched-badge" class="hidden px-1.5 py-0.2 rounded-full text-[10px] bg-rose-500 text-white font-black">0</span>
        </button>
        <button onclick="switchTab('bots')" class="nav-link" data-tab="bots">
            <i class="fa-solid fa-robot text-xs"></i> Bots
            <span id="nav-bot-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-primary/25 text-primary font-black">0</span>
        </button>
        <button onclick="switchTab('tools')" class="nav-link" data-tab="tools">
            <i class="fa-solid fa-screwdriver-wrench text-xs"></i> Tools
        </button>
        <button onclick="switchTab('tokens')" class="nav-link" data-tab="tokens">
            <i class="fa-solid fa-key text-xs"></i> Tokens
        </button>
        <button onclick="switchTab('settings')" class="nav-link" data-tab="settings">
            <i class="fa-solid fa-gear text-xs"></i> Settings
        </button>
    </div>

    <!-- Right Controls -->
    <div class="flex items-center gap-2">
        <div class="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Online</span>
        </div>
        <button onclick="refreshDashboard()" title="Refresh" class="w-9 h-9 rounded-full bg-surface hover:bg-surface-2 flex items-center justify-center text-text-sec hover:text-text border border-hairline transition">
            <i id="global-refresh-icon" class="fa-solid fa-arrows-rotate text-sm"></i>
        </button>
        <button id="mobile-toggle-btn" onclick="toggleMobileNav()" class="lg:hidden w-9 h-9 rounded-full bg-surface flex items-center justify-center text-text-sec hover:text-text border border-hairline transition">
            <i id="mobile-toggle-icon" class="fa-solid fa-bars text-sm"></i>
        </button>
    </div>

    <!-- Mobile Drawer -->
    <div id="mobile-menu" class="hidden absolute top-[calc(100%+8px)] left-0 w-full glass-panel p-3 flex flex-col gap-1.5 lg:hidden shadow-strong z-50">
        <button onclick="switchTab('overview'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-gauge-high text-primary"></i> Overview
        </button>
        <button onclick="switchTab('media'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-clapperboard text-primary"></i> Media
        </button>
        <button onclick="switchTab('unmatched'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-list-check text-primary"></i> Queue
        </button>
        <button onclick="switchTab('bots'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-robot text-primary"></i> Bots
        </button>
        <button onclick="switchTab('tools'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-screwdriver-wrench text-primary"></i> Tools &amp; Re-Index
        </button>
        <button onclick="switchTab('tokens'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-key text-primary"></i> Tokens &amp; Stremio
        </button>
        <button onclick="switchTab('settings'); toggleMobileNav()" class="px-4 py-2.5 rounded-xl hover:bg-surface text-left font-medium text-sm flex items-center gap-3">
            <i class="fa-solid fa-gear text-primary"></i> Settings
        </button>
    </div>
</nav>

<!-- Main Container -->
<main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">

    <!-- ========================================== -->
    <!-- TAB 1: OVERVIEW -->
    <!-- ========================================== -->
    <div id="tab-overview" class="tab-pane">
        <header class="mb-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                        System Overview
                    </h1>
                    <p class="text-text-sec text-xs sm:text-sm mt-1">Real-time performance, multi-bot cluster, and live stream activity</p>
                </div>

                <button onclick="refreshDashboard()"
                    class="w-full md:w-auto flex items-center justify-center space-x-2 px-6 py-3 rounded-2xl bg-primary/10 border border-primary/20 hover:bg-primary hover:text-white transition-all group active:scale-95 flex-shrink-0">
                    <i id="overview-refresh-icon" class="fa-solid fa-arrows-rotate group-hover:rotate-180 transition-transform duration-700 text-primary group-hover:text-white"></i>
                    <span class="font-bold text-sm uppercase tracking-wider text-primary group-hover:text-white">Refresh Data</span>
                </button>
            </div>
        </header>

        <!-- Top 4 Quick Stats -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mb-8">
            <div class="glass-panel p-3.5 sm:p-5 rounded-2xl sm:rounded-[2rem] flex items-center gap-3 sm:gap-4 min-w-0">
                <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl bg-primary/10 flex items-center justify-center text-primary shadow-glow flex-shrink-0">
                    <i class="fa-solid fa-clock"></i>
                </div>
                <div class="min-w-0">
                    <p class="text-[9px] sm:text-[10px] uppercase font-bold text-text-sec tracking-widest">Uptime</p>
                    <p id="sys-uptime" class="text-sm sm:text-lg font-bold text-text truncate">Active</p>
                </div>
            </div>

            <div class="glass-panel p-3.5 sm:p-5 rounded-2xl sm:rounded-[2rem] flex items-center gap-3 sm:gap-4 min-w-0">
                <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl bg-accent/10 flex items-center justify-center text-accent shadow-glow flex-shrink-0">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div class="min-w-0">
                    <p class="text-[9px] sm:text-[10px] uppercase font-bold text-text-sec tracking-widest">Active Bots</p>
                    <p id="sys-bots-count" class="text-sm sm:text-lg font-bold text-text truncate">0 Nodes</p>
                </div>
            </div>

            <div class="glass-panel p-3.5 sm:p-5 rounded-2xl sm:rounded-[2rem] flex items-center gap-3 sm:gap-4 min-w-0">
                <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl bg-primary/10 flex items-center justify-center text-primary shadow-glow flex-shrink-0">
                    <i class="fa-solid fa-tower-broadcast"></i>
                </div>
                <div class="min-w-0">
                    <p class="text-[9px] sm:text-[10px] uppercase font-bold text-text-sec tracking-widest">Live Streams</p>
                    <p id="sys-live-streams" class="text-sm sm:text-lg font-bold text-text truncate">0 Active</p>
                </div>
            </div>

            <div class="glass-panel p-3.5 sm:p-5 rounded-2xl sm:rounded-[2rem] flex items-center gap-3 sm:gap-4 min-w-0">
                <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl bg-surface flex items-center justify-center text-text-sec flex-shrink-0">
                    <i class="fa-solid fa-code-branch"></i>
                </div>
                <div class="min-w-0">
                    <p class="text-[9px] sm:text-[10px] uppercase font-bold text-text-sec tracking-widest">Version</p>
                    <p id="sys-version" class="text-sm sm:text-lg font-bold text-text truncate">v2.0.0 Turbo</p>
                </div>
            </div>
        </div>

        <!-- Main 2-Column Split: Storage & Media vs Live Streams Network -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 min-w-0">
            <!-- Left 2 Cols: Storage & Quick Links -->
            <div class="lg:col-span-2 space-y-8 min-w-0">
                <section>
                    <h3 class="flex items-center gap-2 text-lg font-bold mb-4 ml-2">
                        <i class="fa-solid fa-database text-primary"></i> Database &amp; Storage Nodes
                    </h3>

                    <div id="storage-nodes-container" class="grid grid-cols-1 md:grid-cols-2 gap-4 min-w-0">
                        <div class="glass-panel p-6 rounded-[2rem] border-hairline bg-card/10 min-w-0">
                            <div class="flex justify-between items-start gap-3 mb-6 min-w-0">
                                <div>
                                    <h4 class="font-bold text-text truncate">MongoDB (Atlas)</h4>
                                    <p class="text-xs text-text-sec mt-0.5">Primary Media &amp; Metadata Database</p>
                                </div>
                                <span class="text-[10px] bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 px-2 py-1 rounded-lg font-bold uppercase whitespace-nowrap">Online</span>
                            </div>

                            <div class="space-y-4 min-w-0">
                                <div class="flex justify-between text-sm gap-2 min-w-0">
                                    <span class="text-text-sec">Movies / TV Series</span>
                                    <span id="db-media-counts" class="font-bold text-text truncate">0 / 0</span>
                                </div>
                                <div class="flex justify-between text-sm gap-2 min-w-0">
                                    <span class="text-text-sec">Total Indexed Documents</span>
                                    <span id="db-total-media" class="font-bold text-text truncate">0</span>
                                </div>

                                <div class="space-y-2 min-w-0 pt-2 border-t border-hairline">
                                    <div class="flex justify-between text-xs font-bold uppercase tracking-widest gap-2 min-w-0">
                                        <span class="text-text-sec">Storage Footprint</span>
                                        <span id="db-storage-size" class="text-primary truncate">~0 MB</span>
                                    </div>
                                    <div class="w-full h-1.5 bg-surface rounded-full overflow-hidden">
                                        <div class="h-full bg-gradient-to-r from-primary to-accent rounded-full" style="width: 35%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="glass-panel p-6 rounded-[2rem] border-hairline bg-card/10 min-w-0">
                            <div class="flex justify-between items-start gap-3 mb-6 min-w-0">
                                <div>
                                    <h4 class="font-bold text-text truncate">Engine Architecture</h4>
                                    <p class="text-xs text-text-sec mt-0.5">Multi-Bot Parallel Streamer</p>
                                </div>
                                <span class="text-[10px] bg-primary/15 text-primary border border-primary/30 px-2 py-1 rounded-lg font-bold uppercase whitespace-nowrap">Active</span>
                            </div>

                            <div class="space-y-4 min-w-0">
                                <div class="flex justify-between text-sm gap-2 min-w-0">
                                    <span class="text-text-sec">Prefetch Chunk Window</span>
                                    <span class="font-bold text-text truncate">8 MB Parallel</span>
                                </div>
                                <div class="flex justify-between text-sm gap-2 min-w-0">
                                    <span class="text-text-sec">Connection Pre-warming</span>
                                    <span class="font-bold text-emerald-400 truncate">Enabled (DC 4/2/1)</span>
                                </div>
                                <div class="flex justify-between text-sm gap-2 min-w-0">
                                    <span class="text-text-sec">Catalog Spotlight</span>
                                    <span class="font-bold text-accent truncate">15m Dynamic Rotation</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="grid grid-cols-1 sm:grid-cols-2 gap-4 min-w-0">
                    <div onclick="switchTab('media', 'movie')" class="glass-panel p-6 rounded-[2rem] hover:bg-primary/5 transition-all group border border-hairline cursor-pointer min-w-0">
                        <div class="flex items-center gap-4 min-w-0">
                            <div class="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary group-hover:scale-110 transition-transform flex-shrink-0">
                                <i class="fa-solid fa-film text-2xl"></i>
                            </div>
                            <div class="min-w-0">
                                <h4 class="font-bold text-text truncate">Manage Movies</h4>
                                <p class="text-xs text-text-sec truncate">Browse library, posters &amp; qualities</p>
                            </div>
                            <i class="fa-solid fa-chevron-right ml-auto text-muted group-hover:text-primary group-hover:translate-x-1 transition-all flex-shrink-0"></i>
                        </div>
                    </div>

                    <div onclick="switchTab('media', 'tv')" class="glass-panel p-6 rounded-[2rem] hover:bg-accent/5 transition-all group border border-hairline cursor-pointer min-w-0">
                        <div class="flex items-center gap-4 min-w-0">
                            <div class="w-14 h-14 rounded-2xl bg-accent/10 flex items-center justify-center text-accent group-hover:scale-110 transition-transform flex-shrink-0">
                                <i class="fa-solid fa-tv text-2xl"></i>
                            </div>
                            <div class="min-w-0">
                                <h4 class="font-bold text-text truncate">Manage TV Shows</h4>
                                <p class="text-xs text-text-sec truncate">Handle series, seasons &amp; episodes</p>
                            </div>
                            <i class="fa-solid fa-chevron-right ml-auto text-muted group-hover:text-accent group-hover:translate-x-1 transition-all flex-shrink-0"></i>
                        </div>
                    </div>

                    <div onclick="switchTab('tools')" class="glass-panel p-6 rounded-[2rem] hover:bg-primary/5 transition-all group border border-hairline cursor-pointer min-w-0">
                        <div class="flex items-center gap-4 min-w-0">
                            <div class="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary group-hover:scale-110 transition-transform flex-shrink-0">
                                <i class="fa-solid fa-screwdriver-wrench text-2xl"></i>
                            </div>
                            <div class="min-w-0">
                                <h4 class="font-bold text-text truncate">Tools &amp; Re-Index</h4>
                                <p class="text-xs text-text-sec truncate">Scan channels, DB check, duplicates</p>
                            </div>
                            <i class="fa-solid fa-chevron-right ml-auto text-muted group-hover:text-primary group-hover:translate-x-1 transition-all flex-shrink-0"></i>
                        </div>
                    </div>

                    <div onclick="switchTab('unmatched')" class="glass-panel p-6 rounded-[2rem] hover:bg-amber-500/5 transition-all group border border-hairline cursor-pointer min-w-0">
                        <div class="flex items-center gap-4 min-w-0">
                            <div class="w-14 h-14 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-400 group-hover:scale-110 transition-transform flex-shrink-0">
                                <i class="fa-solid fa-triangle-exclamation text-2xl"></i>
                            </div>
                            <div class="min-w-0">
                                <h4 class="font-bold text-text truncate">Unmatched Queue</h4>
                                <p class="text-xs text-text-sec truncate">1-click TMDB poster search &amp; match</p>
                            </div>
                            <span id="quick-unmatched-badge" class="ml-auto px-2.5 py-1 text-xs font-black rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">0</span>
                        </div>
                    </div>
                </section>
            </div>

            <!-- Right 1 Col: Live Network -->
            <div class="lg:col-span-1 min-w-0">
                <div class="glass-panel rounded-[2.5rem] overflow-hidden h-full min-w-0">
                    <div class="p-6 border-b border-hairline min-w-0">
                        <div class="flex items-center flex-wrap justify-between gap-3 mb-2 min-w-0">
                            <h3 class="flex items-center gap-2 text-lg font-bold whitespace-nowrap">
                                <i class="fa-solid fa-circle-play text-red-500 animate-pulse"></i> Live Network
                            </h3>
                            <span id="live-stream-count" class="text-[10px] font-bold uppercase tracking-[0.2em] text-primary bg-primary/10 px-3 py-1 rounded-full whitespace-nowrap">
                                0 Active
                            </span>
                        </div>
                        <p class="text-xs text-text-sec">Current Telegram streaming sessions</p>
                    </div>

                    <div class="p-6 space-y-6 min-w-0">
                        <div class="grid grid-cols-2 gap-3 min-w-0">
                            <div class="glass-panel p-4 rounded-2xl min-w-0">
                                <p class="text-[10px] uppercase font-bold tracking-widest text-text-sec truncate">Live Now</p>
                                <p id="live-now-count" class="text-2xl font-extrabold mt-1 text-text truncate">0</p>
                            </div>
                            <div class="glass-panel p-4 rounded-2xl min-w-0">
                                <p class="text-[10px] uppercase font-bold tracking-widest text-text-sec truncate">Recent</p>
                                <p id="recent-stream-count" class="text-2xl font-extrabold mt-1 text-text truncate">0</p>
                            </div>
                        </div>

                        <div class="min-w-0">
                            <div class="flex items-center flex-wrap justify-between gap-2 mb-3 min-w-0">
                                <h4 class="text-sm font-bold text-text whitespace-nowrap">Active Streams</h4>
                                <span class="text-[10px] uppercase tracking-widest text-text-sec whitespace-nowrap">Real-time</span>
                            </div>
                            <div id="active-streams-container" class="space-y-4 min-w-0">
                                <div class="glass-panel p-8 rounded-[2rem] text-center border-dashed border-hairline">
                                    <i class="fa-solid fa-satellite-dish text-4xl text-muted mb-3"></i>
                                    <p class="text-sm text-text-sec font-medium">No active streams right now</p>
                                    <p class="text-xs text-text-sec mt-1">The live network is idle at the moment.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 2: MEDIA MANAGEMENT -->
    <!-- ========================================== -->
    <div id="tab-media" class="tab-pane hidden">
        <section class="glass-panel rounded-3xl p-4 sm:p-5 mb-6">
            <div class="flex flex-col xl:flex-row xl:items-center gap-4">
                <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight text-text shrink-0">
                    <i class="fa-solid fa-clapperboard text-primary mr-2"></i>Media Library
                </h1>

                <div class="relative flex-1 min-w-0">
                    <i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-text-sec text-sm"></i>
                    <input type="text" id="media-search-input"
                           onkeyup="if(event.key==='Enter') loadMediaLibrary()"
                           placeholder="Search indexed movies &amp; series by title..."
                           class="w-full pl-11 pr-24 py-3 rounded-2xl bg-slate-900/80 text-text placeholder:text-text-sec border border-border focus:outline-none focus:ring-2 focus:ring-primary/60 focus:border-primary transition">
                    <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                        <button onclick="document.getElementById('media-search-input').value=''; loadMediaLibrary()" title="Clear"
                                class="w-8 h-8 inline-flex items-center justify-center rounded-xl text-text-sec hover:bg-surface-2 transition">
                            <i class="fa-solid fa-rotate-left text-xs"></i>
                        </button>
                        <button onclick="loadMediaLibrary()" title="Search"
                                class="w-8 h-8 inline-flex items-center justify-center rounded-xl bg-primary text-white shadow-lg shadow-primary/20">
                            <i class="fa-solid fa-magnifying-glass text-xs"></i>
                        </button>
                    </div>
                </div>

                <div class="flex flex-wrap items-center gap-2">
                    <button onclick="setMediaFilter(null)" id="filter-all-btn"
                       class="inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border bg-primary text-white border-primary shadow-lg shadow-primary/20">
                        All Media
                    </button>
                    <button onclick="setMediaFilter('movie')" id="filter-movies-btn"
                       class="inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border glass-panel text-text hover:bg-surface-2 border-hairline">
                        <i class="fa-solid fa-film"></i> Movies
                    </button>
                    <button onclick="setMediaFilter('tv')" id="filter-tv-btn"
                       class="inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border glass-panel text-text hover:bg-surface-2 border-hairline">
                        <i class="fa-solid fa-tv"></i> TV Series
                    </button>
                </div>
            </div>
        </section>

        <div id="media-library-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 sm:gap-5 mb-8"></div>
        <div id="media-loading-state" class="hidden text-center py-16">
            <i class="fa-solid fa-spinner animate-spin text-3xl text-primary mb-3"></i>
            <p class="text-sm text-text-sec">Loading media library...</p>
        </div>
        <div id="media-empty-state" class="hidden text-center py-16">
            <div class="glass-panel rounded-3xl p-8 max-w-md mx-auto">
                <i class="fa-solid fa-film text-4xl text-muted mb-3"></i>
                <h3 class="text-lg font-bold text-text">No media found</h3>
                <p class="text-xs text-text-sec mt-1">Start by scanning your Telegram channels or adjust search query.</p>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: 1-CLICK UNMATCHED QUEUE -->
    <!-- ========================================== -->
    <div id="tab-unmatched" class="tab-pane hidden">
        <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
                <h2 class="text-2xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                    1-Click Unmatched Media Queue
                </h2>
                <p class="text-text-sec text-xs sm:text-sm mt-1">
                    Review items skipped during crawling. Search TMDB and bind them in 1-click with zero URL pasting.
                </p>
            </div>
            <button onclick="loadUnmatchedQueue()" class="px-4 py-2 rounded-xl bg-surface hover:bg-surface-2 text-text text-xs font-bold border border-hairline flex items-center gap-2 transition">
                <i class="fa-solid fa-arrow-rotate-right"></i> Refresh Queue
            </button>
        </div>

        <div id="unmatched-items-list" class="space-y-4"></div>
        <div id="unmatched-empty-state" class="hidden p-12 text-center rounded-[2rem] border border-emerald-500/30 bg-emerald-500/5">
            <div class="w-16 h-16 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/20">
                <i class="fa-solid fa-circle-check text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-text">Queue is clear!</h3>
            <p class="text-text-sec text-xs sm:text-sm mt-1">All channel video items have been successfully resolved and indexed.</p>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 4: BOTS -->
    <!-- ========================================== -->
    <div id="tab-bots" class="tab-pane hidden">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-1">
                <div class="glass-panel p-6 rounded-[2rem]">
                    <h3 class="text-lg font-bold text-text mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-robot text-primary"></i> Add Bot Worker
                    </h3>
                    <p class="text-xs text-text-sec mb-5">
                        Add secondary Telegram Bot Tokens from @BotFather. The engine stripes chunk downloads across all connected bots to multiply streaming speeds.
                    </p>

                    <div class="space-y-4">
                        <div>
                            <label class="text-xs font-bold uppercase tracking-wider text-text-sec block mb-1.5">Telegram Bot Token</label>
                            <input type="text" id="new-bot-token" placeholder="7123456789:AAH..." class="field font-mono text-xs">
                        </div>

                        <button onclick="addBotWorker()" class="w-full btn-primary py-3 rounded-xl flex items-center justify-center gap-2">
                            <i class="fa-solid fa-plus"></i> Connect Bot
                        </button>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-2">
                <div class="glass-panel p-6 rounded-[2rem]">
                    <div class="flex items-center justify-between mb-5">
                        <h3 class="text-lg font-bold text-text flex items-center gap-2">
                            <i class="fa-solid fa-network-wired text-primary"></i> Connected Bot Workers
                        </h3>
                        <span id="bot-tab-count" class="badge">0 Connected</span>
                    </div>

                    <div id="bots-list-container" class="space-y-3"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: TOOLS (CHANNEL SCANNER, RE-INDEX, DB CHECK, DUPLICATES) -->
    <!-- ========================================== -->
    <div id="tab-tools" class="tab-pane hidden">
        <div class="space-y-6">

            <!-- 1. Channel Scanner & Re-Index -->
            <div class="tool-card">
                <div class="flex items-center justify-between flex-wrap gap-2">
                    <h2 style="margin-bottom:0"><i class="fa-solid fa-satellite-dish"></i> Channel Scanner &amp; Re-Index</h2>
                    <span id="scan-status-pill" class="status-pill status-idle">Idle</span>
                </div>

                <p class="hint mt-3 mb-4">
                    Scan and index files from your configured Telegram channels. Scans resume automatically; use Rescan to wipe and re-index from scratch.
                </p>

                <label class="s-label">Select channels</label>
                <div class="flex flex-col gap-2 max-h-56 overflow-y-auto mb-3" id="tool-channels-list">
                    <div class="hint"><i class="fa-solid fa-spinner fa-spin"></i> Loading channels…</div>
                </div>

                <div class="flex items-center gap-2 mb-4">
                    <button class="btn-ghost px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5" type="button" onclick="selectAllScannerChannels(true)">
                        <i class="fa-solid fa-check-double"></i> Select all
                    </button>
                    <button class="btn-ghost px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5" type="button" onclick="selectAllScannerChannels(false)">
                        <i class="fa-solid fa-xmark"></i> Clear
                    </button>
                </div>

                <hr class="divider">

                <div class="flex items-center justify-between mb-2 flex-wrap gap-2">
                    <div class="text-sm font-bold" id="scan-current">No scan running</div>
                    <div class="text-sm text-text-sec">
                        <i class="fa-regular fa-clock"></i> <span id="scan-elapsed">0s</span>
                    </div>
                </div>
                <div class="progress-track mb-4">
                    <div class="progress-fill" id="scan-bar"></div>
                </div>

                <div class="stat-grid mb-4">
                    <div class="stat-box"><div class="v" id="sc-processed">0</div><div class="l">Processed</div></div>
                    <div class="stat-box"><div class="v text-emerald-400" id="sc-indexed">0</div><div class="l">Indexed</div></div>
                    <div class="stat-box"><div class="v" id="sc-dup">0</div><div class="l">Skipped (dup)</div></div>
                    <div class="stat-box"><div class="v text-rose-400" id="sc-errors">0</div><div class="l">Skipped (meta)</div></div>
                </div>

                <div class="flex items-center gap-2 flex-wrap">
                    <button class="btn-primary px-5 py-2.5 rounded-xl text-xs flex items-center gap-1.5" id="scan-start-btn" onclick="startScanner('scan')">
                        <i class="fa-solid fa-play"></i> Start Scan
                    </button>
                    <button class="btn-ghost px-5 py-2.5 rounded-xl text-xs flex items-center gap-1.5 border border-amber-500/40 text-amber-400" id="rescan-btn" onclick="startScanner('rescan')">
                        <i class="fa-solid fa-arrows-rotate"></i> Rescan (Wipe &amp; Re-index)
                    </button>
                </div>
            </div>

            <!-- 2. Manual Upload Session -->
            <div class="tool-card">
                <div class="flex items-center justify-between flex-wrap gap-2">
                    <h2 style="margin-bottom:0"><i class="fa-solid fa-cloud-arrow-up"></i> Manual Upload Session</h2>
                    <span id="ms-status-pill" class="status-pill status-idle">No session</span>
                </div>
                <p class="hint mt-3 mb-4">
                    Pick a title, start a session, then forward files to your channel — each video attaches automatically to that movie or series.
                </p>

                <!-- Active Session Banner -->
                <div id="ms-active-banner" class="hidden mb-4 p-4 rounded-2xl border border-emerald-500/30 bg-emerald-500/10">
                    <div class="flex items-center justify-between flex-wrap gap-2">
                        <div>
                            <div class="text-sm font-bold text-text" id="ms-active-title">—</div>
                            <div class="hint text-emerald-400">Session is active. Forward files to your channel now.</div>
                        </div>
                        <button class="px-3 py-1.5 rounded-xl bg-rose-500/20 text-rose-400 text-xs font-bold hover:bg-rose-500 hover:text-white transition" onclick="endManualSession()">
                            <i class="fa-solid fa-stop"></i> End Session
                        </button>
                    </div>
                </div>

                <div id="ms-setup-box">
                    <div class="flex flex-col sm:flex-row gap-2">
                        <input id="ms-search-input" placeholder="Title (e.g. Inception, Breaking Bad, or TMDB ID)..." class="field text-xs flex-1">
                        <button class="btn-primary px-4 py-2 rounded-xl text-xs flex items-center justify-center gap-1.5 shrink-0" onclick="searchManualTitle()">
                            <i class="fa-solid fa-magnifying-glass"></i> Find Title
                        </button>
                    </div>
                    <div id="ms-results-box" class="mt-3 space-y-2 hidden"></div>

                    <!-- Selected Preview -->
                    <div id="ms-selected-box" class="hidden mt-4 p-4 rounded-2xl border border-hairline bg-surface/40">
                        <div class="flex items-center gap-3">
                            <img id="ms-sel-poster" src="" class="w-10 h-14 object-cover rounded-lg shrink-0 bg-slate-900">
                            <div class="min-w-0 flex-1">
                                <h4 class="font-bold text-sm text-text truncate" id="ms-sel-title">—</h4>
                                <p class="text-xs text-text-sec" id="ms-sel-sub">—</p>
                            </div>
                        </div>
                        <button class="btn-primary mt-3 px-4 py-2 rounded-xl text-xs flex items-center gap-1.5" onclick="startManualSession()">
                            <i class="fa-solid fa-play"></i> Start Session
                        </button>
                    </div>
                </div>
            </div>

            <!-- 3. Database Check & Dead Links -->
            <div class="tool-card">
                <div class="flex items-center justify-between flex-wrap gap-2">
                    <h2 style="margin-bottom:0"><i class="fa-solid fa-stethoscope"></i> Database Check &amp; Dead Links</h2>
                    <span id="dbc-status-pill" class="status-pill status-idle">Idle</span>
                </div>
                <p class="hint mt-3 mb-4">
                    Verify indexed files still exist on Telegram, then purge dead entries.
                </p>

                <div class="stat-grid mb-4">
                    <div class="stat-box"><div class="v" id="dbc-checked">0</div><div class="l">Checked</div></div>
                    <div class="stat-box"><div class="v text-emerald-400" id="dbc-alive">0</div><div class="l">Alive</div></div>
                    <div class="stat-box"><div class="v text-rose-400" id="dbc-dead">0</div><div class="l">Dead</div></div>
                    <div class="stat-box"><div class="v" id="dbc-purged">0</div><div class="l">Purged</div></div>
                </div>

                <div class="flex items-center gap-2 flex-wrap">
                    <button class="btn-primary px-4 py-2 rounded-xl text-xs flex items-center gap-1.5" onclick="runDbCheck()">
                        <i class="fa-solid fa-play"></i> Run DB Check
                    </button>
                    <button class="btn-ghost px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 text-rose-400 border border-rose-500/30" onclick="purgeDeadLinks()">
                        <i class="fa-solid fa-trash"></i> Purge Dead Links
                    </button>
                </div>
            </div>

            <!-- 4. Duplicate Check & Cleanup -->
            <div class="tool-card">
                <div class="flex items-center justify-between flex-wrap gap-2">
                    <h2 style="margin-bottom:0"><i class="fa-solid fa-clone"></i> Duplicate Check &amp; Cleanup</h2>
                    <span id="dup-status-pill" class="status-pill status-idle">Idle</span>
                </div>
                <p class="hint mt-3 mb-4">
                    Find and remove streams stored more than once to keep the library compact and fast.
                </p>

                <div class="stat-grid mb-4">
                    <div class="stat-box"><div class="v" id="dup-scanned">0</div><div class="l">Scanned</div></div>
                    <div class="stat-box"><div class="v" id="dup-groups">0</div><div class="l">Groups</div></div>
                    <div class="stat-box"><div class="v text-amber-400" id="dup-count">0</div><div class="l">Redundant</div></div>
                </div>

                <div class="flex items-center gap-2 flex-wrap mb-4">
                    <button class="btn-primary px-4 py-2 rounded-xl text-xs flex items-center gap-1.5" onclick="scanDuplicates()">
                        <i class="fa-solid fa-magnifying-glass"></i> Scan for Duplicates
                    </button>
                    <button class="btn-ghost px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 text-rose-400 border border-rose-500/30" onclick="purgeDuplicates()">
                        <i class="fa-solid fa-broom"></i> Clean All Duplicates
                    </button>
                </div>

                <div id="dup-results-list" class="space-y-2 max-h-60 overflow-y-auto"></div>
            </div>

        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 6: TOKENS & ACCESS -->
    <!-- ========================================== -->
    <div id="tab-tokens" class="tab-pane hidden">
        <div class="glass-panel p-6 sm:p-8 rounded-[2rem] mb-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                    <h2 class="text-xl sm:text-2xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                        Stremio Tokens &amp; Access
                    </h2>
                    <p class="text-text-sec text-xs sm:text-sm mt-1">Generate personalized addon manifests with 1-click Stremio installation.</p>
                </div>

                <div class="flex items-center gap-2">
                    <input type="text" id="new-token-name" placeholder="User / Device Name" class="field py-2 text-xs w-48">
                    <button onclick="createNewToken()" class="btn-primary px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 shrink-0">
                        <i class="fa-solid fa-plus"></i> Add Token
                    </button>
                </div>
            </div>

            <div id="tokens-list-container" class="space-y-4"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 7: SETTINGS (EXACT MATCH OF OLD VERSION) -->
    <!-- ========================================== -->
    <div id="tab-settings" class="tab-pane hidden">
        <!-- Settings Header with Save button -->
        <div class="flex items-center justify-between mb-8">
            <div>
                <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Settings</h1>
                <p class="mt-1 text-xs sm:text-sm text-text-sec">
                    Runtime configuration — stored in the database, no restart needed.
                </p>
            </div>
            <button id="save-btn" onclick="saveSettings()"
                class="btn-primary flex items-center gap-2 px-6 py-2.5 rounded-full font-bold text-sm text-white shadow-lg transition-all">
                <i class="fa-solid fa-floppy-disk"></i>
                <span id="save-label">Save Settings</span>
            </button>
        </div>

        <div class="space-y-6">

            <!-- 1. System & Maintenance (With 1-Click Update from GitHub!) -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-server"></i> System &amp; Maintenance</h2>

                <!-- 1-Click Server Update Feature -->
                <div class="p-4 sm:p-5 rounded-2xl border border-primary/30 bg-primary/10 mb-5">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                            <h4 class="font-bold text-sm sm:text-base text-text flex items-center gap-2">
                                <i class="fa-brands fa-github text-primary"></i> Apply Latest GitHub Updates
                            </h4>
                            <p class="text-xs text-text-sec mt-1">
                                Pulls latest commits from your repository and reloads the container automatically — no SSH login needed!
                            </p>
                        </div>
                        <button id="server-update-btn" onclick="applyServerUpdate()" class="btn-primary px-5 py-2.5 rounded-xl text-xs font-bold flex items-center justify-center gap-2 shrink-0">
                            <i id="update-spinner" class="fa-solid fa-arrows-rotate"></i>
                            <span>Update &amp; Reload</span>
                        </button>
                    </div>
                    <div id="update-output-box" class="hidden mt-3 p-3 rounded-xl bg-black/60 font-mono text-xs text-slate-300 border border-hairline whitespace-pre-wrap"></div>
                </div>

                <!-- Database stats -->
                <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                    <label class="s-label" style="margin-bottom:0">Database &amp; System Stats</label>
                    <button class="btn-ghost px-3 py-1 rounded-xl text-xs" type="button" onclick="loadDbStats()">
                        <i class="fa-solid fa-rotate"></i> Refresh
                    </button>
                </div>
                <div class="stat-grid mb-5" id="settings-stats-grid">
                    <div class="stat-box"><div class="v" id="set-stat-media">0</div><div class="l">Total Media</div></div>
                    <div class="stat-box"><div class="v text-primary" id="set-stat-movies">0</div><div class="l">Movies</div></div>
                    <div class="stat-box"><div class="v text-accent" id="set-stat-series">0</div><div class="l">TV Shows</div></div>
                    <div class="stat-box"><div class="v" id="set-stat-bots">0</div><div class="l">Bots</div></div>
                </div>

                <hr class="divider">

                <!-- Live logs -->
                <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                    <label class="s-label" style="margin-bottom:0">Server Logs</label>
                    <div class="flex items-center gap-3 flex-wrap">
                        <label class="toggle-wrap text-xs">
                            <input type="checkbox" class="toggle-input" id="log-live-toggle" onchange="toggleLiveLogs()">
                            <span class="toggle-track"></span>
                            <span class="text-xs font-bold text-text-sec">Live</span>
                        </label>
                        <button class="btn-ghost px-3 py-1 rounded-xl text-xs" type="button" onclick="loadLogs()">
                            <i class="fa-solid fa-rotate"></i> Refresh
                        </button>
                        <button class="btn-ghost px-3 py-1 rounded-xl text-xs" type="button" onclick="window.open('/admin/api/system/logs/download','_blank')">
                            <i class="fa-solid fa-download"></i> Download
                        </button>
                    </div>
                </div>
                <pre id="log-view" class="bg-black/70 border border-border rounded-xl p-3 font-mono text-xs text-slate-300 max-h-64 overflow-y-auto whitespace-pre-wrap">Loading server logs…</pre>
            </div>

            <!-- 2. General -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-sliders"></i> General</h2>
                <div class="space-y-4">
                    <label class="toggle-wrap">
                        <input type="checkbox" class="toggle-input" id="replace_mode">
                        <span class="toggle-track"></span>
                        <span class="toggle-label">
                            <strong>Replace Mode</strong>
                            <span class="text-xs text-text-sec block">Overwrite existing media entries on re-index</span>
                        </span>
                    </label>
                    <label class="toggle-wrap">
                        <input type="checkbox" class="toggle-input" id="duplicate_protection">
                        <span class="toggle-track"></span>
                        <span class="toggle-label">
                            <strong>Duplicate Protection</strong>
                            <span class="text-xs text-text-sec block">Skip re-indexing a file that already exists (same name &amp; size)</span>
                        </span>
                    </label>
                    <label class="toggle-wrap">
                        <input type="checkbox" class="toggle-input" id="hide_catalog">
                        <span class="toggle-track"></span>
                        <span class="toggle-label">
                            <strong>Hide Catalog</strong>
                            <span class="text-xs text-text-sec block">Hide the public Stremio catalog from unauthenticated users</span>
                        </span>
                    </label>
                </div>
            </div>

            <!-- 3. Admin Authentication -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-shield-halved"></i> Admin Authentication</h2>
                <div class="grid-2 mb-4">
                    <div>
                        <label class="s-label" for="admin_username">Admin Username</label>
                        <input type="text" id="admin_username" class="s-input" value="admin">
                    </div>
                    <div>
                        <label class="s-label" for="admin_password">Admin Password</label>
                        <div class="relative">
                            <input type="password" id="admin_password" class="s-input pr-10" placeholder="Leave blank to keep current password">
                            <button type="button" onclick="togglePwdVisibility()" class="absolute right-3 top-1/2 -translate-y-1/2 text-text-sec">
                                <i class="fa-solid fa-eye" id="eye-icon"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <hr class="divider">

                <!-- Auth Channels -->
                <label class="s-label">AUTH_CHANNELS (Telegram Channels to Index)</label>
                <div class="multi-list-items" id="auth_channels_items"></div>
                <div class="flex gap-2">
                    <input type="text" id="auth_channels_new" class="s-input text-xs" placeholder="-100xxxxxxxxxx" onkeydown="if(event.key==='Enter'){event.preventDefault();addChannelChip('auth_channels')}">
                    <button class="btn-ghost px-4 py-2 rounded-xl text-xs font-bold shrink-0" onclick="addChannelChip('auth_channels')">+ Add Channel</button>
                </div>
            </div>

            <!-- 4. Media & Content -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-film"></i> Media &amp; Content</h2>
                <div class="grid-2 mb-4">
                    <div>
                        <label class="s-label" for="tmdb_api">TMDB API Key</label>
                        <input type="text" id="tmdb_api" class="s-input font-mono text-xs" placeholder="Your TMDB v3 API key">
                    </div>
                    <div>
                        <label class="s-label" for="tvdb_api">TVDB API Key</label>
                        <input type="text" id="tvdb_api" class="s-input font-mono text-xs" placeholder="TheTVDB v4 API key (series priority)">
                    </div>
                </div>
                <div class="mb-4">
                    <label class="s-label" for="base_url">Public Base URL</label>
                    <input type="url" id="base_url" class="s-input font-mono text-xs" placeholder="http://your-vm-ip:8000 or https://stremio.yourdomain.com">
                </div>
                <hr class="divider">
                <div class="grid-2">
                    <div>
                        <label class="s-label" for="upstream_repo">Upstream Repo</label>
                        <input type="text" id="upstream_repo" class="s-input font-mono text-xs" value="https://github.com/haarryyyyyyy/Telegram-Stremio-v2">
                    </div>
                    <div>
                        <label class="s-label" for="upstream_branch">Upstream Branch</label>
                        <input type="text" id="upstream_branch" class="s-input font-mono text-xs" value="main">
                    </div>
                </div>
            </div>

            <!-- 5. Poster Provider -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-image"></i> Poster Provider</h2>
                <p class="hint mb-4">Replace catalog posters with artwork from textless and high-res metadata providers.</p>

                <div class="space-y-4">
                    <div>
                        <label class="toggle-wrap">
                            <input type="checkbox" class="toggle-input" id="better_poster_enabled" onchange="document.getElementById('better-wrap').classList.toggle('hidden', !this.checked)">
                            <span class="toggle-track"></span>
                            <span class="toggle-label"><strong>BetterPoster (btttr.cc)</strong></span>
                        </label>
                        <div id="better-wrap" class="mt-2 hidden">
                            <input type="text" id="better_poster" class="s-input text-xs" placeholder="https://btttr.cc/poster/imdb/poster-default/{imdb_id}.jpg">
                        </div>
                    </div>

                    <div>
                        <label class="toggle-wrap">
                            <input type="checkbox" class="toggle-input" id="rpdb_enabled" onchange="document.getElementById('rpdb-wrap').classList.toggle('hidden', !this.checked)">
                            <span class="toggle-track"></span>
                            <span class="toggle-label"><strong>RPDB (RatingPosterDB)</strong></span>
                        </label>
                        <div id="rpdb-wrap" class="mt-2 hidden">
                            <input type="text" id="rpdb_api_key" class="s-input text-xs" placeholder="RPDB API Key (or empty for free tier)">
                        </div>
                    </div>

                    <div>
                        <label class="toggle-wrap">
                            <input type="checkbox" class="toggle-input" id="fanart_enabled" onchange="document.getElementById('fanart-wrap').classList.toggle('hidden', !this.checked)">
                            <span class="toggle-track"></span>
                            <span class="toggle-label"><strong>Fanart.tv Artwork</strong></span>
                        </label>
                        <div id="fanart-wrap" class="mt-2 hidden space-y-2">
                            <input type="text" id="fanart_api_key" class="s-input text-xs" placeholder="Fanart.tv Project API Key">
                            <label class="toggle-wrap">
                                <input type="checkbox" class="toggle-input" id="fanart_low_res_poster">
                                <span class="toggle-track"></span>
                                <span class="text-xs text-text-sec">Faster artwork (Optimized for mobile)</span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 6. Stream Formatter -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-wand-magic-sparkles"></i> Stream Formatter</h2>
                <p class="hint mb-4">How each stream's name and description look in Stremio.</p>
                <div class="space-y-3">
                    <div>
                        <label class="s-label">Preset Formatter</label>
                        <select id="stream_formatter" class="s-input text-xs">
                            <option value="default">Default (Built-in)</option>
                            <option value="prism">Prism</option>
                            <option value="tamtaro">Tamtaro</option>
                            <option value="gdrive">GDrive</option>
                            <option value="torrentio">Torrentio</option>
                        </select>
                    </div>
                    <div>
                        <label class="s-label">Name Template</label>
                        <input type="text" id="formatter_name" class="s-input font-mono text-xs" value="{stream.quality} {stream.resolution}">
                    </div>
                    <div>
                        <label class="s-label">Description Template</label>
                        <input type="text" id="formatter_description" class="s-input font-mono text-xs" value="⚡ {stream.releaseGroup} • {stream.size}">
                    </div>
                </div>
            </div>

            <!-- 7. Backup & Restore -->
            <div class="settings-card">
                <h2><i class="fa-solid fa-box-archive"></i> Backup &amp; Restore</h2>
                <p class="hint mb-4">Export all settings and token configurations to a JSON file.</p>
                <div class="flex items-center gap-3 flex-wrap">
                    <button onclick="exportBackup()" class="btn-ghost px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2">
                        <i class="fa-solid fa-download text-primary"></i> Export Backup JSON
                    </button>
                </div>
            </div>

        </div>
    </div>

</main>

<!-- Footer -->
<footer class="mt-auto w-full max-w-5xl mx-auto px-6 py-8">
    <div class="glass-panel rounded-3xl p-6 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-2">
            <i class="fa-brands fa-telegram text-primary text-xl"></i>
            <p class="text-text-sec text-xs">© 2026 Telegram Stremio • High-Performance Multi-Bot Engine</p>
        </div>
        <div class="flex items-center gap-3 text-xs text-text-sec">
            <span>Striped Multiplexer</span>
            <span>•</span>
            <span>TVDB &amp; TMDB v4</span>
            <span>•</span>
            <span class="text-emerald-400 font-semibold">1GB VM Optimized</span>
        </div>
    </div>
</footer>

<!-- Toast Notifications Container -->
<div id="toast-container"></div>

<script>
let currentTab = 'overview';
let activeMediaFilter = null;
let liveStreamsInterval = null;
let liveLogsInterval = null;
let streamState = { activeStreams: [] };
let cachedSettings = {};

function showToast(message, type = 'info', title = '', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-triangle-exclamation' : 'fa-circle-info');
    toast.innerHTML = `
        <i class="fa-solid ${icon} text-lg shrink-0"></i>
        <div class="min-w-0">
            ${title ? `<div class="font-bold text-xs uppercase tracking-wider mb-0.5">${escapeHtml(title)}</div>` : ''}
            <div class="text-xs text-slate-200">${escapeHtml(message)}</div>
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'toast-out 0.2s ease-in forwards';
        setTimeout(() => toast.remove(), 220);
    }, duration);
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function formatBytes(bytes) {
    const value = Number(bytes || 0);
    if (!value) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    const index = Math.min(Math.floor(Math.log(value) / Math.log(1024)), units.length - 1);
    return (value / Math.pow(1024, index)).toFixed(index === 0 ? 0 : 2) + ' ' + units[index];
}

function formatDuration(seconds) {
    const total = Math.floor(Math.max(0, Number(seconds || 0)));
    const h = Math.floor(total / 3600);
    const m = Math.floor((total % 3600) / 60);
    const s = total % 60;
    if (h > 0) return `${h}h ${m}m ${s}s`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
}

function switchTab(tabId, filter = null) {
    currentTab = tabId;
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById('tab-' + tabId);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.classList.toggle('pill-active', btn.getAttribute('data-tab') === tabId);
    });

    if (tabId === 'overview') {
        refreshDashboard();
    } else if (tabId === 'media') {
        setMediaFilter(filter);
    } else if (tabId === 'unmatched') {
        loadUnmatchedQueue();
    } else if (tabId === 'bots') {
        loadBots();
    } else if (tabId === 'tools') {
        loadTools();
    } else if (tabId === 'tokens') {
        loadTokens();
    } else if (tabId === 'settings') {
        loadSettings();
    }
}

function toggleMobileNav() {
    const menu = document.getElementById('mobile-menu');
    const icon = document.getElementById('mobile-toggle-icon');
    if (menu) {
        menu.classList.toggle('hidden');
        if (icon) {
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-xmark');
        }
    }
}

// ==========================================
// OVERVIEW & SYSTEM STATS
// ==========================================
async function refreshDashboard() {
    const gIcon = document.getElementById('global-refresh-icon');
    const oIcon = document.getElementById('overview-refresh-icon');
    if (gIcon) gIcon.classList.add('animate-spin');
    if (oIcon) oIcon.classList.add('animate-spin');

    try {
        const res = await fetch('/admin/api/stats');
        if (res.ok) {
            const data = await res.json();
            document.getElementById('sys-uptime').textContent = data.uptime || 'Active';
            document.getElementById('sys-bots-count').textContent = (data.connected_bots || 0) + ' Nodes';
            document.getElementById('sys-live-streams').textContent = (data.total_active_streams || 0) + ' Active';
            document.getElementById('sys-version').textContent = 'v' + (data.version || '2.0.0');

            document.getElementById('db-media-counts').textContent = `${data.movies || 0} / ${data.series || 0}`;
            document.getElementById('db-total-media').textContent = String(data.total_media || 0);

            const storageMb = Math.round((data.total_media || 0) * 0.35);
            document.getElementById('db-storage-size').textContent = `~${storageMb} MB`;

            document.getElementById('quick-unmatched-badge').textContent = String(data.unmatched || 0);
            const navBadge = document.getElementById('nav-unmatched-badge');
            if (navBadge) {
                navBadge.textContent = String(data.unmatched || 0);
                navBadge.classList.toggle('hidden', (data.unmatched || 0) === 0);
            }

            const botBadge = document.getElementById('nav-bot-count');
            if (botBadge) botBadge.textContent = String(data.connected_bots || 0);
        }

        await loadLiveStreams();
    } catch (e) {
        console.error('Error refreshing dashboard:', e);
    } finally {
        setTimeout(() => {
            if (gIcon) gIcon.classList.remove('animate-spin');
            if (oIcon) oIcon.classList.remove('animate-spin');
        }, 500);
    }
}

async function loadLiveStreams() {
    try {
        const res = await fetch('/admin/api/streams');
        if (!res.ok) return;
        const data = await res.json();
        const active = data.active_streams || [];
        const recent = data.recent_streams || [];
        streamState.activeStreams = active;

        document.getElementById('live-stream-count').textContent = active.length + ' Active';
        document.getElementById('live-now-count').textContent = String(active.length);
        document.getElementById('recent-stream-count').textContent = String(recent.length);

        const container = document.getElementById('active-streams-container');
        if (!container) return;

        if (!active.length) {
            container.innerHTML = `
                <div class="glass-panel p-8 rounded-[2rem] text-center border-dashed border-hairline">
                    <i class="fa-solid fa-satellite-dish text-4xl text-muted mb-3"></i>
                    <p class="text-sm text-text-sec font-medium">No active streams right now</p>
                    <p class="text-xs text-text-sec mt-1">The live network is idle at the moment.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = active.map(s => {
            const title = escapeHtml(s.title || s.file_name || 'Stream');
            const fileName = escapeHtml(s.file_name || '');
            const speed = s.avg_mbps ? s.avg_mbps.toFixed(3) + ' MB/s' : '—';
            const total = formatBytes(s.total_bytes || 0);

            return `
                <div class="stream-card p-5 min-w-0 max-w-full overflow-hidden">
                    <div class="flex justify-between items-start gap-3 min-w-0">
                        <div class="min-w-0 flex-1 pr-2">
                            <h5 class="font-bold text-sm text-text truncate" title="${title}">${title}</h5>
                            ${fileName ? `<p class="text-[10px] text-text-sec truncate leading-tight mt-0.5">${fileName}</p>` : ''}
                            <div class="mt-2 flex flex-wrap items-center gap-1.5 text-[10px] uppercase tracking-wider">
                                <span class="inline-flex items-center gap-1 font-bold px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                    <i class="fa-solid fa-robot text-[9px]"></i> Bot ${(s.client_index || 0) + 1}
                                </span>
                                <span class="text-text-sec font-mono text-[9px]">DC ${s.dc_id || 4}</span>
                            </div>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-1 rounded-lg uppercase stream-badge-live shrink-0">Live</span>
                    </div>

                    <div class="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-hairline">
                        <div class="text-center">
                            <p class="text-[9px] text-text-sec uppercase font-bold">Speed</p>
                            <p class="text-xs font-bold text-text truncate">${speed}</p>
                        </div>
                        <div class="text-center">
                            <p class="text-[9px] text-text-sec uppercase font-bold">Transferred</p>
                            <p class="text-xs font-bold text-text truncate">${total}</p>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('Error loading streams:', e);
    }
}

// ==========================================
// MEDIA LIBRARY
// ==========================================
function setMediaFilter(type) {
    activeMediaFilter = type;
    document.getElementById('filter-all-btn').className = !type ?
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border bg-primary text-white border-primary shadow-lg shadow-primary/20' :
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border glass-panel text-text hover:bg-surface-2 border-hairline';
    document.getElementById('filter-movies-btn').className = type === 'movie' ?
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border bg-primary text-white border-primary shadow-lg shadow-primary/20' :
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border glass-panel text-text hover:bg-surface-2 border-hairline';
    document.getElementById('filter-tv-btn').className = type === 'tv' ?
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border bg-primary text-white border-primary shadow-lg shadow-primary/20' :
        'inline-flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-bold transition border glass-panel text-text hover:bg-surface-2 border-hairline';

    loadMediaLibrary();
}

async function loadMediaLibrary() {
    const grid = document.getElementById('media-library-grid');
    const loading = document.getElementById('media-loading-state');
    const empty = document.getElementById('media-empty-state');
    const search = document.getElementById('media-search-input').value.trim();

    grid.innerHTML = '';
    loading.classList.remove('hidden');
    empty.classList.add('hidden');

    try {
        let url = `/admin/api/media?limit=60`;
        if (activeMediaFilter) url += `&media_type=${activeMediaFilter}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;

        const res = await fetch(url);
        loading.classList.add('hidden');
        if (!res.ok) throw new Error('Failed to load media');
        const data = await res.json();
        const items = data.items || [];

        if (!items.length) {
            empty.classList.remove('hidden');
            return;
        }

        grid.innerHTML = items.map(m => {
            const title = escapeHtml(m.title || 'Untitled');
            const poster = m.poster || 'https://via.placeholder.com/300x450/111827/6366f1?text=No+Poster';
            const year = m.year || '';
            const quality = escapeHtml(m.quality || 'HD');
            const mediaType = m.media_type === 'tv' ? 'TV' : 'Movie';

            return `
                <div class="glass-panel rounded-2xl overflow-hidden group hover:border-primary/40 transition duration-300 flex flex-col">
                    <div class="relative aspect-[2/3] overflow-hidden bg-slate-900">
                        <img src="${poster}" alt="${title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                        <div class="absolute top-2 left-2 flex items-center gap-1">
                            <span class="px-2 py-0.5 rounded text-[10px] font-black bg-black/70 text-white backdrop-blur border border-white/10 uppercase">${mediaType}</span>
                            <span class="px-2 py-0.5 rounded text-[10px] font-black bg-primary/80 text-white backdrop-blur uppercase">${quality}</span>
                        </div>
                    </div>
                    <div class="p-3.5 flex flex-col flex-1 justify-between">
                        <div>
                            <h4 class="font-bold text-xs sm:text-sm text-text truncate" title="${title}">${title}</h4>
                            <p class="text-[10px] text-text-sec mt-0.5">${year ? year : '—'}</p>
                        </div>
                        <div class="mt-3 pt-2.5 border-t border-hairline flex items-center justify-between">
                            <span class="text-[10px] text-text-sec font-mono truncate">${formatBytes(m.file_size || 0)}</span>
                            <button onclick="deleteMediaItem('${m.id || m._id}')" title="Delete" class="w-7 h-7 rounded-lg hover:bg-rose-500/10 text-rose-400 flex items-center justify-center transition">
                                <i class="fa-solid fa-trash text-xs"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        loading.classList.add('hidden');
        showToast('Error loading media library: ' + e.message, 'error', 'Error');
    }
}

async function deleteMediaItem(mediaId) {
    if (!confirm('Are you sure you want to delete this media item?')) return;
    try {
        const res = await fetch(`/admin/api/media/${mediaId}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Item deleted successfully', 'success', 'Deleted');
            loadMediaLibrary();
            refreshDashboard();
        } else {
            showToast('Failed to delete item', 'error', 'Error');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Delete error');
    }
}

// ==========================================
// 1-CLICK UNMATCHED QUEUE
// ==========================================
async function loadUnmatchedQueue() {
    const list = document.getElementById('unmatched-items-list');
    const empty = document.getElementById('unmatched-empty-state');
    if (!list) return;

    list.innerHTML = '<div class="text-center py-12"><i class="fa-solid fa-spinner animate-spin text-2xl text-primary"></i></div>';
    empty.classList.add('hidden');

    try {
        const res = await fetch('/admin/api/unmatched');
        if (!res.ok) throw new Error('Failed to load queue');
        const data = await res.json();
        const items = data.items || [];

        if (!items.length) {
            list.innerHTML = '';
            empty.classList.remove('hidden');
            return;
        }

        list.innerHTML = items.map(item => {
            const rawTitle = escapeHtml(item.parsed_title || item.filename || 'Unknown File');
            const cleanId = item.id;

            return `
                <div class="glass-panel p-5 rounded-2xl border border-hairline" id="queue-card-${cleanId}">
                    <div class="flex flex-col lg:flex-row justify-between gap-4">
                        <div class="min-w-0 flex-1">
                            <div class="flex items-center gap-2 mb-1 flex-wrap">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-primary/15 text-primary border border-primary/25 uppercase">${escapeHtml(item.quality || 'HD')}</span>
                                <span class="text-xs text-text-sec">Chat: ${item.chat_id} • Msg: ${item.message_id}</span>
                                <span class="text-xs text-text-sec font-mono">${formatBytes(item.file_size)}</span>
                            </div>
                            <h4 class="text-base font-bold text-text truncate" title="${rawTitle}">${rawTitle}</h4>
                            ${item.filename !== rawTitle ? `<p class="text-xs text-text-sec font-mono truncate mt-0.5">${escapeHtml(item.filename)}</p>` : ''}
                        </div>

                        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 shrink-0">
                            <input type="text" id="tmdb-search-input-${cleanId}" value="${rawTitle}" placeholder="Search TMDB..." class="field text-xs sm:w-60">
                            <button onclick="searchTmdbForQueue('${cleanId}')" class="btn-ghost px-4 py-2 text-xs flex items-center justify-center gap-1.5 shrink-0">
                                <i class="fa-solid fa-magnifying-glass"></i> Search
                            </button>
                        </div>
                    </div>

                    <div id="tmdb-results-${cleanId}" class="mt-4 pt-4 border-t border-hairline hidden">
                        <p class="text-xs font-bold text-text-sec uppercase tracking-wider mb-3">Select Matching TMDB Title:</p>
                        <div id="tmdb-results-grid-${cleanId}" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        list.innerHTML = '<div class="text-center py-8 text-rose-400">Failed to load unmatched queue.</div>';
    }
}

async function searchTmdbForQueue(cleanId) {
    const input = document.getElementById(`tmdb-search-input-${cleanId}`);
    const resultsBox = document.getElementById(`tmdb-results-${cleanId}`);
    const resultsGrid = document.getElementById(`tmdb-results-grid-${cleanId}`);
    if (!input || !resultsBox || !resultsGrid) return;

    const query = input.value.trim();
    if (!query) return;

    resultsBox.classList.remove('hidden');
    resultsGrid.innerHTML = '<div class="col-span-full text-center py-4 text-xs text-text-sec"><i class="fa-solid fa-spinner animate-spin text-primary mr-1"></i> Searching TMDB...</div>';

    try {
        const res = await fetch(`/admin/api/search-tmdb?query=${encodeURIComponent(query)}&type=movie`);
        const data = await res.json();
        const results = data.results || [];

        if (!results.length) {
            resultsGrid.innerHTML = '<div class="col-span-full text-center py-4 text-xs text-text-sec">No matching titles found on TMDB.</div>';
            return;
        }

        resultsGrid.innerHTML = results.map(r => `
            <div class="p-3 rounded-xl border border-hairline bg-surface flex items-center gap-3 hover:border-primary/40 transition">
                <img src="${r.poster || 'https://via.placeholder.com/60x90'}" class="w-10 h-14 object-cover rounded-lg shrink-0">
                <div class="min-w-0 flex-1">
                    <h5 class="font-bold text-xs text-text truncate" title="${escapeHtml(r.title)}">${escapeHtml(r.title)}</h5>
                    <p class="text-[10px] text-text-sec">${r.year || ''} • TMDB ${r.id}</p>
                    <button onclick="bindQueueItem('${cleanId}', ${r.id}, 'movie', '${escapeHtml(r.title)}', ${r.year || 'null'})" class="mt-1.5 btn-primary px-3 py-1 text-[10px] rounded-lg">
                        <i class="fa-solid fa-link"></i> Match
                    </button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        resultsGrid.innerHTML = '<div class="col-span-full text-center py-4 text-xs text-rose-400">Search error.</div>';
    }
}

async function bindQueueItem(unmatchedId, tmdbId, mediaType, title, year) {
    try {
        const res = await fetch('/admin/api/match', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                unmatched_id: unmatchedId,
                tmdb_id: tmdbId,
                media_type: mediaType,
                canonical_title: title,
                year: year
            })
        });

        if (res.ok) {
            showToast(`Matched "${title}" successfully!`, 'success', 'Matched');
            const card = document.getElementById(`queue-card-${unmatchedId}`);
            if (card) card.remove();
            refreshDashboard();
        } else {
            showToast('Failed to bind match.', 'error', 'Error');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Match error');
    }
}

// ==========================================
// BOT CLUSTER
// ==========================================
async function loadBots() {
    const list = document.getElementById('bots-list-container');
    const badge = document.getElementById('bot-tab-count');
    if (!list) return;

    try {
        const res = await fetch('/admin/api/bots');
        if (!res.ok) return;
        const data = await res.json();
        const bots = data.bots || [];

        if (badge) badge.textContent = `${bots.length} Connected`;

        if (!bots.length) {
            list.innerHTML = '<p class="text-xs text-text-sec">No secondary bots added yet. Add tokens on the left.</p>';
            return;
        }

        list.innerHTML = bots.map((b, idx) => `
            <div class="p-4 rounded-2xl border border-hairline bg-surface/50 flex items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary font-bold">
                        #${idx + 1}
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="font-bold text-sm text-text">Bot Worker ${idx + 1}</span>
                            <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">Online</span>
                        </div>
                        <p class="text-xs text-text-sec font-mono mt-0.5">${escapeHtml(b.masked)}</p>
                    </div>
                </div>

                <button onclick="removeBotWorker('${escapeHtml(b.token)}')" class="px-3 py-1.5 rounded-xl text-xs font-bold text-rose-400 bg-rose-500/10 hover:bg-rose-500 hover:text-white transition">
                    Remove
                </button>
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading bots:', e);
    }
}

async function addBotWorker() {
    const input = document.getElementById('new-bot-token');
    const token = input.value.trim();
    if (!token) return;

    try {
        const res = await fetch('/admin/api/bots', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });
        if (res.ok) {
            showToast('Bot connected to cluster', 'success', 'Bot Added');
            input.value = '';
            loadBots();
            refreshDashboard();
        } else {
            showToast('Failed to add bot worker', 'error', 'Error');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Error');
    }
}

async function removeBotWorker(token) {
    if (!confirm('Remove this bot from the cluster?')) return;
    try {
        const res = await fetch('/admin/api/bots/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });
        if (res.ok) {
            showToast('Bot removed', 'success', 'Removed');
            loadBots();
            refreshDashboard();
        }
    } catch (e) {
        showToast(e.message, 'error', 'Error');
    }
}

// ==========================================
// TOOLS & RE-INDEX
// ==========================================
async function loadTools() {
    loadChannelsForScanner();
    loadScannerStatus();
    checkManualSessionStatus();
}

async function loadChannelsForScanner() {
    const list = document.getElementById('tool-channels-list');
    if (!list) return;

    try {
        const res = await fetch('/admin/api/channels');
        if (!res.ok) return;
        const data = await res.json();
        const channels = data.channels || [];

        if (!channels.length) {
            list.innerHTML = '<p class="text-xs text-text-sec">No channels configured. Add channel IDs in Settings.</p>';
            return;
        }

        list.innerHTML = channels.map(c => `
            <label class="flex items-center gap-3 p-3 rounded-xl border border-hairline bg-surface/40 hover:border-primary/40 cursor-pointer transition">
                <input type="checkbox" value="${escapeHtml(c.id)}" checked class="scanner-channel-check w-4 h-4 rounded accent-indigo-500">
                <span class="text-xs font-bold text-text">${escapeHtml(c.name)}</span>
                <span class="text-[10px] text-text-sec font-mono ml-auto">${escapeHtml(c.id)}</span>
            </label>
        `).join('');
    } catch (e) {
        list.innerHTML = '<p class="text-xs text-rose-400">Error loading channels.</p>';
    }
}

function selectAllScannerChannels(check) {
    document.querySelectorAll('.scanner-channel-check').forEach(el => el.checked = check);
}

async function startScanner(mode = 'scan') {
    const checked = Array.from(document.querySelectorAll('.scanner-channel-check:checked')).map(el => el.value);
    if (!checked.length) {
        showToast('Please select at least one channel to scan.', 'error', 'No Channels');
        return;
    }

    try {
        const res = await fetch('/admin/api/reindex', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ channels: checked })
        });
        if (res.ok) {
            showToast(`Channel ${mode} started in background`, 'success', 'Scanner Started');
            loadScannerStatus();
        } else {
            showToast('Failed to start channel scanner.', 'error', 'Error');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Scanner Error');
    }
}

async function loadScannerStatus() {
    try {
        const res = await fetch('/admin/api/reindex/status');
        if (!res.ok) return;
        const data = await res.json();

        const pill = document.getElementById('scan-status-pill');
        if (pill) {
            pill.textContent = data.status || 'Idle';
            pill.className = 'status-pill ' + (data.status === 'running' ? 'status-running' : 'status-idle');
        }

        document.getElementById('sc-processed').textContent = String(data.scanned || 0);
        document.getElementById('sc-indexed').textContent = String(data.matched || 0);
        document.getElementById('sc-errors').textContent = String(data.unmatched || 0);

        const total = (data.scanned || 0);
        const percent = total > 0 ? Math.min(100, Math.round(((data.matched || 0) / total) * 100)) : 0;
        document.getElementById('scan-bar').style.width = percent + '%';
        document.getElementById('scan-current').textContent = data.status === 'running' ? `Scanning... (${data.scanned} scanned)` : 'Scan Idle';
    } catch (e) {}
}

// Manual Session
let currentManualSelected = null;

async function checkManualSessionStatus() {
    try {
        const res = await fetch('/admin/api/tools/manual-session');
        if (!res.ok) return;
        const data = await res.json();
        const session = data.session;
        const pill = document.getElementById('ms-status-pill');
        const banner = document.getElementById('ms-active-banner');
        const setup = document.getElementById('ms-setup-box');

        if (session && session.title) {
            pill.textContent = 'Active Session';
            pill.className = 'status-pill status-running';
            banner.classList.remove('hidden');
            setup.classList.add('hidden');
            document.getElementById('ms-active-title').textContent = `${session.title} (${session.media_type.toUpperCase()}) • TMDB ${session.tmdb_id}`;
        } else {
            pill.textContent = 'No session';
            pill.className = 'status-pill status-idle';
            banner.classList.add('hidden');
            setup.classList.remove('hidden');
        }
    } catch (e) {}
}

async function searchManualTitle() {
    const query = document.getElementById('ms-search-input').value.trim();
    const box = document.getElementById('ms-results-box');
    if (!query || !box) return;

    box.classList.remove('hidden');
    box.innerHTML = '<div class="text-xs text-text-sec"><i class="fa-solid fa-spinner animate-spin text-primary mr-1"></i> Searching...</div>';

    try {
        const res = await fetch('/admin/api/tools/manual-session/search?query=' + encodeURIComponent(query));
        const data = await res.json();
        const results = data.results || [];

        if (!results.length) {
            box.innerHTML = '<div class="text-xs text-text-sec">No titles found. Try searching for a movie or TV show.</div>';
            return;
        }

        box.innerHTML = results.map(r => `
            <div class="flex items-center gap-3 p-2.5 rounded-xl border border-hairline bg-surface/50 hover:border-primary/40 cursor-pointer transition"
                 onclick='pickManualTitle(${JSON.stringify(r).replace(/'/g, "&apos;")})'>
                <img src="${r.poster || 'https://via.placeholder.com/60x90'}" class="w-8 h-12 object-cover rounded-md shrink-0">
                <div class="min-w-0 flex-1">
                    <h5 class="font-bold text-xs text-text truncate">${escapeHtml(r.title)}</h5>
                    <p class="text-[10px] text-text-sec">${r.year || ''} • ${r.media_type.toUpperCase()}</p>
                </div>
            </div>
        `).join('');
    } catch (e) {
        box.innerHTML = '<div class="text-xs text-rose-400">Search error.</div>';
    }
}

function pickManualTitle(item) {
    currentManualSelected = item;
    document.getElementById('ms-results-box').classList.add('hidden');
    const selBox = document.getElementById('ms-selected-box');
    selBox.classList.remove('hidden');
    document.getElementById('ms-sel-poster').src = item.poster || 'https://via.placeholder.com/60x90';
    document.getElementById('ms-sel-title').textContent = item.title;
    document.getElementById('ms-sel-sub').textContent = `${item.year || ''} • ${item.media_type.toUpperCase()} • TMDB ${item.tmdb_id}`;
}

async function startManualSession() {
    if (!currentManualSelected) return;
    try {
        const res = await fetch('/admin/api/tools/manual-session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tmdb_id: currentManualSelected.tmdb_id,
                title: currentManualSelected.title,
                media_type: currentManualSelected.media_type
            })
        });
        if (res.ok) {
            showToast('Manual upload session started!', 'success', 'Session Live');
            checkManualSessionStatus();
        }
    } catch (e) {
        showToast(e.message, 'error', 'Error');
    }
}

async function endManualSession() {
    try {
        await fetch('/admin/api/tools/manual-session/stop', { method: 'POST' });
        showToast('Manual upload session ended', 'info', 'Session Ended');
        checkManualSessionStatus();
    } catch (e) {}
}

// DB Check
async function runDbCheck() {
    const pill = document.getElementById('dbc-status-pill');
    if (pill) {
        pill.textContent = 'Running';
        pill.className = 'status-pill status-running';
    }
    try {
        const res = await fetch('/admin/api/tools/db-check', { method: 'POST' });
        const data = await res.json();
        document.getElementById('dbc-checked').textContent = String(data.checked || 0);
        document.getElementById('dbc-alive').textContent = String(data.alive || 0);
        document.getElementById('dbc-dead').textContent = String(data.dead || 0);
        document.getElementById('dbc-purged').textContent = String(data.purged || 0);
        showToast('Database integrity check finished', 'success', 'Check Complete');
    } catch (e) {
        showToast(e.message, 'error', 'Check failed');
    } finally {
        if (pill) {
            pill.textContent = 'Idle';
            pill.className = 'status-pill status-idle';
        }
    }
}

async function purgeDeadLinks() {
    if (!confirm('Purge all dead link entries from the database?')) return;
    try {
        const res = await fetch('/admin/api/tools/purge-dead', { method: 'POST' });
        showToast('Dead links purged successfully', 'success', 'Purged');
        runDbCheck();
    } catch (e) {
        showToast(e.message, 'error', 'Purge failed');
    }
}

// Duplicates
async function scanDuplicates() {
    const pill = document.getElementById('dup-status-pill');
    const list = document.getElementById('dup-results-list');
    if (pill) {
        pill.textContent = 'Scanning';
        pill.className = 'status-pill status-running';
    }
    list.innerHTML = '<div class="text-xs text-text-sec"><i class="fa-solid fa-spinner animate-spin text-primary mr-1"></i> Scanning database for duplicate entries...</div>';

    try {
        const res = await fetch('/admin/api/tools/duplicates', { method: 'POST' });
        const data = await res.json();
        document.getElementById('dup-scanned').textContent = String(data.scanned || 0);
        document.getElementById('dup-groups').textContent = String(data.groups || 0);
        document.getElementById('dup-count').textContent = String(data.redundant || 0);

        if (!data.items || !data.items.length) {
            list.innerHTML = '<div class="text-xs text-emerald-400"><i class="fa-solid fa-circle-check mr-1"></i> No duplicate video items found. Library is clean!</div>';
        } else {
            list.innerHTML = data.items.map(g => `
                <div class="p-3 rounded-xl border border-hairline bg-surface/40 flex items-center justify-between text-xs">
                    <div>
                        <span class="font-bold text-text">${escapeHtml(g.key)}</span>
                        <span class="text-amber-400 font-bold ml-2">(${g.count} copies)</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (e) {
        list.innerHTML = '<div class="text-xs text-rose-400">Scan failed.</div>';
    } finally {
        if (pill) {
            pill.textContent = 'Idle';
            pill.className = 'status-pill status-idle';
        }
    }
}

async function purgeDuplicates() {
    if (!confirm('Remove duplicate stream entries? This keeps the newest version of each duplicate.')) return;
    try {
        const res = await fetch('/admin/api/tools/duplicates/purge', { method: 'POST' });
        showToast('Duplicate cleaning completed', 'success', 'Cleaned');
        scanDuplicates();
    } catch (e) {
        showToast(e.message, 'error', 'Purge error');
    }
}

// ==========================================
// TOKENS & ACCESS
// ==========================================
async function loadTokens() {
    const list = document.getElementById('tokens-list-container');
    if (!list) return;

    try {
        const res = await fetch('/admin/api/tokens');
        if (!res.ok) return;
        const data = await res.json();
        const tokens = data.tokens || [];

        if (!tokens.length) {
            list.innerHTML = '<p class="text-xs text-text-sec">No user tokens generated yet. Create one above.</p>';
            return;
        }

        list.innerHTML = tokens.map(t => `
            <div class="glass-panel p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 border border-hairline">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="font-bold text-sm text-text">${escapeHtml(t.name)}</span>
                        <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">${escapeHtml(t.token)}</span>
                    </div>
                    <p class="text-xs text-text-sec font-mono mt-1 break-all">${escapeHtml(t.manifest_url)}</p>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                    <a href="${escapeHtml(t.stremio_install_url)}" class="btn-primary px-4 py-2 text-xs flex items-center gap-1.5">
                        <i class="fa-solid fa-download"></i> Install in Stremio
                    </a>
                    <button onclick="navigator.clipboard.writeText('${escapeHtml(t.manifest_url)}'); showToast('Manifest URL copied!', 'success', 'Copied')" class="btn-ghost px-3 py-2 text-xs">
                        <i class="fa-solid fa-copy"></i> Copy
                    </button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error('Error loading tokens:', e);
    }
}

async function createNewToken() {
    const input = document.getElementById('new-token-name');
    const name = input.value.trim() || 'User';

    try {
        const res = await fetch('/admin/api/tokens', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        if (res.ok) {
            showToast('Token created successfully!', 'success', 'Created');
            input.value = '';
            loadTokens();
        }
    } catch (e) {
        showToast(e.message, 'error', 'Error');
    }
}

// ==========================================
// SETTINGS
// ==========================================
async function loadSettings() {
    loadDbStats();
    loadLogs();

    try {
        const res = await fetch('/admin/api/settings');
        if (!res.ok) return;
        const data = await res.json();
        cachedSettings = data;

        document.getElementById('replace_mode').checked = !!data.replace_mode;
        document.getElementById('duplicate_protection').checked = data.duplicate_protection !== false;
        document.getElementById('hide_catalog').checked = !!data.hide_catalog;

        document.getElementById('admin_username').value = data.admin_username || 'admin';
        document.getElementById('tmdb_api').value = data.tmdb_api || data.tmdb_api_key || '';
        document.getElementById('tvdb_api').value = data.tvdb_api || data.tvdb_api_key || '';
        document.getElementById('base_url').value = data.base_url || '';
        document.getElementById('upstream_repo').value = data.upstream_repo || 'https://github.com/haarryyyyyyy/Telegram-Stremio-v2';
        document.getElementById('upstream_branch').value = data.upstream_branch || 'main';

        document.getElementById('better_poster_enabled').checked = !!data.better_poster_enabled;
        document.getElementById('better_poster').value = data.better_poster || '';
        document.getElementById('better-wrap').classList.toggle('hidden', !data.better_poster_enabled);

        document.getElementById('rpdb_enabled').checked = !!data.rpdb_enabled;
        document.getElementById('rpdb_api_key').value = data.rpdb_api_key || '';
        document.getElementById('rpdb-wrap').classList.toggle('hidden', !data.rpdb_enabled);

        document.getElementById('fanart_enabled').checked = !!data.fanart_enabled;
        document.getElementById('fanart_api_key').value = data.fanart_api_key || '';
        document.getElementById('fanart_low_res_poster').checked = data.fanart_low_res_poster !== false;
        document.getElementById('fanart-wrap').classList.toggle('hidden', !data.fanart_enabled);

        document.getElementById('stream_formatter').value = data.stream_formatter || 'default';
        document.getElementById('formatter_name').value = data.formatter_name || '{stream.quality} {stream.resolution}';
        document.getElementById('formatter_description').value = data.formatter_description || '⚡ {stream.releaseGroup} • {stream.size}';

        renderChannelChips(data.auth_channels || data.channels || []);
    } catch (e) {
        console.error('Error loading settings:', e);
    }
}

function renderChannelChips(channels) {
    const container = document.getElementById('auth_channels_items');
    if (!container) return;
    container.innerHTML = channels.map(ch => `
        <div class="multi-item">
            <span class="channel-chip">${escapeHtml(String(ch))}</span>
            <button class="remove-btn" onclick="removeChannelChip(this, '${ch}')">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
    `).join('');
}

function addChannelChip(type) {
    const input = document.getElementById(type + '_new');
    const val = input.value.trim();
    if (!val) return;
    const channels = cachedSettings.auth_channels || cachedSettings.channels || [];
    if (!channels.includes(val)) {
        channels.push(val);
        cachedSettings.auth_channels = channels;
        cachedSettings.channels = channels;
        renderChannelChips(channels);
    }
    input.value = '';
}

function removeChannelChip(btn, ch) {
    const channels = cachedSettings.auth_channels || cachedSettings.channels || [];
    const idx = channels.indexOf(ch);
    if (idx !== -1) {
        channels.splice(idx, 1);
        cachedSettings.auth_channels = channels;
        cachedSettings.channels = channels;
        renderChannelChips(channels);
    }
}

function togglePwdVisibility() {
    const input = document.getElementById('admin_password');
    const icon = document.getElementById('eye-icon');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

async function loadDbStats() {
    try {
        const res = await fetch('/admin/api/stats');
        const data = await res.json();
        document.getElementById('set-stat-media').textContent = String(data.total_media || 0);
        document.getElementById('set-stat-movies').textContent = String(data.movies || 0);
        document.getElementById('set-stat-series').textContent = String(data.series || 0);
        document.getElementById('set-stat-bots').textContent = String(data.connected_bots || 0);
    } catch (e) {}
}

async function loadLogs() {
    try {
        const res = await fetch('/admin/api/system/logs');
        const data = await res.json();
        const pre = document.getElementById('log-view');
        if (pre) {
            pre.textContent = data.raw || 'No logs recorded.';
            pre.scrollTop = pre.scrollHeight;
        }
    } catch (e) {}
}

function toggleLiveLogs() {
    const chk = document.getElementById('log-live-toggle');
    if (chk && chk.checked) {
        loadLogs();
        liveLogsInterval = setInterval(loadLogs, 2500);
    } else {
        clearInterval(liveLogsInterval);
    }
}

// 1-Click Server Update Feature
async function applyServerUpdate() {
    if (!confirm('Pull latest updates from GitHub and reload the server?')) return;
    const btn = document.getElementById('server-update-btn');
    const icon = document.getElementById('update-spinner');
    const outBox = document.getElementById('update-output-box');

    if (btn) btn.disabled = true;
    if (icon) icon.classList.add('animate-spin');
    if (outBox) {
        outBox.classList.remove('hidden');
        outBox.textContent = 'Pulling latest commits from GitHub repository...\n';
    }

    try {
        const res = await fetch('/admin/api/system/update', { method: 'POST' });
        const data = await res.json();

        if (outBox) {
            outBox.textContent += (data.output || '') + '\n' + (data.message || '');
        }

        if (data.success) {
            showToast('Update pulled successfully! Reloading server...', 'success', 'Update Applied');
            let countdown = 4;
            const timer = setInterval(() => {
                if (outBox) outBox.textContent += `\nReloading page in ${countdown}s...`;
                countdown--;
                if (countdown < 0) {
                    clearInterval(timer);
                    window.location.reload();
                }
            }, 1000);
        } else {
            showToast('Update failed: ' + (data.output || 'Error'), 'error', 'Update Failed');
            if (btn) btn.disabled = false;
            if (icon) icon.classList.remove('animate-spin');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Update Request Failed');
        if (btn) btn.disabled = false;
        if (icon) icon.classList.remove('animate-spin');
    }
}

async function saveSettings() {
    const btn = document.getElementById('save-btn');
    const lbl = document.getElementById('save-label');
    if (lbl) lbl.textContent = 'Saving...';

    const payload = {
        replace_mode: document.getElementById('replace_mode').checked,
        duplicate_protection: document.getElementById('duplicate_protection').checked,
        hide_catalog: document.getElementById('hide_catalog').checked,
        admin_username: document.getElementById('admin_username').value.trim(),
        tmdb_api: document.getElementById('tmdb_api').value.trim(),
        tvdb_api: document.getElementById('tvdb_api').value.trim(),
        base_url: document.getElementById('base_url').value.trim(),
        upstream_repo: document.getElementById('upstream_repo').value.trim(),
        upstream_branch: document.getElementById('upstream_branch').value.trim(),
        better_poster_enabled: document.getElementById('better_poster_enabled').checked,
        better_poster: document.getElementById('better_poster').value.trim(),
        rpdb_enabled: document.getElementById('rpdb_enabled').checked,
        rpdb_api_key: document.getElementById('rpdb_api_key').value.trim(),
        fanart_enabled: document.getElementById('fanart_enabled').checked,
        fanart_api_key: document.getElementById('fanart_api_key').value.trim(),
        fanart_low_res_poster: document.getElementById('fanart_low_res_poster').checked,
        stream_formatter: document.getElementById('stream_formatter').value,
        formatter_name: document.getElementById('formatter_name').value.trim(),
        formatter_description: document.getElementById('formatter_description').value.trim(),
        auth_channels: cachedSettings.auth_channels || [],
        channels: cachedSettings.auth_channels || [],
    };

    const pwd = document.getElementById('admin_password').value;
    if (pwd) payload.admin_password = pwd;

    try {
        const res = await fetch('/admin/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            showToast('Settings saved successfully!', 'success', 'Saved');
        } else {
            showToast('Failed to save settings.', 'error', 'Error');
        }
    } catch (e) {
        showToast(e.message, 'error', 'Save Error');
    } finally {
        if (lbl) lbl.textContent = 'Save Settings';
    }
}

async function exportBackup() {
    try {
        const res = await fetch('/admin/api/backup');
        const data = await res.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `telegram-stremio-backup-${new Date().toISOString().slice(0,10)}.json`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        showToast('Backup downloaded successfully', 'success', 'Exported');
    } catch (e) {
        showToast('Export failed: ' + e.message, 'error', 'Export Failed');
    }
}

// Initial Run
document.addEventListener('DOMContentLoaded', () => {
    refreshDashboard();
    liveStreamsInterval = setInterval(() => {
        if (currentTab === 'overview') {
            loadLiveStreams();
        } else if (currentTab === 'tools') {
            loadScannerStatus();
        }
    }, 4000);
});
</script>
</body>
</html>
"""
