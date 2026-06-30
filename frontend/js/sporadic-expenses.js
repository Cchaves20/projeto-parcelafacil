renderSidebar("sporadic-expenses.html");

const sporadicForm = document.getElementById("sporadic-form");
const sporadicError = document.getElementById("sporadic-error");
const sporadicTableBody = document.getElementById("sporadic-table-body");
const sporadicEmpty = document.getElementById("sporadic-empty");
const categorySelect = document.getElementById("sporadic-category");
const submitBtn = document.getElementById("sporadic-submit-btn");
const cancelEditBtn = document.getElementById("sporadic-cancel-edit-btn");

const datePicker = createDatePicker(null);
document.getElementById("sporadic-date-container").appendChild(datePicker.container);

let editingExpenseId = null;

async function loadCategories() {
  const categories = await api.listCategories();
  categories.forEach((category) => {
    categorySelect.appendChild(el("option", { value: category.id, text: category.name }));
  });
}

function resetForm() {
  editingExpenseId = null;
  sporadicForm.reset();
  datePicker.setValue(null);
  submitBtn.textContent = "Adicionar";
  cancelEditBtn.classList.add("hidden");
}

function startEdit(expense) {
  editingExpenseId = expense.id;
  document.getElementById("sporadic-description").value = expense.description;
  document.getElementById("sporadic-amount").value = expense.amount;
  document.getElementById("sporadic-currency").value = expense.currency;
  categorySelect.value = expense.category_id || "";
  datePicker.setValue(expense.expense_date);
  submitBtn.textContent = "Salvar alterações";
  cancelEditBtn.classList.remove("hidden");
  sporadicForm.scrollIntoView({ behavior: "smooth" });
}

cancelEditBtn.addEventListener("click", resetForm);

function renderSporadicExpenses(expenses) {
  sporadicTableBody.innerHTML = "";
  sporadicEmpty.classList.toggle("hidden", expenses.length > 0);

  expenses.forEach((expense) => {
    const editBtn = el("button", { class: "table-action", text: "Editar" });
    editBtn.addEventListener("click", () => startEdit(expense));

    const removeBtn = el("button", { class: "table-action", text: "Remover" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteSporadicExpense(expense.id);
      await refreshSporadicExpenses();
    });

    sporadicTableBody.appendChild(
      el("tr", {}, [
        el("td", { text: expense.description }),
        el("td", { text: formatCurrency(expense.amount, expense.currency) }),
        el("td", {}, [
          el("span", {
            class: `badge ${expense.currency === "USD" ? "badge-usd" : "badge-brl"}`,
            text: expense.currency,
          }),
        ]),
        el("td", { text: expense.category_id ? (expense.category_name || "—") : "—" }),
        el("td", { text: formatDate(expense.expense_date) }),
        el("td", {}, [editBtn, removeBtn]),
      ])
    );
  });
}

async function refreshSporadicExpenses() {
  const expenses = await api.listSporadicExpenses();
  renderSporadicExpenses(expenses);
}

sporadicForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(sporadicError);

  const expenseDate = datePicker.getValue();
  if (!expenseDate) {
    showError(sporadicError, "Informe a data do gasto");
    return;
  }

  const payload = {
    description: document.getElementById("sporadic-description").value.trim(),
    amount: document.getElementById("sporadic-amount").value,
    currency: document.getElementById("sporadic-currency").value,
    category_id: categorySelect.value ? Number(categorySelect.value) : null,
    expense_date: expenseDate,
  };

  try {
    if (editingExpenseId) {
      await api.updateSporadicExpense(editingExpenseId, payload);
    } else {
      await api.createSporadicExpense(payload);
    }
    resetForm();
    await refreshSporadicExpenses();
  } catch (error) {
    showError(sporadicError, error.message);
  }
});

(async function init() {
  await loadCategories();
  await refreshSporadicExpenses();
})();
