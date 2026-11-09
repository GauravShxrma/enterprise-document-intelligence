const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const evalForm = document.getElementById('evalForm');
const submitBtn = document.getElementById('submitBtn');
const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const leaderboard = document.getElementById('leaderboard');
const candidateCountBadge = document.getElementById('candidateCountBadge');
const exportCsvBtn = document.getElementById('exportCsvBtn');

let lastEvaluatedCandidates = [];

// 1. Drag & Drop Event Handling
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('border-blue-500', 'bg-blue-500/10');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('border-blue-500', 'bg-blue-500/10');
    }, false);
});

dropZone.addEventListener('drop', (e) => {
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
        const dt = new DataTransfer();
        for (let i = 0; i < droppedFiles.length; i++) {
            dt.items.add(droppedFiles[i]);
        }
        fileInput.files = dt.files;
        updateFileList();
    }
});

fileInput.addEventListener('change', updateFileList);

function updateFileList() {
    fileList.innerHTML = '';
    const files = Array.from(fileInput.files || []);
    if (files.length === 0) return;

    files.forEach((file) => {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between bg-slate-900/80 px-3 py-2 rounded border border-slate-700/50';
        item.innerHTML = `
            <div class="flex items-center space-x-2 truncate">
                <svg class="w-4 h-4 text-blue-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span class="truncate max-w-[220px] text-slate-200 text-xs">${file.name}</span>
            </div>
            <span class="text-[10px] text-slate-500 font-mono">${(file.size / 1024).toFixed(1)} KB</span>
        `;
        fileList.appendChild(item);
    });
}

// 2. Form Submission Handler
evalForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const roleTitle = document.getElementById('role_title').value.trim();
    const requiredSkills = document.getElementById('required_skills').value.trim();
    const files = fileInput.files;

    if (!roleTitle || !requiredSkills) {
        alert('Please enter a Target Role Title and Required Skills.');
        return;
    }

    if (!files || files.length === 0) {
        alert('Please attach at least one PDF or DOCX resume file.');
        return;
    }

    const formData = new FormData();
    formData.append('role_title', roleTitle);
    formData.append('required_skills', requiredSkills);
    
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    emptyState.classList.add('hidden');
    leaderboard.classList.add('hidden');
    exportCsvBtn.classList.add('hidden');
    loadingState.classList.remove('hidden');
    submitBtn.disabled = true;

    try {
        const endpoint = files.length === 1 
            ? '/api/v1/evaluate' 
            : '/api/v1/evaluate-batch';

        const response = await fetch(endpoint, { method: 'POST', body: formData });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Evaluation failed.');
        }

        const data = await response.json();
        renderLeaderboard(data);
    } catch (err) {
        alert(`Error: ${err.message}`);
        loadingState.classList.add('hidden');
        emptyState.classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
    }
});

