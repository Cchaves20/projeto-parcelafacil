renderSidebar("recurring-expenses.html");

const recurringForm = document.getElementById("recurring-form");
const recurringError = document.getElementById("recurring-error");
const recurringTableBody = document.getElementById("recurring-table-body");
const recurringEmpty = document.getElementById("recurring-empty");
const categorySelect = document.getElementById("recurring-category");
const frequencySelect = document.getElementById("recurring-frequency");
const monthlyFields = document.getElementById("monthly-fields");
const weeklyFields = document.getElementById("weekly-fields");
const variableFields = document.getElementById("variable-fields");
const periodsContainer = document.getElementById("periods-container");
const addPeriodBtn = document.getElementById("add-period-btn");
const submitBtn = document.getElementById("recurring-submit-btn");
const cancelEditBtn = document.getElementById("recurring-cancel-edit-btn");

const WEEKDAY_LABELS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];

let editingExpenseId = null;

function addPeriodRow(period) {
  const startPicker = createDatePicker(period ? period.start_date : null);
  const endPicker = createDatePicker(period ? period.end_date : null);
  startPicker.container.classList.add("period-start");
  endPicker.container.classList.add("period-end");

  const row = el("div", { class: "period-row" }, [startPicker.container, endPicker.container]);
  row._startPicker = startPicker;
  row._endPicker = endPicker;

  const removeBtn = el("button", { type: "button", class: "table-action", text: "Remover" });
  removeBtn.addEventListener("click", () => {
    if (periodsContainer.children.length > 1) row.remove();
  });
  row.appendChild(removeBtn);
  periodsContainer.appendChild(row);
}

addPeriodBtn.addEventListener("click", () => addPeriodRow());

function updateFrequencyUI() {
  const freq = frequencySelect.value;
  monthlyFields.classList.toggle("hidden", freq !== "MONTHLY");
  weeklyFields.classList.toggle("hidden", freq !== "WEEKLY");
  variableFields.classList.toggle("hidden", freq !== "VARIABLE");

  if (freq === "WEEKLY") {
    document.getElementById("recurring-amount-label").textContent = "Valor por semana";
  } else if (freq === "VARIABLE") {
    document.getElementById("recurring-amount-label").textContent = "Valor por ocorrência";
  } else {
    document.getElementById("recurring-amount-label").textContent = "Valor";
  }
}

frequencySelect.addEventListener("change", updateFrequencyUI);

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

function resetForm() {
  editingExpenseId = null;
  recurringForm.reset();
  periodsContainer.innerHTML = "";
  addPeriodRow();
  monthlyFields.classList.remove("hidden");
  weeklyFields.classList.add("hidden");
  variableFields.classList.add("hidden");
  document.getElementById("recurring-amount-label").textContent = "Valor";
  submitBtn.textContent = "Adicionar";
  cancelEditBtn.classList.add("hidden");
}

function startEdit(expense) {
  editingExpenseId = expense.id;
  document.getElementById("recurring-name").value = expense.name;
  document.getElementById("recurring-amount").value = expense.amount;
  document.getElementById("recurring-currency").value = expense.currency;
  categorySelect.value = expense.category_id || "";
  frequencySelect.value = expense.frequency;

  monthlyFields.classList.toggle("hidden", expense.frequency !== "MONTHLY");
  weeklyFields.classList.toggle("hidden", expense.frequency !== "WEEKLY");
  variableFields.classList.toggle("hidden", expense.frequency !== "VARIABLE");

  if (expense.frequency === "WEEKLY") {
    weeklyFields.querySelectorAll("input[type=checkbox]").forEach((checkbox) => {
      checkbox.checked = (expense.weekdays || []).includes(Number(checkbox.value));
    });
    document.getElementById("recurring-amount-label").textContent = "Valor por semana";
  } else if (expense.frequency === "VARIABLE") {
    document.getElementById("recurring-monthly-occurrences").value = expense.estimated_monthly_occurrences || "";
    document.getElementById("recurring-amount-label").textContent = "Valor por ocorrência";
  } else {
    document.getElementById("recurring-billing-day").value = expense.billing_day;
    document.getElementById("recurring-amount-label").textContent = "Valor";
  }

  periodsContainer.innerHTML = "";
  expense.periods.forEach((period) => addPeriodRow(period));

  submitBtn.textContent = "Salvar alterações";
  cancelEditBtn.classList.remove("hidden");
  recurringForm.scrollIntoView({ behavior: "smooth" });
}

cancelEditBtn.addEventListener("click", resetForm);

function frequencyLabel(expense) {
  if (expense.frequency === "WEEKLY") {
    return "Semanal (" + (expense.weekdays || []).map((day) => WEEKDAY_LABELS[day]).join(", ") + ")";
  }
  if (expense.frequency === "VARIABLE") {
    return "Variável (~" + expense.estimated_monthly_occurrences + "x/mês)";
  }
  return "Mensal (dia " + expense.billing_day + ")";
}

function renderRecurringExpenses(expenses) {
  recurringTableBody.innerHTML = "";
  recurringEmpty.classList.toggle("hidden", expenses.length > 0);

  expenses.forEach((expense) => {
    const editBtn = el("button", { class: "table-action", text: "Editar" });
    editBtn.addEventListener("click", () => startEdit(expense));

    const removeBtn = el("button", { class: "table-action", text: "Remover" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteRecurringExpense(expense.id);
      await refreshRecurringExpenses();
    });

    recurringTableBody.appendChild(
      el("tr", {}, [
        el("td", { text: expense.name }),
        el("td", { text: formatCurrency(expense.amount, expense.currency) }),
        el("td", {}, [
          el("span", {
            class: "badge " + (expense.currency === "USD" ? "badge-usd" : "badge-brl"),
            text: expense.currency,
          }),
        ]),
        el("td", { text: frequencyLabel(expense) }),
        el("td", { text: formatPeriods(expense.periods) }),
        el("td", {}, [editBtn, removeBtn]),
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
    start_date: row._startPicker.getValue(),
    end_date: row._endPicker.getValue(),
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
  } else if (frequency === "VARIABLE") {
    payload.estimated_monthly_occurrences = Number(document.getElementById("recurring-monthly-occurrences").value);
  } else {
    payload.billing_day = Number(document.getElementById("recurring-billing-day").value);
  }

  try {
    if (editingExpenseId) {
      await api.updateRecurringExpense(editingExpenseId, payload);
    } else {
      await api.createRecurringExpense(payload);
    }
    resetForm();
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
