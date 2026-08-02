/* ===============================================================================
Open Caption by YO JI STUDIO - Standalone App UI JavaScript Logic + Full i18n
=============================================================================== */

const I18N = {
    zh: {
        sec_engine: "⚙️ AI 引擎配置",
        lbl_whisper_model: "Whisper 模型",
        lbl_device: "运行设备",
        lbl_compute: "计算精度",
        sec_task: "⚙️ 转写与断句微调",
        lbl_task: "处理任务",
        btn_transcribe: "语音转写",
        btn_translate: "翻译为英文",
        lbl_lang: "语种选择",
        opt_auto: "自动识别",
        lbl_vad: "✓ VAD 静音降噪",
        lbl_min_silence: "最小静音间隔",
        lbl_prompt: "Prompt 提示词",
        ph_prompt: "例如: 专有名词、行业术语或标点规范...",
        lbl_max_width: "单行最大字数",
        drop_title: "拖拽视频或音频文件到这里",
        drop_subtitle: "支持 MP4, MOV, WAV, MP3, M4A, FLAC 等格式",
        btn_browse: "选择文件",
        lbl_queue: "任务队列",
        btn_clear: "⟳ 清空",
        btn_start: "⚡ 开始 AI 智能识别与字幕生成",
        lbl_live_recognizing: "实时识别中...",
        lbl_elapsed: "已用时",
        lbl_remaining: "预计剩余",
        tab_edit: "🖊 字幕编辑",
        tab_export: "📄 导出字幕",
        tab_burn: "🎬 视频烧录",
        tab_batch: "📦 批量打包",
        ph_search: "查找文本...",
        ph_replace: "替换为...",
        btn_replace_all: "全部替换",
        th_start: "开始时间 ⏱",
        th_end: "结束时间 ⏱",
        th_content: "字幕内容",
        exp_srt: "⬇️ 导出 .SRT 标准字幕",
        exp_vtt: "⬇️ 导出 .VTT Web 字幕",
        exp_ass: "⬇️ 导出 .ASS 特效字幕",
        lbl_font_size: "字号",
        lbl_font_color: "文字颜色",
        color_white: "白色",
        color_yellow: "黄色",
        btn_start_burn: "🔥 开始硬烧录 MP4",
        btn_download_zip: "🎁 一键下载全套字幕打包 (.ZIP)"
    },
    en: {
        sec_engine: "⚙️ AI Engine Config",
        lbl_whisper_model: "Whisper Model",
        lbl_device: "Computing Device",
        lbl_compute: "Compute Precision",
        sec_task: "⚙️ Task & Segmentation",
        lbl_task: "Task Mode",
        btn_transcribe: "Transcribe",
        btn_translate: "Translate to EN",
        lbl_lang: "Language",
        opt_auto: "Auto Detect",
        lbl_vad: "✓ VAD Silence Filter",
        lbl_min_silence: "Min Silence Duration",
        lbl_prompt: "Initial Prompt",
        ph_prompt: "e.g. specialized terminology, brand names...",
        lbl_max_width: "Max Chars Per Line",
        drop_title: "Drag & drop video/audio files here",
        drop_subtitle: "Supports MP4, MOV, WAV, MP3, M4A, FLAC",
        btn_browse: "Browse Files",
        lbl_queue: "Task Queue",
        btn_clear: "⟳ Clear",
        btn_start: "⚡ Start AI Subtitle Generation",
        lbl_live_recognizing: "Live Transcribing...",
        lbl_elapsed: "Elapsed",
        lbl_remaining: "Remaining",
        tab_edit: "🖊 Subtitle Editor",
        tab_export: "📄 Export Files",
        tab_burn: "🎬 Video Burn-in",
        tab_batch: "📦 Batch ZIP",
        ph_search: "Search text...",
        ph_replace: "Replace with...",
        btn_replace_all: "Replace All",
        th_start: "Start Time ⏱",
        th_end: "End Time ⏱",
        th_content: "Subtitle Content",
        exp_srt: "⬇️ Export .SRT Subtitle",
        exp_vtt: "⬇️ Export .VTT Subtitle",
        exp_ass: "⬇️ Export .ASS Subtitle",
        lbl_font_size: "Font Size",
        lbl_font_color: "Font Color",
        color_white: "White",
        color_yellow: "Yellow",
        btn_start_burn: "🔥 Burn Subtitles to MP4",
        btn_download_zip: "🎁 Download All Subtitles (.ZIP)"
    },
    fr: {
        sec_engine: "⚙️ Config Moteur IA",
        lbl_whisper_model: "Modèle Whisper",
        lbl_device: "Appareil de calcul",
        lbl_compute: "Précision",
        sec_task: "⚙️ Tâche & Segmentation",
        lbl_task: "Mode de tâche",
        btn_transcribe: "Transcription",
        btn_translate: "Traduire en anglais",
        lbl_lang: "Langue",
        opt_auto: "Détection auto",
        lbl_vad: "✓ Filtre de silence VAD",
        lbl_min_silence: "Silence min",
        lbl_prompt: "Invite initiale",
        ph_prompt: "Ex. terminologie spécialisée, noms de marque...",
        lbl_max_width: "Caractères max / ligne",
        drop_title: "Glissez-déposez vos fichiers vidéo/audio ici",
        drop_subtitle: "Prend en charge MP4, MOV, WAV, MP3, M4A, FLAC",
        btn_browse: "Parcourir",
        lbl_queue: "File d'attente",
        btn_clear: "⟳ Vider",
        btn_start: "⚡ Générer les Sous-titres IA",
        lbl_live_recognizing: "Transcription en direct...",
        lbl_elapsed: "Écoulé",
        lbl_remaining: "Restant",
        tab_edit: "🖊 Éditeur de Tableau",
        tab_export: "📄 Exportation",
        tab_burn: "🎬 Incrustation Vidéo",
        tab_batch: "📦 Paquet ZIP",
        ph_search: "Rechercher...",
        ph_replace: "Remplacer par...",
        btn_replace_all: "Remplacer Tout",
        th_start: "Début ⏱",
        th_end: "Fin ⏱",
        th_content: "Texte du sous-titre",
        exp_srt: "⬇️ Exporter .SRT",
        exp_vtt: "⬇️ Exporter .VTT",
        exp_ass: "⬇️ Exporter .ASS",
        lbl_font_size: "Taille police",
        lbl_font_color: "Couleur police",
        color_white: "Blanc",
        color_yellow: "Jaune",
        btn_start_burn: "🔥 Incruster dans la Vidéo MP4",
        btn_download_zip: "🎁 Télécharger Tout en ZIP"
    }
};

