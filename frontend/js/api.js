const API_BASE_URL = "";

async function apiRequest(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = "Erro inesperado";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch (_) {
      // resposta sem corpo JSON
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

const api = {
  me: () => apiRequest("/users/me"),

  listIncomes: () => apiRequest("/users/me/incomes"),
  createIncome: (payload) => apiRequest("/users/me/incomes", { method: "POST", body: payload }),
  deleteIncome: (id) => apiRequest(`/users/me/incomes/${id}`, { method: "DELETE" }),

  listCategories: () => apiRequest("/categories"),
  createCategory: (payload) => apiRequest("/categories", { method: "POST", body: payload }),
  deleteCategory: (id) => apiRequest(`/categories/${id}`, { method: "DELETE" }),

  listRecurringExpenses: () => apiRequest("/recurring-expenses"),
  createRecurringExpense: (payload) => apiRequest("/recurring-expenses", { method: "POST", body: payload }),
  deleteRecurringExpense: (id) => apiRequest(`/recurring-expenses/${id}`, { method: "DELETE" }),

  listInstallmentPurchases: () => apiRequest("/installment-purchases"),
  createInstallmentPurchase: (payload) => apiRequest("/installment-purchases", { method: "POST", body: payload }),
  deleteInstallmentPurchase: (id) => apiRequest(`/installment-purchases/${id}`, { method: "DELETE" }),

  getDashboardSummary: (year, month) => apiRequest(`/dashboard/summary?year=${year}&month=${month}`),
  getAnnualReport: (year) => apiRequest(`/reports/annual?year=${year}`),
  getCalendar: (startDate, endDate) => apiRequest(`/calendar?start_date=${startDate}&end_date=${endDate}`),
};
