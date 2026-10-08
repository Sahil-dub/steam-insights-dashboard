const DATA_URL="../data/steam_games_cleaned.csv";
const $=id=>document.getElementById(id);
function parseCSV(text){const rows=[];let row=[],cell="",quoted=false;for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='\"'){if(quoted&&n==='\"'){cell+='\"';i++;}else quoted=!quoted;}else if(c===','&&!quoted){row.push(cell);cell="";}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(cell);if(row.some(v=>v!==""))rows.push(row);row=[];cell="";}else cell+=c;}if(cell||row.length){row.push(cell);rows.push(row);}const h=rows.shift().map(x=>x.trim());return rows.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]??""])));}
const num=v=>{const x=Number(v);return Number.isFinite(x)?x:null};
const cleanGenres=v=>String(v||"").replace(/[\[\]'\"\\]/g,"").split(",").map(x=>x.trim()).filter(Boolean);
const money=v=>v==null?"—":"€"+v.toFixed(2);
function render(data){
 const games=data.length, prices=data.map(r=>num(r.price)).filter(v=>v!=null), scores=data.map(r=>num(r.user_score)).filter(v=>v!=null&&v>0);
 const dates=data.map(r=>new Date(r.release_date)).filter(d=>!isNaN(d)), years=dates.map(d=>d.getFullYear());
 $("kpi-games").textContent=games.toLocaleString(); $("kpi-price").textContent=money(prices.reduce((a,b)=>a+b,0)/prices.length); $("kpi-score").textContent=(scores.reduce((a,b)=>a+b,0)/scores.length).toFixed(2); $("kpi-years").textContent=Math.min(...years)+"–"+Math.max(...years);
 const yc={}; years.forEach(y=>yc[y]=(yc[y]||0)+1); const ys=Object.keys(yc).sort((a,b)=>a-b), maxY=Math.max(...Object.values(yc));
 $("release-chart").innerHTML=ys.map(y=>'<div class="bar-col" title="'+y+': '+yc[y].toLocaleString()+' games"><div class="bar" style="height:'+Math.max(2,yc[y]/maxY*100)+'%"></div></div>').join("")+ys.filter((_,i)=>i%5===0).map(y=>'<span class="bar-label">'+y+'</span>').join("");
 const gc={};data.forEach(r=>cleanGenres(r.genres).forEach(g=>gc[g]=(gc[g]||0)+1)); const topG=Object.entries(gc).sort((a,b)=>b[1]-a[1]).slice(0,10), maxG=topG[0]?topG[0][1]:1;
 $("genre-chart").innerHTML=topG.map(x=>'<div class="genre-row"><span>'+x[0]+'</span><div class="track"><i style="width:'+(x[1]/maxG*100)+'%"></i></div><b>'+x[1].toLocaleString()+'</b></div>').join("");
 const scatter=data.filter(r=>num(r.price)>0&&num(r.user_score)>0).sort(()=>Math.random()-.5).slice(0,450), sx=Math.max(...scatter.map(r=>num(r.price)));
 $("scatter").innerHTML=scatter.map(r=>{const x=num(r.price),y=num(r.user_score);return '<span class="dot" title="'+String(r.name).replace(/\"/g,"'")+' · €'+x+' · score '+y+'" style="left:'+Math.min(98,x/sx*100)+'%;bottom:'+Math.min(98,y/10*100)+'%"></span>';}).join("");
 const values=data.map(r=>({name:r.name,price:num(r.price),play:num(r.average_playtime_forever)})).filter(r=>r.name&&r.price>0&&r.play>0).map(r=>Object.assign(r,{value:r.play/r.price})).sort((a,b)=>b.value-a.value).slice(0,8);
 $("value-table").innerHTML='<table class="table"><thead><tr><th>Game</th><th>Price</th><th>Playtime</th><th>Min/€</th></tr></thead><tbody>'+values.map(r=>'<tr><td>'+r.name+'</td><td>€'+r.price.toFixed(2)+'</td><td>'+Math.round(r.play).toLocaleString()+' min</td><td>'+Math.round(r.value).toLocaleString()+'</td></tr>').join("")+'</tbody></table>';
 $("status").textContent="Live preview powered by the repository dataset";
}
fetch(DATA_URL).then(r=>{if(!r.ok)throw Error("Dataset unavailable");return r.text();}).then(t=>render(parseCSV(t))).catch(e=>{$("status").textContent="Dataset preview unavailable — see GitHub source";console.error(e);});
