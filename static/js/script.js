function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

function search_researchers(){
    var input = document.getElementById("researcher_search");
}

function filter(index, value, id){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById(id);
  filter = input.value.toUpperCase();
  table = document.getElementById("ResearchersTable");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[index];

    // if there is a value in the field
    if (td) {
      txtValue = td.textContent || td.innerText;

      // Showing record
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";

      // Hiding record
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}