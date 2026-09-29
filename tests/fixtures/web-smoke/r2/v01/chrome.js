// Shared nav for every page of this direction. Links are relative to v01/.
const NAV = `<div class="wrap"><nav><b>Tempo</b> <a href="index.html">Home</a> <a href="features.html">Features</a></nav></div>`;
document.querySelectorAll('[data-chrome="nav"]').forEach((el) => (el.innerHTML = NAV));