let currentLang = 'zh';
let selectedFiles = [];
let transcribeResults = {};

document.addEventListener("DOMContentLoaded", () => {
    initAppBindings();
    fetchHardwareInfo();
    applyI18n();
});

// 1. 事件绑定
function initAppBindings() {
    // 语言切换按钮
    document.querySelectorAll(".lbtn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".lbtn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentLang = btn.dataset.lang;
            applyI18n();
        });
    });

    // 分段控制按钮 (语音转写 / 翻译为英文)
    document.querySelectorAll(".seg-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".seg-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
        });
    });

    // 滑块联动
    const rngSilence = document.getElementById("rngSilence");
    const txtSilence = document.getElementById("txtSilenceMs");
    if (rngSilence && txtSilence) {
        rngSilence.addEventListener("input", () => txtSilence.textContent = rngSilence.value + " ms");
    }

    // 拖拽与文件选择
    const dropzone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");

    if (dropzone && fileInput) {
        dropzone.addEventListener("dragover", (e) => { e.preventDefault(); dropzone.style.borderColor = "#007aff"; });
        dropzone.addEventListener("dragleave", () => { dropzone.style.borderColor = "rgba(255, 255, 255, 0.12)"; });
        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropzone.style.borderColor = "rgba(255, 255, 255, 0.12)";
            handleFileSelection(e.dataTransfer.files);
        });

        fileInput.addEventListener("change", () => handleFileSelection(fileInput.files));
    }

    // 清空队列
    document.getElementById("btnClearQueue").addEventListener("click", () => {
        selectedFiles = [];
        document.getElementById("lblQueueCount").textContent = "0";
        document.getElementById("queueItems").innerHTML = "<div style='color:#94a3b8; font-size:0.8rem;'>暂无文件</div>";
    });

    // 开始识别
    document.getElementById("btnStartRecognize").addEventListener("click", startTranscription);

    // 工作室 Tabs 切换
    document.querySelectorAll(".nav-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
            tab.classList.add("active");
            document.getElementById(tab.dataset.pane).classList.add("active");
        });
    });

    // 全部替换
    document.getElementById("btnReplaceAll").addEventListener("click", doTableReplace);
}

// 2. 实时语言切换实现
function applyI18n() {
    const dict = I18N[currentLang] || I18N.zh;

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.dataset.i18n;
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    document.querySelectorAll("[data-i18n-ph]").forEach(el => {
        const key = el.dataset.i18nPh;
        if (dict[key]) {
            el.placeholder = dict[key];
        }
    });
}

