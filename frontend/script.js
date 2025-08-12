const api = location.origin;

function parseList(s){
  if(!s) return [];
  return s.split(/[;,.\s]+/).map(x=>parseInt(x,10)).filter(n=>!isNaN(n));
}
function toCSV(games){
  const head=[...Array(15)].map((_,i)=>`d${i+1}`).join(";");
  return head+"\n"+games.map(g=>g.join(";")).join("\n");
}
function render(games){
  const wrap=document.getElementById("results"); wrap.innerHTML="";
  (games||[]).forEach((g,i)=>{
    const card=document.createElement("div"); card.className="card";
    const title=document.createElement("div"); title.textContent=`Jogo ${i+1}`;
    const nums=document.createElement("div"); nums.className="nums";
    g.forEach(n=>{const b=document.createElement("div"); b.className="ball"; b.textContent=n; nums.appendChild(b);});
    card.appendChild(title); card.appendChild(nums); wrap.appendChild(card);
  });
  window.__games = (games||[]); window.__csv = toCSV(games||[]);
  const dl = document.getElementById("btn-download"); if (dl) dl.disabled = !(games && games.length);
}
function setMeta(text){ document.getElementById("meta").textContent = text || ""; }

async function ping(){
  try{const r=await fetch(`${api}/status`);const j=await r.json();
    document.getElementById("status").textContent=j.ok?`OK • v${j.version}`:"Indisponível";
  }catch{document.getElementById("status").textContent="Erro"}
}
async function loadStrategies(){
  const sel=document.getElementById("strategy");
  const r=await fetch(`${api}/api/strategies`); const list=await r.json();
  sel.innerHTML=""; for(const s of list){const o=document.createElement("option");o.value=s.id;o.textContent=`${s.name} — ${s.desc}`;sel.appendChild(o);}
}

async function loadLast(auto=false){
  try{
    const r = await fetch(`${api}/api/last`);
    if(!r.ok) throw new Error("sem último lote");
    const j = await r.json();
    render(j.games||[]);
    const when = j?.meta?.created_at || "";
    setMeta(`Último lote: ${j.batch_id} • jogos: ${j.count} • ${when}`);
    if(!auto) alert("Último lote carregado!");
  }catch(e){
    if(!auto) alert("Nenhum lote anterior encontrado.");
  }
}
async function loadHistory(){
  const page = parseInt(document.getElementById("hpage").value||"1",10);
  const size = parseInt(document.getElementById("hsize").value||"5",10);
  const r = await fetch(`${api}/api/history?page=${page}&page_size=${size}`);
  const j = await r.json();
  const el = document.getElementById("history");
  el.innerHTML = "";
  const list = j.items||[];
  if(list.length===0){ el.textContent = "Sem histórico."; return; }
  const table = document.createElement("table");
  table.style.width="100%"; table.style.borderCollapse="collapse";
  table.innerHTML = "<tr><th style='text-align:left'>Batch</th><th>Data</th><th>Modo</th><th>Qtd</th></tr>";
  list.forEach(it=>{
    const tr=document.createElement("tr");
    tr.innerHTML = `<td>${it.batch_id}</td><td style="text-align:center">${it.created_at||""}</td><td style="text-align:center">${it.mode}</td><td style="text-align:center">${it.total_games}</td>`;
    tr.style.borderTop="1px solid #2b2b2b";
    table.appendChild(tr);
  });
  el.appendChild(table);
}

document.getElementById("btn-generate").addEventListener("click", async ()=>{
  const body={
    strategy: document.getElementById("strategy").value,
    quantity: parseInt(document.getElementById("qty").value||"1",10),
    even: parseInt(document.getElementById("even").value||"NaN",10),
    min_sum: parseInt(document.getElementById("min_sum").value||"NaN",10),
    max_sum: parseInt(document.getElementById("max_sum").value||"NaN",10),
    reference: parseList(document.getElementById("reference").value),
    min_repeat: parseInt(document.getElementById("min_repeat").value||"NaN",10),
    max_repeat: parseInt(document.getElementById("max_repeat").value||"NaN",10),
  };
  for(const k of ["even","min_sum","max_sum","min_repeat","max_repeat"]){ if(Number.isNaN(body[k])) delete body[k]; }
  const r=await fetch(`${api}/api/generate`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const j=await r.json(); render(j.games||[]); setMeta(`Batch: ${j.batch_id||"-"} • ${j.quantity||0} jogos`);
});
document.getElementById("btn-download")?.addEventListener("click", ()=>{
  const blob=new Blob([window.__csv||""],{type:"text/csv;charset=utf-8;"}); const url=URL.createObjectURL(blob);
  const a=document.createElement("a"); a.href=url; a.download="sidloto2025.csv"; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
});
document.getElementById("btn-opt").addEventListener("click", async ()=>{
  const body={
    quantity: parseInt(document.getElementById("oqty").value||"10",10),
    last_result: parseList(document.getElementById("last_result").value),
    hot: parseList(document.getElementById("hot").value),
    cold: parseList(document.getElementById("cold").value),
    repeat_target: parseInt(document.getElementById("repeat_target").value||"9",10),
    even_target: parseInt(document.getElementById("even_target").value||"NaN",10),
    min_sum: parseInt(document.getElementById("omin").value||"NaN",10),
    max_sum: parseInt(document.getElementById("omax").value||"NaN",10),
    must: parseList(document.getElementById("must").value),
    avoid: parseList(document.getElementById("avoid").value),
    seed: parseInt(document.getElementById("seed").value||"NaN",10)
  };
  for(const k of ["even_target","min_sum","max_sum","seed"]){ if(Number.isNaN(body[k])) delete body[k]; }
  const r=await fetch(`${api}/api/generate_optimized`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const j=await r.json(); render(j.games||[]); setMeta(`Batch: ${j.batch_id||"-"} • ${j.games?.length||0} jogos (otimizado)`);
});
document.getElementById("btn-last").addEventListener("click", ()=>loadLast(false));
document.getElementById("btn-history").addEventListener("click", loadHistory);

ping(); loadStrategies(); loadLast(true);

function buildShareText(){
  const games = window.__games || [];
  if(!games.length) return "Sem resultados para compartilhar.";
  const meta = document.getElementById("meta")?.textContent || "";
  let lines = [];
  lines.push("Sidloto2025 — Jogos gerados");
  if(meta) lines.push(meta);
  lines.push("");
  games.forEach((g,i)=>{ lines.push(`Jogo ${i+1}: ` + g.join("-")); });
  lines.push("");
  lines.push("Padrão recomendado: repetição 8–9 • pares 7/8 • soma 185–200.");
  return lines.join("\\n");
}

async function copyShareText(){
  const txt = buildShareText();
  try{
    await navigator.clipboard.writeText(txt);
    alert("Texto copiado! Cole no WhatsApp/Telegram.");
  }catch(e){
    // fallback simples
    const ta = document.createElement("textarea");
    ta.value = txt; document.body.appendChild(ta); ta.select();
    document.execCommand("copy"); ta.remove();
    alert("Texto copiado (fallback)!");
  }
}

function sendWhatsApp(){
  const txt = buildShareText();
  const input = document.getElementById("wa_number");
  let num = (input?.value || "").replace(/[^0-9]/g, "");
  // Se não informar, abre WhatsApp para escolher contato
  const base = num ? `https://wa.me/${num}` : "https://wa.me/";
  const url = base + "?text=" + encodeURIComponent(txt);
  window.open(url, "_blank");
}
document.getElementById("btn-copy")?.addEventListener("click", copyShareText);
document.getElementById("btn-wa")?.addEventListener("click", sendWhatsApp);
