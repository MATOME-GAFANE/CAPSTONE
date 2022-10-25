$(document).ready(function() {
  $('.filter').change(function(){

    filter_function();
    
    //calling filter function each select box value change
    
  });

  $('table tbody tr').show(); //intially all rows will be shown

  function filter_function(){
    $('table tbody tr').hide(); //hide all rows
    
    var surnameFlag = 0;
    //var surnameValue = $('#input_surname').text();
    var surnameValue = $('#input_surname').val();

    var ratingFlag = 0;
    var ratingValue = $('#input_rating').val();

    var institutionFlag = 0;
    var institutionValue = $('#input_institution').val();

    var primaryFlag = 0;
    var primaryValue = $('#input_Primary').val();

    var secondaryFlag = 0;
    var secondaryValue = $('#input_Secondary').val();

    var specializationsFlag = 0;
    var specializationsValue = $('#input_Specializations').val();
    
    
    //setting intial values and flags needed
    
   //traversing each row one by one
    $('table tr').each(function() {  

      
      var surnameTable = $(this).find('td:eq(0)').text().toLowerCase();
      surnameValue = surnameValue.toLowerCase();
      //alert(surnameValue)
      if(surnameValue == 0){   //if no value then display row
      surnameFlag = 1;
      }
      //surnameTable = $(this).find('td:eq(0)').text().toLowerCase()
      else if(surnameValue == surnameTable){ 
        surnameFlag = 1;       //if value is same display row
      }
      else{
        surnameFlag = 0;
      }
      
      var ratingTable = $(this).find('td:eq(4)').text().toLowerCase();
      ratingValue = ratingValue.toLowerCase();
      if(ratingValue == 0){   //if no value then display row
        ratingFlag = 1;
      }
      else if(ratingValue == ratingTable){ 
        ratingFlag = 1;       //if value is same display row
      }
      else{
        ratingFlag = 0;
      }
      

      var institutionTable = $(this).find('td:eq(3)').text().toLowerCase();
      institutionValue = institutionValue.toLowerCase();
      if(institutionValue == 0){   //if no value then display row
        institutionFlag = 1;
      }
      else if(institutionValue == institutionTable){ 
        institutionFlag = 1;       //if value is same display row
      }
      else{
        institutionFlag = 0;
      }
      

      var primaryTable = $(this).find('td:eq(5)').text().toLowerCase();
      primaryValue = primaryValue.toLowerCase();
      if(primaryValue == 0){   //if no value then display row
        primaryFlag = 1;
      }
      //var str1 = $(this).find('td.primaryResearch').data('primaryResearch');

      else if(primaryTable.indexOf(primaryValue) > -1){  //parentString.indexOf(substring);
        primaryFlag = 1;       //if value is same display row
      }
      else{
        primaryFlag = 0;
      }
      

      var secondaryTable = $(this).find('td:eq(6)').text().toLowerCase();
      secondaryValue = secondaryValue.toLowerCase();
      if(secondaryValue == 0){   //if no value then display row
        secondaryFlag = 1;
      }
      else if(secondaryTable.indexOf(secondaryValue) > -1){ 
        secondaryFlag = 1;       //if value is same display row
      }
      else{
        secondaryFlag = 0;
      }
      

      var specilizationsTable = $(this).find('td:eq(7)').text().toLowerCase();
      specializationsValue = specializationsValue.toLowerCase();
      if(specializationsValue == 0){   //if no value then display row
        specializationsFlag = 1;
      }
      else if(specilizationsTable.indexOf(specializationsValue) > -1){ 
        specializationsFlag = 1;       //if value is same display row
      }
      else{
        specializationsFlag = 0;
      }
      
      if(surnameFlag && ratingFlag && institutionFlag && primaryFlag && secondaryFlag && specializationsFlag){
        $(this).show();  //displaying row which satisfies all conditions
      }
      
  
  });
      
  }

});
