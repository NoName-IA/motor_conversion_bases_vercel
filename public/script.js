document.getElementById("btnConvertir").addEventListener("click", async () => {
  const numero = document.getElementById("numero").value;
  const baseOrigen = document.getElementById("baseOrigen").value;
  const wordSize = document.getElementById("wordSize").value;
  const errorEl = document.getElementById("errorConvertir");

  errorEl.textContent = "";
  ["outBin", "outOct", "outDec", "outHex"].forEach(id => document.getElementById(id).value = "");

  try {
    const res = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numero, base_origen: baseOrigen, word_size: wordSize })
    });
    const data = await res.json();

    if (!data.ok) {
      errorEl.textContent = data.error;
      return;
    }

    document.getElementById("outBin").value = data.resultado.binario;
    document.getElementById("outOct").value = data.resultado.octal;
    document.getElementById("outDec").value = data.resultado.decimal;
    document.getElementById("outHex").value = data.resultado.hexadecimal;
  } catch (err) {
    errorEl.textContent = "No se pudo conectar con el backend.";
  }
});

document.getElementById("btnAlu").addEventListener("click", async () => {
  const bin1 = document.getElementById("aluBin1").value;
  const bin2 = document.getElementById("aluBin2").value;
  const operacion = document.getElementById("aluOp").value;
  const wordSize = document.getElementById("wordSize").value;
  const errorEl = document.getElementById("errorAlu");

  errorEl.textContent = "";
  document.getElementById("aluResultado").value = "";

  try {
    const res = await fetch("/api/alu", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bin1, bin2, operacion, word_size: wordSize })
    });
    const data = await res.json();

    if (!data.ok) {
      errorEl.textContent = data.error;
      return;
    }

    document.getElementById("aluResultado").value = data.resultado;
  } catch (err) {
    errorEl.textContent = "No se pudo conectar con el backend.";
  }
});
