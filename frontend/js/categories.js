renderSidebar("categories.html");

const categoryForm = document.getElementById("category-form");
const categoryError = document.getElementById("category-error");
const categoryTableBody = document.getElementById("category-table-body");
const categoryEmpty = document.getElementById("category-empty");

function renderCategories(categories) {
  categoryTableBody.innerHTML = "";
  categoryEmpty.classList.toggle("hidden", categories.length > 0);

  categories.forEach((category) => {
    const removeBtn = el("button", { class: "table-action", text: "Remover" });
    removeBtn.addEventListener("click", async () => {
      await api.deleteCategory(category.id);
      await refreshCategories();
    });

    categoryTableBody.appendChild(
      el("tr", {}, [
        el("td", { text: category.name }),
        el("td", {}, [removeBtn]),
      ])
    );
  });
}

async function refreshCategories() {
  const categories = await api.listCategories();
  renderCategories(categories);
}

categoryForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError(categoryError);

  const name = document.getElementById("category-name").value.trim();

  try {
    await api.createCategory({ name });
    categoryForm.reset();
    await refreshCategories();
  } catch (error) {
    showError(categoryError, error.message);
  }
});

refreshCategories();
