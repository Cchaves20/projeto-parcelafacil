renderSidebar("reports.html");

const yearSelect = document.getElementById("report-year");
const tableBody = document.getElementById("report-table-body");

function populateYearSelector() {
  const currentYear = new Date().getFullYear();
  for (let y = currentYear - 2; y <= currentYear + 2; y++) {
    yearSelect.appendChild(el("option", { value: y, text: y }));
  }
  yearSelect.value = currentYear;
}

function renderTable(summaries) {
  tableBody.innerHTML = "";
  summaries.forEach((summary) => {
    tableBody.appendChild(
      el("tr", {}, [
        el("td", { text: monthName(summary.month) }),
        el("td", { text: formatCurrency(summary.monthly_income_brl) }),
        el("td", { text: formatCurrency(summary.recurring_expenses_brl) }),
        el("td", { text: formatCurrency(summary.installments_brl) }),
        el("td", { text: formatCurrency(summary.total_committed_brl) }),
        el("td", { text: `${Number(summary.committed_percentage).toFixed(2)}%` }),
      ])
    );
  });
}

function renderChart(summaries) {
  drawBarChart(document.getElementById("report-chart"), {
    labels: summaries.map((summary) => monthName(summary.month).slice(0, 3)),
    datasets: [
      { color: "#2563eb", values: summaries.map((s) => Number(s.monthly_income_brl)) },
      { color: "#dc2626", values: summaries.map((s) => Number(s.total_committed_brl)) },
    ],
  });
}

async function loadReport() {
  const year = Number(yearSelect.value);
  const summaries = await api.getAnnualReport(year);
  renderTable(summaries);
  renderChart(summaries);
}

yearSelect.addEventListener("change", loadReport);

populateYearSelector();
loadReport();
