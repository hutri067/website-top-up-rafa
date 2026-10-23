from flask import Flask, request, render_template_string
from urllib.parse import quote

app = Flask(__name__)

ADMIN_WA = "85378380599"

PRODUCTS = {
    "Free Fire": [
        ("5 Diamonds", 1000),
        ("12 Diamonds", 2000),
        ("50 Diamonds", 8000),
        ("70 Diamonds", 10000),
        ("140 Diamonds", 20000),
    ],
    "Mobile Legends": [
        ("Weekly Diamond Pass", 28000),
        ("86 Diamonds", 22000),
        ("172 Diamonds", 44000),
        ("257 Diamonds", 65000),
    ],
    "PUBG Mobile": [
        ("60 UC", 15000),
        ("325 UC", 75000),
        ("660 UC", 145000),
    ],
    "Genshin Impact": [
        ("60 Genesis Crystals", 16000),
        ("Blessing of the Welkin Moon", 80000),
    ],
}

PAGE = r"""
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RAFA TOPUP — Top Up Game</title>
  <style>
    :root { --bg:#090d18; --panel:#121a2b; --muted:#9aa8c4; --text:#f5f7ff; --accent:#7c5cff; --cyan:#24d6c8; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:system-ui,Arial,sans-serif; background:radial-gradient(circle at 80% 0%,#20245a 0,transparent 32%),var(--bg); color:var(--text); }
    header { padding:20px 6%; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ffffff12; }
    .logo { font-weight:900; letter-spacing:1px; font-size:21px; }.logo span { color:var(--cyan); }
    .pill { border:1px solid #ffffff20; color:#c9d4ed; border-radius:99px; padding:8px 12px; font-size:12px; }
    main { max-width:1050px; margin:auto; padding:38px 18px 70px; }
    .hero { padding:30px 0 24px; }.eyebrow { color:var(--cyan); font-weight:800; font-size:12px; letter-spacing:2px; }
    h1 { font-size:clamp(34px,7vw,60px); line-height:1.05; margin:12px 0; letter-spacing:-2px; }
    h1 span { color:var(--cyan); }.hero p { color:var(--muted); max-width:560px; line-height:1.7; }
    .layout { display:grid; grid-template-columns:1.05fr .95fr; gap:18px; align-items:start; }
    .panel { background:linear-gradient(145deg,#151e32,#101625); border:1px solid #ffffff12; border-radius:22px; padding:22px; box-shadow:0 18px 50px #0002; }
    h2 { font-size:18px; margin:0 0 16px; } .games { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .game { background:#0c1220; border:1px solid #ffffff17; border-radius:14px; padding:14px; color:var(--text); text-align:left; cursor:pointer; min-height:78px; }
    .game strong { display:block; margin-top:8px; font-size:13px; }.game.active { border-color:var(--cyan); background:#123033; }
    .emoji { font-size:23px; } label { display:block; font-size:13px; color:#c8d1e6; margin:15px 0 7px; }
    input,select { width:100%; border:1px solid #ffffff1c; background:#0b1120; color:white; border-radius:11px; padding:13px; outline:none; }
    input:focus,select:focus { border-color:var(--cyan); }
    .packages { display:grid; grid-template-columns:1fr 1fr; gap:9px; }
    .pkg { text-align:left; padding:13px; border:1px solid #ffffff18; background:#0b1120; color:white; border-radius:12px; cursor:pointer; }
    .pkg b { display:block; font-size:14px; }.pkg small { color:var(--cyan); display:block; margin-top:6px; }.pkg.active { border-color:var(--accent); background:#211b43; }
    .summary { background:#0b1120; border-radius:14px; padding:15px; margin-top:18px; }
    .sumrow { display:flex; justify-content:space-between; gap:12px; margin:7px 0; color:var(--muted); font-size:14px; }.sumrow.total { color:white; font-size:17px; font-weight:800; padding-top:10px; border-top:1px solid #ffffff16; }
    .buy { margin-top:14px; width:100%; border:0; border-radius:12px; padding:15px; background:linear-gradient(90deg,var(--accent),#4b8dff); color:white; font-weight:900; font-size:15px; cursor:pointer; }
    .note { color:var(--muted); font-size:12px; line-height:1.6; margin-top:14px; }.footer { text-align:center; color:#7e8ba6; font-size:12px; padding:26px; }
    @media(max-width:720px) { .layout { grid-template-columns:1fr; } header { padding:16px 18px; } main { padding-top:20px; } .panel { padding:17px; } }
  </style>
</head>
<body>
<header><div class="logo">NEXA<span>TOPUP</span></div><div class="pill">● Demo Store</div></header>
<main>
  <section class="hero">
    <div class="eyebrow">LEVEL UP YOUR GAME</div>
    <h1>Top up cepat.<br><span>Main tanpa batas.</span></h1>
    <p>Pilih game, tentukan nominal, lalu kirim pesanan ke admin melalui WhatsApp. Harga di bawah ini adalah contoh dan perlu kamu sesuaikan.</p>
  </section>
  <form id="orderForm">
    <div class="layout">
      <section class="panel">
        <h2>01 / Pilih game</h2>
        <div class="games">
          <button type="button" class="game active" data-game="Free Fire"><span class="emoji">🔥</span><strong>Free Fire</strong></button>
          <button type="button" class="game" data-game="Mobile Legends"><span class="emoji">⚔️</span><strong>Mobile Legends</strong></button>
          <button type="button" class="game" data-game="PUBG Mobile"><span class="emoji">🎯</span><strong>PUBG Mobile</strong></button>
          <button type="button" class="game" data-game="Genshin Impact"><span class="emoji">✨</span><strong>Genshin Impact</strong></button>
        </div>
        <input type="hidden" id="game" value="Free Fire">
        <label for="player">ID pemain</label><input id="player" placeholder="Masukkan ID game" required>
        <label for="server">Server / Zone (jika diperlukan)</label><input id="server" placeholder="Contoh: 1234 atau kosong">
        <label for="nickname">Nama pembeli (opsional)</label><input id="nickname" placeholder="Nama kamu">
      </section>
      <section class="panel">
        <h2>02 / Pilih nominal</h2>
        <div id="packages" class="packages"></div>
        <input type="hidden" id="package" value="">
        <input type="hidden" id="price" value="0">
        <div class="summary">
          <div class="sumrow"><span>Game</span><strong id="sumGame">Free Fire</strong></div>
          <div class="sumrow"><span>Nominal</span><strong id="sumPackage">Pilih nominal</strong></div>
          <div class="sumrow total"><span>Total</span><strong id="sumPrice">Rp0</strong></div>
        </div>
        <button class="buy" type="submit">Pesan via WhatsApp ↗</button>
        <p class="note">Demo ini belum memproses pembayaran otomatis. Pastikan ID pemain benar dan konfirmasi harga serta pembayaran dengan admin sebelum transaksi.</p>
      </section>
    </div>
  </form>
</main>
<div class="footer">© 2026 RAFATOPUP · Fan-made demo, bukan situs resmi game.</div>
<script>
const products = {{ products|tojson }};
let selectedPackage = "";
let selectedPrice = 0;
const rupiah = n => "Rp" + Number(n).toLocaleString("id-ID");
function drawPackages() {
  const game = document.getElementById("game").value;
  const root = document.getElementById("packages");
  root.innerHTML = "";
  selectedPackage = ""; selectedPrice = 0;
  document.getElementById("package").value = "";
  document.getElementById("price").value = "0";
  document.getElementById("sumGame").textContent = game;
  document.getElementById("sumPackage").textContent = "Pilih nominal";
  document.getElementById("sumPrice").textContent = "Rp0";
  products[game].forEach(([name, price]) => {
    const button = document.createElement("button");
    button.type = "button"; button.className = "pkg";
    const title = document.createElement("b"); title.textContent = name;
    const cost = document.createElement("small"); cost.textContent = rupiah(price);
    button.append(title, cost);
    button.addEventListener("click", () => {
      document.querySelectorAll(".pkg").forEach(el => el.classList.remove("active"));
      button.classList.add("active");
      selectedPackage = name; selectedPrice = price;
      document.getElementById("package").value = name;
      document.getElementById("price").value = price;
      document.getElementById("sumPackage").textContent = name;
      document.getElementById("sumPrice").textContent = rupiah(price);
    });
    root.appendChild(button);
  });
}
document.querySelectorAll(".game").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".game").forEach(el => el.classList.remove("active"));
  button.classList.add("active");
  document.getElementById("game").value = button.dataset.game;
  drawPackages();
}));
document.getElementById("orderForm").addEventListener("submit", event => {
  event.preventDefault();
  const player = document.getElementById("player").value.trim();
  if (!player) { alert("Masukkan ID pemain dulu."); return; }
  if (!selectedPackage) { alert("Pilih nominal top up dulu."); return; }
  const game = document.getElementById("game").value;
  const server = document.getElementById("server").value.trim() || "-";
  const nickname = document.getElementById("nickname").value.trim() || "-";
  const message = `Halo admin, saya mau pesan top up.%0AGame: ${game}%0AID pemain: ${player}%0AServer: ${server}%0ANama: ${nickname}%0ANominal: ${selectedPackage}%0ATotal: ${rupiah(selectedPrice)}`;
  const url = "https://wa.me/" + "{{ admin_wa }}" + "?text=" + encodeURIComponent(decodeURIComponent(message));
  window.open(url, "_blank");
});
drawPackages();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(PAGE, products=PRODUCTS, admin_wa=ADMIN_WA)

if __name__ == "__main__":
    print("Website berjalan di http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
