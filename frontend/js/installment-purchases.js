renderSidebar("installment-purchases.html");

const purchaseForm = document.getElementById("purchase-form");
const purchaseError = document.getElementById("purchase-error");
const purchaseList = document.getElementById("purchase-list");
const purchaseEmpty = document.getElementById("purchase-empty");
const categorySelect = document.getElementById("purchase-category");
const firstDuePicker = createDatePicker(null);
document.getElementById("purchase-first-due-container").appendChild(firstDuePicker.container);

async function loadCategories() {
  const categories = await api.listCategories();
  categories.forEach((category) => {
    categorySelect.appendChild(el("option", { value: category.id, text: category.name }));
  });
}

function renderPurchases(purchases) {
  purchaseList.innerHTML = "";
  purchaseEmpty.classList.toggle("hidden", purchases.length > 0);

  purchases.forEach((purchase) => {
    const removeBtn = el("button", { class: "btn btn-danger", text: "Excluir compra" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteInstallmentPurchase(purchase.id);
      await refreshPurchases();
    });

    const header = el("div", { class: "page-header" }, [
      el("h2", { text: `${purchase.description} — ${formatCurrency(purchase.total_amount, purchase.currency)}` }),
      removeBtn,
    ]);

    const rows = purchase.installments.map((installment) => {
      const toggleBtn = el("button", {
        class: `table-action ${installment.status === "PAID" ? "btn-undo" : ""}`,
        text: installment.status === "PAID" ? "Desfazer" : "Marcar pago",
      });
      toggleBtn.addEventListener("click", async () => {
        await api.toggleInstallment(purchase.id, installment.id);
        await refreshPurchases();
      });
      return el("tr", {}, [
        el("td", { text: `${installment.number}/${purchase.installments_count}` }),
        el("td", { text: formatCurrency(installment.amount, purchase.currency) }),
        el("td", { text: formatDate(installment.due_date) }),
        el("td", {}, [
          el("span", {
            class: `badge ${installment.status === "PAID" ? "badge-paid" : "badge-pending"}`,
            text: installment.status === "PAID" ? "Pago" : "Pendente",
          }),
        ]),
        el("td", {}, [toggleBtn]),
      ]);
    });

    const table = el("table", { class: "data-table" }, [
      el("thead", {}, [
        el("tr", {}, [
          el("th", { text: "Parcela" }),
          el("th", { text: "Valor" }),
          el("th", { text: "Vencimento" }),
          el("th", { text: "Status" }),
          el("th", { text: "Ação" }),
        ]),
      ]),
      el("tbody", {}, rows),
    ]);

    purchaseList.appendChild(el("div", { class: "card" }, [header, table]));
  });
}

async function refreshPurchases() {
  const purchases = await api.listInstallmentPurchases();
  renderPurchases(purchases);
}

purchaseForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(purchaseError);

  const firstDueDate = firstDuePicker.getValue();
  if (!firstDueDate) {
    showError(purchaseError, "Informe a data da 1ª parcela");
    return;
  }

  const payload = {
    description: document.getElementById("purchase-description").value.trim(),
    total_amount: document.getElementById("purchase-total").value,
    currency: document.getElementById("purchase-currency").value,
    category_id: categorySelect.value ? Number(categorySelect.value) : null,
    installments_count: Number(document.getElementById("purchase-installments").value),
    first_due_date: firstDueDate,
  };

  try {
    await api.createInstallmentPurchase(payload);
    purchaseForm.reset();
    firstDuePicker.setValue(null);
    await refreshPurchases();
  } catch (error) {
    showError(purchaseError, error.message);
  }
});

(async function init() {
  await loadCategories();
  await refreshPurchases();
})();
