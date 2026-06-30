renderSidebar("dashboard.html");

const monthSelect = document.getElementById("month-select");
const yearSelect = document.getElementById("year-select");
const summaryGrid = document.getElementById("summary-grid");
const exchangeRateNote = document.getElementById("exchange-rate-note");
const incomeForm = document.getElementById("income-form");
const incomeError = document.getElementById("income-error");
const incomeTableBody = document.getElementById("income-table-body");
const incomeEmpty = document.getElementById("income-empty");
const incomeSubmitBtn = document.getElementById("income-submit-btn");
const incomeCancelEditBtn = document.getElementById("income-cancel-edit-btn");

const incomeStartPicker = createDatePicker(null);
const incomeEndPicker = createDatePicker(null);
document.getElementById("income-start-date-container").appendChild(incomeStartPicker.container);
document.getElementById("income-end-date-container").appendChild(incomeEndPicker.container);

let editingIncomeId = null;

const today = new Date();

function populateSelectors() {
  for (let m = 1; m <= 12; m++) {
    monthSelect.appendChild(el("option", { value: m, text: monthName(m) }));
  }
  monthSelect.value = today.getMonth() + 1;

  const currentYear = today.getFullYear();
  for (let y = currentYear - 2; y <= currentYear + 2; y++) {
    yearSelect.appendChild(el("option", { value: y, text: y }));
  }
  yearSelect.value = currentYear;
}

function renderSummary(summary) {
  summaryGrid.innerHTML = "";

  const percentage = Number(summary.committed_percentage);
  let percentageClass = "success";
  if (percentage >= 100) percentageClass = "danger";
  else if (percentage >= 70) percentageClass = "warning";

  const cards = [
    { label: "Renda do mês (BRL)", value: formatCurrency(summary.monthly_income_brl) },
    { label: "Gastos recorrentes (BRL)", value: formatCurrency(summary.recurring_expenses_brl) },
    { label: "Parcelas do mês (BRL)", value: formatCurrency(summary.installments_brl) },
    { label: "Gastos esporádicos (BRL)", value: formatCurrency(summary.sporadic_expenses_brl) },
    { label: "Total comprometido (BRL)", value: formatCurrency(summary.total_committed_brl) },
  ];

  cards.forEach((card) => {
    summaryGrid.appendChild(
      el("div", { class: "summary-card" }, [
        el("div", { class: "label", text: card.label }),
        el("div", { class: "value", text: card.value }),
      ])
    );
  });

  const progressCard = el("div", { class: "summary-card" }, [
    el("div", { class: "label", text: "Percentual comprometido" }),
    el("div", { class: "value", text: `${percentage.toFixed(2)}%` }),
  ]);
  const progressBar = el("div", { class: "progress-bar" }, [
    el("div", {
      class: `progress-bar-fill ${percentageClass === "warning" ? "warning" : percentageClass === "danger" ? "danger" : ""}`,
      style: `width: ${Math.min(percentage, 100)}%`,
    }),
  ]);
  progressCard.appendChild(progressBar);
  summaryGrid.appendChild(progressCard);

  exchangeRateNote.textContent = `Cotação USD → BRL utilizada: ${formatCurrency(summary.exchange_rate_usd_brl)}`;

  drawBarChart(document.getElementById("dashboard-chart"), {
    labels: ["Renda", "Recorrentes", "Parcelas", "Esporádicos"],
    datasets: [
      {
        color: "#2563eb",
        values: [
          Number(summary.monthly_income_brl),
          Number(summary.recurring_expenses_brl),
          Number(summary.installments_brl),
          Number(summary.sporadic_expenses_brl),
        ],
      },
    ],
  });
}

async function loadSummary() {
  const year = Number(yearSelect.value);
  const month = Number(monthSelect.value);
  const summary = await api.getDashboardSummary(year, month);
  renderSummary(summary);
}

function renderIncomes(incomes) {
  incomeTableBody.innerHTML = "";
  incomeEmpty.classList.toggle("hidden", incomes.length > 0);

  incomes.forEach((income) => {
    const editBtn = el("button", { class: "table-action", text: "Editar" });
    editBtn.addEventListener("click", () => startEditIncome(income));

    const removeBtn = el("button", { class: "table-action", text: "Remover" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteIncome(income.id);
      await refreshIncomes();
      await loadSummary();
    });

    const row = el("tr", {}, [
      el("td", { text: income.description || "—" }),
      el("td", { text: formatCurrency(income.amount, income.currency) }),
      el("td", {}, [
        el("span", {
          class: `badge ${income.currency === "USD" ? "badge-usd" : "badge-brl"}`,
          text: income.currency,
        }),
      ]),
      el("td", { text: income.payment_day ? `Dia ${income.payment_day}` : "—" }),
      el("td", {
        text: income.start_date || income.end_date
          ? `${income.start_date ? formatDate(income.start_date) : "início"} – ${income.end_date ? formatDate(income.end_date) : "sem fim"}`
          : "Sempre ativa",
      }),
      el("td", {}, [editBtn, removeBtn]),
    ]);
    incomeTableBody.appendChild(row);
  });
}

function resetIncomeForm() {
  editingIncomeId = null;
  incomeForm.reset();
  incomeStartPicker.setValue(null);
  incomeEndPicker.setValue(null);
  incomeSubmitBtn.textContent = "Adicionar";
  incomeCancelEditBtn.classList.add("hidden");
}

function startEditIncome(income) {
  editingIncomeId = income.id;
  document.getElementById("income-description").value = income.description || "";
  document.getElementById("income-amount").value = income.amount;
  document.getElementById("income-currency").value = income.currency;
  document.getElementById("income-payment-day").value = income.payment_day || "";
  incomeStartPicker.setValue(income.start_date || null);
  incomeEndPicker.setValue(income.end_date || null);
  incomeSubmitBtn.textContent = "Salvar alterações";
  incomeCancelEditBtn.classList.remove("hidden");
  incomeForm.scrollIntoView({ behavior: "smooth" });
}

incomeCancelEditBtn.addEventListener("click", resetIncomeForm);

async function refreshIncomes() {
  const incomes = await api.listIncomes();
  renderIncomes(incomes);
}

incomeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(incomeError);

  const description = document.getElementById("income-description").value.trim();
  const amount = document.getElementById("income-amount").value;
  const currency = document.getElementById("income-currency").value;
  const paymentDayValue = document.getElementById("income-payment-day").value;
  const payment_day = paymentDayValue ? Number(paymentDayValue) : null;

  try {
    const payload = {
      description: description || null,
      amount,
      currency,
      payment_day,
      start_date: incomeStartPicker.getValue(),
      end_date: incomeEndPicker.getValue(),
    };
    if (editingIncomeId) {
      await api.updateIncome(editingIncomeId, payload);
    } else {
      await api.createIncome(payload);
    }
    resetIncomeForm();
    await refreshIncomes();
    await loadSummary();
  } catch (error) {
    showError(incomeError, error.message);
  }
});

monthSelect.addEventListener("change", loadSummary);
yearSelect.addEventListener("change", loadSummary);

(async function init() {
  populateSelectors();
  await Promise.all([loadSummary(), refreshIncomes()]);
})();