// 3. Leaderboard Renderer
function renderLeaderboard(data) {
    loadingState.classList.add('hidden');
    leaderboard.classList.remove('hidden');
    leaderboard.innerHTML = '';

    const candidates = data.ranked_candidates || (data.candidate_name ? [data] : []);
    lastEvaluatedCandidates = candidates;
    
    if (candidates.length === 0) {
        candidateCountBadge.textContent = "0 Candidates Evaluated";
        candidateCountBadge.classList.remove('hidden');
        leaderboard.innerHTML = `
            <div class="bg-rose-500/10 border border-rose-500/20 rounded-xl p-6 text-center">
                <p class="text-rose-400 font-semibold text-sm">No valid candidates evaluated.</p>
            </div>
        `;
        return;
    }

    candidateCountBadge.textContent = `${candidates.length} Candidate${candidates.length > 1 ? 's' : ''} Evaluated`;
    candidateCountBadge.classList.remove('hidden');
    exportCsvBtn.classList.remove('hidden');

    candidates.forEach((candidate, index) => {
        const rank = index + 1;
        const score = candidate.deterministic_match_score;
        
        // Match score color styling
        let scoreColor = 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
        if (score < 50) scoreColor = 'text-rose-400 bg-rose-500/10 border-rose-500/20';
        else if (score < 75) scoreColor = 'text-amber-400 bg-amber-500/10 border-amber-500/20';

        // Verdict Badge Styling
        const verdict = candidate.hiring_verdict || 'Consider';
        let verdictBadge = '<span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">Consider</span>';
        if (verdict === 'Strong Hire') {
            verdictBadge = '<span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Strong Hire</span>';
        } else if (verdict === 'Pass') {
            verdictBadge = '<span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">Pass</span>';
        }

        const matchedBadges = candidate.matched_skills.map(s => 
            `<span class="px-2 py-0.5 rounded text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">${s}</span>`
        ).join('');

        const missingBadges = candidate.missing_skills.map(s => 
            `<span class="px-2 py-0.5 rounded text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">${s}</span>`
        ).join('');

        const totalSkillsCount = candidate.matched_skills.length + candidate.missing_skills.length;

        const card = document.createElement('div');
        card.className = 'bg-slate-900 border border-slate-700/80 rounded-xl p-5 hover:border-slate-600 transition shadow-lg';
        card.innerHTML = `
            <div class="flex items-start justify-between">
                <div class="flex items-center space-x-3">
                    <span class="flex items-center justify-center w-7 h-7 rounded-full bg-slate-800 text-slate-300 font-bold text-xs border border-slate-700">
                        #${rank}
                    </span>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h3 class="font-bold text-base text-white">${candidate.candidate_name}</h3>
                            ${verdictBadge}
                        </div>
                        <p class="text-xs text-slate-400 mt-1 font-medium">
                            ${candidate.years_of_experience} Yrs Experience &bull; Matched ${candidate.matched_skills.length} of ${totalSkillsCount} required skills
                        </p>
                    </div>
                </div>
                <div class="text-right">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-bold border ${scoreColor}">
                        ${score.toFixed(0)}% Match
                    </span>
                </div>
            </div>

            <div class="mt-4 pt-4 border-t border-slate-800/80 space-y-3">
                <div>
                    <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Matched Skills</span>
                    <div class="flex flex-wrap gap-1.5">${matchedBadges || '<span class="text-xs text-slate-500">None</span>'}</div>
                </div>
                ${candidate.missing_skills.length > 0 ? `
                    <div>
                        <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Missing Skills</span>
                        <div class="flex flex-wrap gap-1.5">${missingBadges}</div>
                    </div>
                ` : ''}
                <div class="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
                    <span class="text-[11px] font-semibold text-blue-400 uppercase tracking-wider block mb-1">Recruiter Evaluation & Skill Assessment</span>
                    <p class="text-xs text-slate-300 leading-relaxed">${candidate.summary}</p>
                </div>
            </div>
        `;
        leaderboard.appendChild(card);
    });
}

// 4. CSV Export Listener
exportCsvBtn.addEventListener('click', () => {
    if (lastEvaluatedCandidates.length === 0) return;

    const headers = ["Rank", "Candidate Name", "Match Score (%)", "Verdict", "Years Experience", "Matched Skills", "Missing Skills", "HR Summary"];
    const rows = lastEvaluatedCandidates.map((c, idx) => [
        idx + 1,
        `"${c.candidate_name.replace(/"/g, '""')}"`,
        c.deterministic_match_score.toFixed(1),
        `"${(c.hiring_verdict || 'Consider').replace(/"/g, '""')}"`,
        c.years_of_experience,
        `"${c.matched_skills.join(', ').replace(/"/g, '""')}"`,
        `"${c.missing_skills.join(', ').replace(/"/g, '""')}"`,
        `"${c.summary.replace(/"/g, '""')}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8," 
        + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `TalentRank_Evaluations_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});