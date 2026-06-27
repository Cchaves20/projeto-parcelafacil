requireAuth();
renderSidebar("calendar.html");

const monthSelect = document.getElementById("month-select");
const yearSelect = document.getElementById("year-select");
const calendarList = document.getElementById("calendar-list");
const calendarEmpty = document.getElementById("calendar-empty");

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

function lastDayOfMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

function groupByDate(items) {
  const groups = new Map();
  items.forEach((item) => {
    if (!groups.has(item.due_date)) groups.set(item.due_date, []);
    groups.get(item.due_date).push(item);
  });
  return groups;
}

async function loadCalendar() {
  const year = Number(yearSelect.value);
  const month = Number(monthSelect.value);
  const lastDay = String(lastDayOfMonth(year, month)).padStart(2, "0");
  const startDate = `${year}-${String(month).padStart(2, "0")}-01`;
  const endDate = `${year}-${String(month).padStart(2, "0")}-${lastDay}`;

  const items = await api.getCalendar(startDate, endDate);
  renderCalendar(items);
}

function renderCalendar(items) {
  calendarList.innerHTML = "";
  calendarEmpty.classList.toggle("hidden", items.length > 0);

  const groups = groupByDate(items);
  const sortedDates = Array.from(groups.keys()).sort();

  sortedDates.forEach((date) => {
    const groupItems = groups.get(date).map((item) =>
      el("div", { class: "calendar-item" }, [
        el("div", { class: "item-name" }, [
          el("span", { text: item.type === "installment" ? "📦" : "🔁" }),
          el("span", { text: item.name }),
        ]),
        el("div", { class: "item-amount", text: formatCurrency(item.amount, item.currency) }),
      ])
    );

    calendarList.appendChild(
      el("div", { class: "calendar-day-group" }, [
        el("h3", { text: formatDate(date) }),
        ...groupItems,
      ])
    );
  });
}

monthSelect.addEventListener("change", loadCalendar);
yearSelect.addEventListener("change", loadCalendar);

populateSelectors();
loadCalendar();
