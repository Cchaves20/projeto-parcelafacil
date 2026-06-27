renderSidebar("recurring-expenses.html");

const recurringForm = document.getElementById("recurring-form");
const recurringError = document.getElementById("recurring-error");
const recurringTableBody = document.getElementById("recurring-table-body");
const recurringEmpty = document.getElementById("recurring-empty");
const categorySelect = document.getElementById("recurring-category");

async function loadCategories() {
  const categories = await api.listCategories();
  categories.forEach((category) => {
    categorySelect.appendChild(el("option", { value: category.id, text: category.name }));
  });
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
        el("td", { text: expense.billing_day }),
        el("td", { text: formatDate(expense.start_date) }),
        el("td", { text: expense.end_date ? formatDate(expense.end_date) : "—" }),
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

  const payload = {
    name: document.getElementById("recurring-name").value.trim(),
    amount: document.getElementById("recurring-amount").value,
    currency: document.getElementById("recurring-currency").value,
    category_id: categorySelect.value ? Number(categorySelect.value) : null,
    billing_day: Number(document.getElementById("recurring-billing-day").value),
    start_date: document.getElementById("recurring-start-date").value,
    end_date: document.getElementById("recurring-end-date").value || null,
  };

  try {
    await api.createRecurringExpense(payload);
    recurringForm.reset();
    await refreshRecurringExpenses();
  } catch (error) {
    showError(recurringError, error.message);
  }
});

(async function init() {
  await loadCategories();
  await refreshRecurringExpenses();
})();
