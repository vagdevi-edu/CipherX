function process(type, mode) {
  let text, outputId, shift = 0;

  if (type === "caesar") {
    text = document.getElementById("cText").value;
    shift = document.getElementById("shift").value;
    outputId = "cOut";
  } else if (type === "des") {
    text = document.getElementById("dText").value;
    outputId = "dOut";
  } else {
    text = document.getElementById("rText").value;
    outputId = "rOut";
  }

  fetch(`/${type}`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text, shift, mode})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById(outputId).innerText = data.result;
    addHistory(type, mode, text, data.result);
  });
}

// HISTORY
function addHistory(type, mode, input, output) {
  let li = document.createElement("li");
  li.innerText = `${type.toUpperCase()} | ${mode} → ${input} => ${output}`;
  document.getElementById("historyList").appendChild(li);
}

// DARK MODE
function toggleTheme() {
  document.body.classList.toggle("dark");
}
