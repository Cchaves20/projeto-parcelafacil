renderSidebar("recurring-expenses.html");

const recurringForm = document.getElementById("recurring-form");
const recurringError = document.getElementById("recurring-error");
const recurringTableBody = document.getElementById("recurring-table-body");
const recurringEmpty = document.getElementById("recurring-empty");
const categorySelect = document.getElementById("recurring-category");
const frequencySelect = document.getElementById("recurring-frequency");
const monthlyFields = document.getElementById("monthly-fields");
const weeklyFields = document.getElementById("weekly-fields");
const periodsContainer = document.getElementById("periods-container");
const addPeriodBtn = document.getElementById("add-period-btn");

const WEEKDAY_LABELS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];

function addPeriodRow() {
  const row = el("div", { class: "period-row" }, [
    el("input", { type: "date", class: "period-start", required: "" }),
    el("input", { type: "date", class: "period-end", placeholder: "Fim (opcional)" }),
  ]);
  const removeBtn = el("button", { type: "button", class: "table-action", text: "Remover" });
  removeBtn.addEventListener("click", () => {
    if (periodsContainer.children.length > 1) row.remove();
  });
  row.appendChild(removeBtn);
  periodsContainer.appendChild(row);
}

addPeriodBtn.addEventListener("click", addPeriodRow);

frequencySelect.addEventListener("change", () => {
  const isWeekly = frequencySelect.value === "WEEKLY";
  monthlyFields.classList.toggle("hidden", isWeekly);
  weeklyFields.classList.toggle("hidden", !isWeekly);
});

async function loadCategories() {
  const categories = await api.listCategories();
  categories.forEach((category) => {
    categorySelect.appendChild(el("option", { value: category.id, text: category.name }));
  });
}

function formatPeriods(periods) {
  return periods
    .map((period) => `${formatDate(period.start_date)} – ${period.end_date ? formatDate(period.end_date) : "sem fim"}`)
    .join(", ");
}

function renderRecurringExpenses(expenses) {
  recurringTableBody.innerHTML = "";
  recurringEmpty.classList.toggle("hidden", expenses.length > 0);

  expenses.forEach((expense) => {
    const removeBtn = el("button", { class: "table-action", text: "Remover" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteRecurringExpense(expense.id);
      await refreshRecurringExpenses();
    });

    const frequencyLabel =
      expense.frequency === "WEEKLY"
        ? `Semanal (${(expense.weekdays || []).map((day) => WEEKDAY_LABELS[day]).join(", ")})`
        : `Mensal (dia ${expense.billing_day})`;

    recurringTableBody.appendChild(
      el("tr", {}, [
        el("td", { text: expense.name }),
        el("td", { text: formatCurrency(expense.amount, expense.currency) }),
        el("td", {}, [
          el("span", {
            class: `badge ${expense.currency === "USD" ? "badge-usd" : "badge-brl"}`,
            text: expense.currency,
          }),
        ]),
        el("td", { text: frequencyLabel }),
        el("td", { text: formatPeriods(expense.periods) }),
        el("td", {}, [removeBtn]),
      ])
    );
  });
}

async function refreshRecurringExpenses() {
  const expenses = await api.listRecurringExpenses();
  renderRecurringExpenses(expenses);
}

recurringForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(recurringError);

  const frequency = frequencySelect.value;
  const periods = Array.from(periodsContainer.children).map((row) => ({
    start_date: row.querySelector(".period-start").value,
    end_date: row.querySelector(".period-end").value || null,
  }));

  const payload = {
    name: document.getElementById("recurring-name").value.trim(),
    amount: document.getElementById("recurring-amount").value,
    currency: document.getElementById("recurring-currency").value,
    category_id: categorySelect.value ? Number(categorySelect.value) : null,
    frequency,
    periods,
  };

  if (frequency === "WEEKLY") {
    payload.weekdays = Array.from(weeklyFields.querySelectorAll("input[type=checkbox]:checked")).map((checkbox) =>
      Number(checkbox.value)
    );
  } else {
    payload.billing_day = Number(document.getElementById("recurring-billing-day").value);
  }

  try {
    await api.createRecurringExpense(payload);
    recurringForm.reset();
    periodsContainer.innerHTML = "";
    addPeriodRow();
    monthlyFields.classList.remove("hidden");
    weeklyFields.classList.add("hidden");
    await refreshRecurringExpenses();
  } catch (error) {
    showError(recurringError, error.message);
  }
});

(async function init() {
  addPeriodRow();
  await loadCategories();
  await refreshRecurringExpenses();
})();
