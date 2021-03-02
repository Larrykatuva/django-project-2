const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch("/search-expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((row) => {
            tbody.innerHTML += `
                <tr>
                    <td>${row.amount}</td>
                    <td>${row.category}</td>
                    <td>${row.description}</td>
                    <td>${row.date}</td>
                    <td>
                      <a href="edit-expense/${row.id}"
                      class="btn border border-success text-success btn-sm"
                      >Edit</a>
                      <a href="delete-expense/${row.id}"
                      class="btn border border-danger text-danger btn-sm"
                      >X</a>
                    </td>
                </tr>`;
          });
        }
      });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});