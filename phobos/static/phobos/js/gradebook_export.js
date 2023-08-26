
document.addEventListener("DOMContentLoaded", function () {
    const exportButton = document.getElementById("export-button");
    exportButton.addEventListener("click", function (event) {
        event.preventDefault();
        // Collect table data
        const table = document.querySelector(".table");
        const tableData = XLSX.utils.table_to_sheet(table);

        // Create a new workbook and add the data
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, tableData, "GradeBook");

        // Export the workbook as an Excel file
        XLSX.writeFile(workbook, "GradeBook.xlsx");
    });
});

