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

function createDatePicker(initialIsoDate) {
  const daySelect = el("select", { class: "date-picker-day" });
  daySelect.appendChild(el("option", { value: "", text: "Dia" }));
  for (let day = 1; day <= 31; day++) {
    daySelect.appendChild(el("option", { value: String(day), text: String(day) }));
  }

  const monthSelect = el("select", { class: "date-picker-month" });
  monthSelect.appendChild(el("option", { value: "", text: "Mês" }));
  MONTH_NAMES.forEach((name, index) => {
    monthSelect.appendChild(el("option", { value: String(index + 1), text: name }));
  });

  const currentYear = new Date().getFullYear();
  const yearSelect = el("select", { class: "date-picker-year" });
  yearSelect.appendChild(el("option", { value: "", text: "Ano" }));
  for (let year = currentYear - 2; year <= currentYear + 6; year++) {
    yearSelect.appendChild(el("option", { value: String(year), text: String(year) }));
  }

  const container = el("div", { class: "date-picker" }, [daySelect, monthSelect, yearSelect]);

  function setValue(isoDate) {
    if (!isoDate) {
      daySelect.value = "";
      monthSelect.value = "";
      yearSelect.value = "";
      return;
    }
    const [year, month, day] = isoDate.split("-");
    yearSelect.value = year;
    monthSelect.value = String(Number(month));
    daySelect.value = String(Number(day));
  }

  function getValue() {
    if (!daySelect.value || !monthSelect.value || !yearSelect.value) return null;
    const day = daySelect.value.padStart(2, "0");
    const month = monthSelect.value.padStart(2, "0");
    return `${yearSelect.value}-${month}-${day}`;
  }

  setValue(initialIsoDate);

  return { container, getValue, setValue };
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
