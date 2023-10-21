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

        // Get course name from export-button's data attribute
        const courseName = exportButton.dataset.courseName || "Course";

        // Get current date
        const currentDate = new Date();
        const formattedDate = (currentDate.getMonth() + 1).toString().padStart(2, '0') + 
                              '-' + currentDate.getDate().toString().padStart(2, '0') + 
                              '-' + currentDate.getFullYear();

        // Create file name
        const fileName = `${courseName}_GradeBook_${formattedDate}.xlsx`;

        // Export the workbook as an Excel file
        XLSX.writeFile(workbook, fileName);
    });
});
