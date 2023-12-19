// Function to search the CSV file
function searchCSV() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    
    // Load and parse the CSV file
    Papa.parse("out.csv", {
        header: true,
        download: true,
        skipEmptyLines: true,
        complete: function (results) {
            const data = results.data;
            const matchingRows = data.filter(function (row) {
                return row.columnName.toLowerCase().includes(searchTerm); // Replace 'columnName' with the actual column name you want to search
            });

            displayResults(matchingRows);
        }
    });
}

// Function to display search results
function displayResults(results) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (results.length === 0) {
        resultsDiv.innerHTML = "No results found.";
        return;
    }

    const resultList = document.createElement("ul");
    results.forEach(function (row) {
        const listItem = document.createElement("li");
        listItem.textContent = row.columnName; // Replace 'columnName' with the actual column name you want to display
        resultList.appendChild(listItem);
    });

    resultsDiv.appendChild(resultList);
}
