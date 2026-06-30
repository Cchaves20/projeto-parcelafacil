renderSidebar("savings.html");

const boxForm = document.getElementById("box-form");
const boxError = document.getElementById("box-error");
const boxList = document.getElementById("box-list");
const boxEmpty = document.getElementById("box-empty");
const boxSubmitBtn = document.getElementById("box-submit-btn");
const boxCancelEditBtn = document.getElementById("box-cancel-edit-btn");

let editingBoxId = null;

function resetBoxForm() {
  editingBoxId = null;
  boxForm.reset();
  document.getElementById("box-rate").value = "0";
  boxSubmitBtn.textContent = "Criar caixinha";
  boxCancelEditBtn.classList.add("hidden");
}

function startEditBox(box) {
  editingBoxId = box.id;
  document.getElementById("box-name").value = box.name;
  document.getElementById("box-currency").value = box.currency;
  document.getElementById("box-rate").value = box.annual_rate;
  boxSubmitBtn.textContent = "Salvar alterações";
  boxCancelEditBtn.classList.remove("hidden");
  boxForm.scrollIntoView({ behavior: "smooth" });
}

boxCancelEditBtn.addEventListener("click", resetBoxForm);

boxForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(boxError);

  const payload = {
    name: document.getElementById("box-name").value.trim(),
    currency: document.getElementById("box-currency").value,
    annual_rate: document.getElementById("box-rate").value,
  };

  try {
    if (editingBoxId) {
      await api.updateSavingsBox(editingBoxId, payload);
    } else {
      await api.createSavingsBox(payload);
    }
    resetBoxForm();
    await refreshBoxes();
  } catch (error) {
    showError(boxError, error.message);
  }
});

function renderBoxes(boxes) {
  boxList.innerHTML = "";
  boxEmpty.classList.toggle("hidden", boxes.length > 0);

  boxes.forEach((box) => {
    const editBoxBtn = el("button", { class: "btn btn-secondary", text: "Editar caixinha" });
    editBoxBtn.addEventListener("click", () => startEditBox(box));

    const deleteBoxBtn = el("button", { class: "btn btn-danger", text: "Excluir caixinha" });
    deleteBoxBtn.addEventListener("click", async () => {
      await api.deleteSavingsBox(box.id);
      await refreshBoxes();
    });

    const header = el("div", { class: "page-header" }, [
      el("div", {}, [
        el("h2", { text: box.name }),
        el("p", {
          text: `Saldo: ${formatCurrency(box.balance, box.currency)} · Rendimento: ${box.annual_rate}% a.a. · Moeda: ${box.currency}`,
        }),
      ]),
      el("div", { class: "btn-group" }, [editBoxBtn, deleteBoxBtn]),
    ]);

    // Transaction form
    const txAmountInput = el("input", { type: "number", step: "0.01", placeholder: "Valor (negativo para retirada)" });
    const txDescInput = el("input", { type: "text", placeholder: "Descrição (opcional)" });
    const txSubmitBtn = el("button", { type: "button", class: "btn btn-primary", text: "Adicionar" });
    txSubmitBtn.addEventListener("click", async () => {
      const amount = txAmountInput.value;
      if (!amount || Number(amount) === 0) return;
      await api.addSavingsTransaction(box.id, {
        amount,
        description: txDescInput.value.trim() || null,
      });
      await refreshBoxes();
    });

    const txForm = el("div", { class: "inline-form" }, [
      el("div", { class: "form-field form-field-grow" }, [txAmountInput]),
      el("div", { class: "form-field form-field-grow" }, [txDescInput]),
      txSubmitBtn,
    ]);

    // Transaction history
    const txRows = box.transactions
      .slice()
      .sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date))
      .map((tx) => {
        const deleteBtn = el("button", { class: "table-action", text: "Remover" });
        deleteBtn.addEventListener("click", async () => {
          await api.deleteSavingsTransaction(box.id, tx.id);
          await refreshBoxes();
        });
        return el("tr", {}, [
          el("td", { text: formatCurrency(tx.amount, box.currency) }),
          el("td", { text: tx.description || "—" }),
          el("td", { text: new Date(tx.transaction_date).toLocaleDateString("pt-BR") }),
          el("td", {}, [deleteBtn]),
        ]);
      });

    const txTable =
      txRows.length > 0
        ? el("table", { class: "data-table" }, [
            el("thead", {}, [
              el("tr", {}, [
                el("th", { text: "Valor" }),
                el("th", { text: "Descrição" }),
                el("th", { text: "Data" }),
                el("th", { text: "Ação" }),
              ]),
            ]),
            el("tbody", {}, txRows),
          ])
        : el("p", { class: "empty-state", text: "Nenhuma movimentação ainda." });

    boxList.appendChild(
      el("div", { class: "card" }, [
        header,
        el("h3", { text: "Nova movimentação" }),
        txForm,
        el("h3", { text: "Histórico" }),
        txTable,
      ])
    );
  });
}

async function refreshBoxes() {
  const boxes = await api.listSavingsBoxes();
  renderBoxes(boxes);
}

(async function init() {
  await refreshBoxes();
})();
