const MONTH_NAMES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];

function formatCurrency(amount, currency = "BRL") {
  const value = Number(amount);
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency }).format(value);
}

function formatDate(isoDate) {
  if (!isoDate) return "";
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

function monthName(month) {
  return MONTH_NAMES[month - 1] || "";
}

function showError(container, message) {
  container.textContent = message;
  container.classList.remove("hidden");
}

function hideError(container) {
  container.textContent = "";
  container.classList.add("hidden");
}

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(props).forEach(([key, value]) => {
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else node.setAttribute(key, value);
  });
  children.forEach((child) => node.appendChild(child));
  return node;
}