function handleFileSelection(files) {
    if (!files || files.length === 0) return;
    selectedFiles = Array.from(files);

    document.getElementById("lblQueueCount").textContent = selectedFiles.length;
    const queueList = document.getElementById("queueItems");
    queueList.innerHTML = "";

    selectedFiles.forEach(f => {
        const item = document.createElement("div");
        item.className = "q-item";
        const icon = f.type.startsWith("video") ? "📹" : "🎙️";
        const sizeMb = (f.size / (1024*1024)).toFixed(1);
        const ext = f.name.split('.').pop().toUpperCase();
        item.innerHTML = `
            <div class="q-icon">${icon}</div>
            <div class="q-details">
                <div class="q-name">${f.name}</div>
                <div class="q-meta">${sizeMb} MB • ${ext}</div>
            </div>
        `;
        queueList.appendChild(item);
    });
}

// 3. 硬件检测 Pills 更新
async function fetchHardwareInfo() {
    try {
        const res = await fetch("/api/diagnose_hardware");
        const data = await res.json();

        document.getElementById("txtGpu").textContent = data.device_name;
        document.getElementById("txtFfmpeg").textContent = data.ffmpeg_ready ? "FFmpeg Ready" : "No FFmpeg";
        document.getElementById("txtWhisper").textContent = "Whisper " + data.recommended_model;

        document.getElementById("selModel").value = data.recommended_model;
    } catch (e) {
        console.warn("Diagnostics error:", e);
    }
}

// 4. 执行转写
async function startTranscription() {
    if (selectedFiles.length === 0) {
        alert(currentLang === 'zh' ? "请先选择要处理的视频或音频文件！" : "Please select media files first!");
        return;
    }

    const btn = document.getElementById("btnStartRecognize");
    btn.disabled = true;
    btn.textContent = currentLang === 'zh' ? "⏳ AI 正在深度转写识别中..." : "⏳ AI Transcribing...";

    const formData = new FormData();
    selectedFiles.forEach(f => formData.append("files", f));
    formData.append("model", document.getElementById("selModel").value);
    formData.append("device", document.getElementById("selDevice").value);
    formData.append("compute_type", document.getElementById("selCompute").value);
    
    const activeSeg = document.querySelector(".seg-btn.active");
    formData.append("task", activeSeg ? activeSeg.dataset.task : "transcribe");
    formData.append("language", document.getElementById("selLang").value);
    formData.append("use_vad", document.getElementById("chkVad").checked);
    formData.append("min_silence_ms", document.getElementById("rngSilence").value);
    formData.append("initial_prompt", document.getElementById("txtPrompt").value);
    formData.append("max_line_width", document.getElementById("selMaxWidth").value);

    try {
        const res = await fetch("/api/transcribe", { method: "POST", body: formData });
        const data = await res.json();

        if (data.success) {
            transcribeResults = data.results;
            document.getElementById("txtPercent").textContent = "100%";
            renderTableData();
            alert(currentLang === 'zh' ? "🎉 AI 转写完成！可通过底部【字幕编辑】进行校对与导出。" : "🎉 Transcription completed!");
        } else {
            alert("Error: " + data.error);
        }
    } catch (e) {
        alert("Network Error: " + e);
    } finally {
        btn.disabled = false;
        btn.textContent = I18N[currentLang]?.btn_start || "⚡ 开始 AI 智能识别与字幕生成";
    }
}

// 5. 渲染表格
function renderTableData() {
    const fileNames = Object.keys(transcribeResults);
    if (fileNames.length === 0) return;

    const firstFile = fileNames[0];
    const segments = transcribeResults[firstFile].segments;

    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    segments.forEach((seg, idx) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${formatTime(seg.start)}</td>
            <td>${formatTime(seg.end)}</td>
            <td>${seg.text}</td>
        `;
        tbody.appendChild(tr);
    });
}

function doTableReplace() {
    const searchVal = document.getElementById("inputSearch").value.trim();
    const replaceVal = document.getElementById("inputReplace").value.trim();
    if (!searchVal) return;

    const rows = document.querySelectorAll("#dataTable tbody tr");
    let count = 0;
    rows.forEach(tr => {
        const cell = tr.children[3];
        if (cell.textContent.includes(searchVal)) {
            cell.textContent = cell.textContent.replaceAll(searchVal, replaceVal);
            count++;
        }
    });

    alert(currentLang === 'zh' ? `已批量替换 ${count} 处匹配文字！` : `Replaced ${count} items!`);
}

function formatTime(seconds) {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = Math.floor(seconds % 60);
    let millis = Math.round((seconds - Math.floor(seconds)) * 1000);

    const pad = (n) => String(n).padStart(2, '0');
    const padMs = (n) => String(n).padStart(3, '0');

    return `${pad(hours)}:${pad(minutes)}:${pad(secs)},${padMs(millis)}`;
}

function exportFormat(fmt) {
    alert(`Exporting .${fmt.toUpperCase()}...`);
}

function downloadZip() {
    window.location.href = "/api/export_zip";
}
